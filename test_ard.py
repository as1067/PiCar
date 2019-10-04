from serial import Serial
from time import sleep
s = Serial('/dev/ttyUSB0', 9600, timeout=10)
sleep(10)
print("Finished")
s.rtscts = True
throt = "t160\n"
print("write")
s.write(throt.encode("utf-8"))
sleep(3)
steer = "s200\n"
print("write")
s.write(steer.encode("utf-8"))
sleep(3)
s.close()