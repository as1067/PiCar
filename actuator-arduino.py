from serial import Serial
angle = 125
minturn = 5
ser = ser = Serial('/dev/ttyUSB0', 9600, timeout=1)
cur_speed = 0

# init
def init(default_speed=50):
    stop()
    set_speed(default_speed)
    print ("actuator-arduino init completed.")

def set_speed(speed):
    ser.write("t" + str(speed)+"\n")
    cur_speed = speed
    
def get_speed():
    return cur_speed

def stop():
    ser.write("t90\n")
              
def get_angle():
    return angle
# steering
def center():
    ser.write("s125\n")    
def set_angle(a):
    ser.write("s"+str(a)+"\n")  
    angle = a

# exit    
def turn_off():
    stop()
    center()
    ser.close()
