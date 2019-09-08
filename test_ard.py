from serial import Serial
from time import sleep
s = Serial('/dev/ttyUSB0', 9600, timeout=100)
s.rtscts = True
throt = "t100\n"
s.write(throt.encode("utf-8"))
steer = "s60\n"
s.write(steer.encode("utf-8"))
sleep(1)
throt = "t100\n"
s.write(throt.encode("utf-8"))
steer = "s200\n"
s.write(steer.encode("utf-8"))