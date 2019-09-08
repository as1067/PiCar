from serial import Serial
s = Serial('/dev/ttyUSB0', 9600, timeout=1)
while True:
    s.write(bytes("t110","utf-8"))