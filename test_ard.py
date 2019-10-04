from serial import Serial
from time import sleep
s = Serial('/dev/serial0', 9600, timeout=10)
s.rtscts = True
sleep(10)
throt = "t120\n"
s.write(throt.encode("utf-8"))
sleep(3)
steer = "s200\n"
sleep(3)
s.write(steer.encode("utf-8"))
