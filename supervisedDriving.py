import serial
class Driver():

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=100)
    
    def getSpeed(self):
        waiting = True
        while waiting:
            speed = self.ser.readline()
            angle = angle.decode("utf-8")
            if speed[0] == "t":
                waiting = False
                return int(speed[1:])
    
    def getAngle(self):
        waiting = True
        while waiting:
            angle = self.ser.readline()
            angle = angle.decode("utf-8")
            print(angle)
            if angle[0] == "s" and int(angle[1:])<=250 and int(angle[1:])>=0:
                waiting = False
                return int(angle[1:])