import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BCM)
 
Motor1A = 1
Motor1B = 7
Motor1E = 16
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)


for num in range(0,2):
    sleep(2)
    print ("Turning motor forward")
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
    sleep(0.055)
    GPIO.output(Motor1E,GPIO.LOW)

for num in range(0,2):
    sleep(2)
    print ("Turning motor bacwards")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
    sleep(0.04)
    GPIO.output(Motor1E,GPIO.LOW)

GPIO.cleanup()

