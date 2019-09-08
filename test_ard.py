from serial import Serial
s = Serial('/dev/ttyUSB0', 9600, timeout=100)
while True:
    throt = "t100"
    s.write(throt.encode("utf-8"))