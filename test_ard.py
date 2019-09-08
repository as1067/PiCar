from serial import Serial
s = Serial('/dev/ttyUSB0', 9600, timeout=100)
while True:
    s.write("t110")