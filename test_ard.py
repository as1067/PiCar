from serial import Serial
s = Serial('/dev/ttyUSB0', 9600, timeout=100)
while True:
    s.rtscts = True
    throt = "t100\n"
    s.write(throt.encode("utf-8"))