import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout

# Set up pin 11 for PWM
GPIO.setup(40,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(40, 50)# Sets up pin 11 as a PWM pin
GPIO.setup(12,GPIO.OUT)
q = GPIO.PWM(12,50)
q.start(0)               # Starts running PWM on the pin and sets it to 0
p.start(0)
steer = Serial('/dev/ttyUSB0', 9600, timeout=1)

# Move the servo back and forth
for i in range(200):
    print(i)
    # q.ChangeDutyCycle(i)
    #p.ChangeDutyCycle(i)
    steer.write(bytes(i)+"\n","utf-8"))
    sleep(.1)

# Clean up everything
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()