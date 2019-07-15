from serial import Serial
angle = 125
minturn = 5
ser = Serial('/dev/ttyUSB0', 9600, timeout=1)
cur_speed = 0

# init
def init(default_speed=50):
    stop()
    set_speed(default_speed)
    print ("actuator-arduino init completed.")

def set_speed(speed):
    ser.write(bytes("t" + str(speed)+"\n","utf-8"))
    cur_speed = speed
    
def get_speed():
    return cur_speed

def stop():
    ser.write(bytes("t90\n","utf-8"))
              
def get_angle():
    return angle
# steering
def center():
    ser.write(bytes("s125\n","utf-8"))
def set_angle(a):
    ser.write(bytes("s"+str(a)+"\n","utf-8"))
    angle = a

# exit    
def turn_off():
    stop()
    center()
    ser.close()
