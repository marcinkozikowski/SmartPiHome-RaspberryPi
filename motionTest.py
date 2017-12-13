import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
print "Motion detection thred started"
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.IN)

while True:
    i=GPIO.input(14)
    if i==0:                 #When output from motion sensor is LOW
        time.sleep(3)
        print "No intruders",i
    elif i==1:               #When output from motion sensor is HIGH
        time.sleep(3)
        print "Intruder detected",i
