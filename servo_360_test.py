import RPi.GPIO as GPIO
import os
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(8,GPIO.OUT)
pwm = GPIO.PWM(8,50)

#kanaly 8 i 25 

#krecenie do gory
pwm.start(50)
pwm.ChangeDutyCycle(9.3)    #Neutral otwarte drzwi
time.sleep(1)
pwm.stop()
time.sleep(5)



pwm.start(50)
#krecenie w rolety o dolu
pwm.ChangeDutyCycle(6)    # 0 stopni zamkniete drzwi
time.sleep(1)
pwm.stop()
#set rotating servo


GPIO.cleanup()
        
