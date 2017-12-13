import RPi.GPIO as GPIO
import os
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.OUT)
pwm = GPIO.PWM(10,50)

pwm.start(6)
#krecenie w lewo
pwm.ChangeDutyCycle(2.5)    # 0 stopni zamkniete drzwi
time.sleep(3)
pwm.stop()

#zatrzymanie
pwm.start(6)
pwm.ChangeDutyCycle(7)
time.sleep(2)
pwm.stop()
        

#krecenie w prawo
pwm.start(6)
pwm.ChangeDutyCycle(10)    #Neutral otwarte drzwi
time.sleep(3)
#set rotating servo
pwm.stop()

#GPIO.cleanup()
        
