import RPi.GPIO as GPIO
from time import sleep   # Imports sleep (aka wait or pause) into the program

GPIO.setmode(GPIO.BOARD)  # Sets the pin numbering system to use the physical layout
GPIO.setup(12, GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)

throttle = GPIO.PWM(12, 50)  # Sets up pin 11 as a PWM pin
steer = Serial('/dev/ttyUSB0', 9600, timeout=1)
cur_speed = 0
angle = 0

def init(default_speed=12):
    throttle.start(0)
    steer.write(bytes(str(125)+"\n","utf-8"))
def set_speed(speed):
    cur_speed = speed
    throttle.ChangeDutyCycle(speed)

def get_speed():
    return cur_speed


def get_angle():
    return angle

def stop():
    throttle.ChangeDutyCycle(15)


# steering
def center():
    steer.ChangeDutyCycle(5)


def set_angle(a):
    angle = a
    serial.write(bytes(str(a)+"\n","utf-8"))


# exit
def turn_off():
    throttle.stop()
    steer.stop()
    GPIO.cleanup()