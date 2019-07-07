#!/usr/bin/python
import os
import time
import atexit
import math
import numpy as np
import sys
import params
import argparse
import cv2
from PIL import Image,ImageDraw
import local_common as cm
from camerapicamera import VideoStream
import input_kbd
from supervisedDriving import Driver

##########################################################
# import deeppicar's sensor/actuator modules
##########################################################
camera = VideoStream()
actuator = __import__(params.actuator)

##########################################################
# global variable initialization
##########################################################
use_dnn = False
use_thread = True
view_video = False
fpv_video = False

cfg_cam_res = (320, 240)
cfg_cam_fps = 30
cfg_throttle = 50 # 50% power.

NCPU = 2

frame_id = 0
angle = 0
btn   = ord('k') # center
period = 0.2 # sec (=50ms)
driver = Driver()
##########################################################
# local functions
##########################################################

def g_tick():
    t = time.time()
    count = 0
    while True:
        count += 1
        yield max(t + count*period - time.time(),0)

def turn_off():
    actuator.stop()
    camera.stop()

    keyfile.close()
    keyfile_btn.close()
    vidfile.release()

##########################################################
# program begins
##########################################################
parser = argparse.ArgumentParser(description='DeepPicar main')
parser.add_argument("-d", "--dnn", help="Enable DNN", action="store_true")
parser.add_argument("-t", "--throttle", help="throttle percent. [0-100]%", type=int)
parser.add_argument("-n", "--ncpu", help="number of cores to use.", type=int)
parser.add_argument("-f", "--fpvvideo", help="Take FPV video of DNN driving", action="store_true")
parser.add_argument("-g", "--guide", help="Guided driving", action="store_true")
parser.add_argument("-v", "--video",action="store_true")

args = parser.parse_args()

if args.dnn:
    print ("DNN is on")
    use_dnn = True
if args.throttle:
    cfg_throttle = args.throttle
    print ("throttle = %d pct" % (args.throttle))
if args.ncpu > 0:
    NCPU = args.ncpu
if args.fpvvideo:
    fpv_video = True
if args.guide:
    guided = True
if args.video:
    view_video = True

# create files for data recording
keyfile = open('out-key.csv', 'w+')
keyfile_btn = open('out-key-btn.csv', 'w+')
keyfile.write("ts_micro,frame,wheel\n")
keyfile_btn.write("ts_micro,frame,btn,speed\n")
rec_start_time = 1
try:
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
except AttributeError as e:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
vidfile = cv2.VideoWriter('out-video.avi', fourcc,
                          cfg_cam_fps, cfg_cam_res)

# initlaize deeppicar modules
actuator.init(cfg_throttle)
atexit.register(turn_off)

# initilize dnn model
if use_dnn == True:
    print ("Load TF")
    import tensorflow as tf
    model = __import__(params.model)
    import local_common as cm
    import preprocess

    print ("Load Model")
    config = tf.ConfigProto(intra_op_parallelism_threads=NCPU,
                            inter_op_parallelism_threads=NCPU, \
                            allow_soft_placement=True,
                            device_count = {'CPU': 1})

    sess = tf.InteractiveSession(config=config)
    saver = tf.train.Saver()
    model_load_path = cm.jn(params.save_dir, params.model_load_file)
    saver.restore(sess, model_load_path)
    print ("Done..")

# null_frame = np.zeros((cfg_cam_res[0],cfg_cam_res[1],3), np.uint8)
# cv2.imshow('frame', null_frame)
camera.start()
time.sleep(2)
g = g_tick()
start_ts = time.time()
frame_arr = []
angle_arr = []
# enter main loop
while True:
    if use_thread:
        time.sleep(next(g))
    frame = camera.read()
    ts = time.time()

    # read a frame
    # ret, frame = cap.read()

    if view_video == True:
        cv2.imshow('frame', frame)
        ch = cv2.waitKey(1) & 0xFF
    else:
        ch = ord(input_kbd.read_single_keypress())

    if guided:
        angle = driver.getAngle()
    
    if ch == ord('t'):
        print ("toggle video mode")
        if view_video == False:
            view_video = True
        else:
            view_video = False
    elif ch == ord('d'):
        print ("toggle DNN mode")
        if use_dnn == False:
            use_dnn = True
        else:
            use_dnn = False

    if use_dnn == True:
        # 1. machine input
        img = preprocess.preprocess(frame)
        angle = model.y.eval(feed_dict={model.x: [img]})[0][0]

        if angle>120 and angle<130:
            actuator.center()
        else:
            actuator.set_angle(angle)

    dur = time.time() - ts
    if dur > period:
        print("%.3f: took %d ms - deadline miss."
              % (ts - start_ts, int(dur * 1000)))
    else:
        print("%.3f: took %d ms" % (ts - start_ts, int(dur * 1000)))

    if rec_start_time > 0 and not frame is None:
        print("recording")
        # increase frame_id
        frame_id += 1

        # write input (angle)
        str = "{},{},{}\n".format(int(ts*1000), frame_id, angle)
        keyfile.write(str)

        # write input (button: left, center, stop, speed)
        str = "{},{},{},{}\n".format(int(ts*1000), frame_id, btn, cfg_throttle)
        keyfile_btn.write(str)

        if use_dnn and fpv_video:
            textColor = (255,255,255)
            bgColor = (0,0,0)
            newImage = Image.new('RGBA', (100, 20), bgColor)
            drawer = ImageDraw.Draw(newImage)
            drawer.text((0, 0), "Frame #{}".format(frame_id), fill=textColor)
            drawer.text((0, 10), "Angle:{}".format(angle), fill=textColor)
            newImage = cv2.cvtColor(np.array(newImage), cv2.COLOR_BGR2RGBA)
            frame = cm.overlay_image(frame,
                                     newImage,
                                     x_offset = 0, y_offset = 0)
        # write video stream
        vidfile.write(frame)
        if frame_id >= 1000:
            print ("recorded 1000 frames")
            break
        print ("%.3f %d %.3f %d %d(ms)" %
           (ts, frame_id, angle, btn, int((time.time() - ts)*1000)))
    camera.update()


print ("Finish..")
turn_off()
