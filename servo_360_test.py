import RPi.GPIO as GPIO
import os
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.OUT)
pwm = GPIO.PWM(10,50)

pwm.start(7.5)
#krecenie w lewo
pwm.ChangeDutyCycle(5)    # 0 stopni zamkniete drzwi
time.sleep(2)

#krecenie w prawo
#pwm.start(7.5)
pwm.ChangeDutyCycle(9.5)    #Neutral otwarte drzwi
time.sleep(2)
#set rotating servo
pwm.stop()


#zatrzymanie
pwm.ChangeDutyCycle(7.5)
time.sleep(30)
pwm.stop()
        



#GPIO.cleanup()
        
