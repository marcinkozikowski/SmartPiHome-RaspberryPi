import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setmode(GPIO.BCM)

 
Motor1A = 1
Motor1B = 7
Motor1E = 16
PWM_Frequency = 8

Dutycycle1 = 10
Dutycycke2 = 50
 
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)


#Go forward
p = GPIO.PWM(Motor1A,PWM_Frequency)
GPIO.output(Motor1B,GPIO.LOW)
GPIO.output(Motor1E,GPIO.HIGH)

p.start(10)
 
#If dutycycle is about 10 and sleep about 1.1 seconds then it will make about two rounds
sleep(2)

GPIO.output(Motor1E,GPIO.LOW)

sleep(2)

#Go backwards
p = GPIO.PWM(Motor1B,PWM_Frequency)
GPIO.output(Motor1A,GPIO.LOW)
GPIO.output(Motor1E,GPIO.HIGH)

p.start(10)
 
#If dutycycle is about 10 and sleep about 1.1 seconds then it will make about two rounds
sleep(2)
 
print ("Stopping motor")
GPIO.output(Motor1E,GPIO.LOW)
 
GPIO.cleanup()
