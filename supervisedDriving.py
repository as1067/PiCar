import serial
class Driver():

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    
    def getSpeed(self):
        waiting = True
        while waiting:
            speed = self.ser.readline()
            if speed[0] == "t":
                waiting = False
                return int(speed[1:])
    
    def getAngle(self):
        waiting = True
        while waiting:
            angle = self.ser.readline()
            if angle[0] == "s":
                waiting = False
                return int(angle[1:])