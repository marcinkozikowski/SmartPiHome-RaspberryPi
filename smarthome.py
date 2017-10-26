import RPi.GPIO as GPIO
import os
import time
import sys
import json
import dht11
import datetime
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from gpiozero import MotionSensor

channel = 'SmartPiHome'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Read temp and humidity from 26 pin
tempSensor = dht11.DHT11(pin=26)

#Livinf room diod
GPIO.setup(7,GPIO.OUT)   
GPIO.setup(11,GPIO.OUT)

#DC motor controling blind
Motor1A = 1
Motor1B = 7
Motor1E = 16
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
                             
pnconfig = PNConfiguration()
 
pnconfig.subscribe_key = 'sub-c-0baf6e4c-c5ff-11e6-b2ab-0619f8945a4f'
pnconfig.publish_key = 'pub-c-2902e976-c6d8-41bd-bebf-f3a14c238494'

#konfiguracja PubNub
pubnub = PubNub(pnconfig)
 
#wysylanie  wiadomosci
def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        print("Super udalo sie wyslac wiadomosc")
        pass  # Message successfully published to specified channel.
    else:
        print("lipa wiadomosc nie zostala wyslana")
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
 
#odbieranie wiadomosci 
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            print("Cos dziala")
            pass  # This event happens when radio / connectivity is lost
 
        elif status.category == PNStatusCategory.PNConnectedCategory:
            print("odpowiadam na zapytanie")
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel(channel).message({'type':'info','what':'Welcome note','Message':'hello!!'}).async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            print("Cos dziala")
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            print("Cos dziala")
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
 
    def message(self, pubnub, message):
        m =str(message.message)
        type = message.message['type']
        print (type)

        if(type == "light"):
            led_light(int(message.message['pin_number']),int(message.message['state']))
        elif(type == "temp"):
            temp_handler()
        elif(type =='door'):
            pin = int(message.message['pin_number'])
            state = int(message.message['state'])
            door_handler(pin,state)
        elif(type =='alarm'):
            pin = message.message['pin_number']
            state = message.message['state']
            alarm_handler(pin,state)
        elif(type=="blind"):
            motor_number=message.message['number']
            direction = message.message['direction']
            time = message.message['time']
            blind_handler(motor_number,direction,time)
        
        pass  # Handle new message stored in message.message
 

pubnub.publish().channel(channel).message({"Hello":"Hello from SmartPi I`m ready to take care of your SmartHome"}).sync()

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels(channel).execute()


#Funkcje sterujace podezspolami

#Function to control dc motor go forward or backowards for some period of time
def blind_handler(motor_number,direction,motion_time):
    if(motor_number==1):
        if(direction==1):
            print ("Turning motor1 forward",motion_time)
            GPIO.output(Motor1A,GPIO.HIGH)
            GPIO.output(Motor1B,GPIO.LOW)
            GPIO.output(Motor1E,GPIO.HIGH)
 
            time.sleep(motion_time)
            GPIO.output(Motor1E,GPIO.LOW)
        elif(direction==0):
            print ("Turning motor1 backwards",motion_time)
            GPIO.output(Motor1A,GPIO.LOW)
            GPIO.output(Motor1B,GPIO.HIGH)
            GPIO.output(Motor1E,GPIO.HIGH)
            time.sleep(motion_time)
            GPIO.output(Motor1E,GPIO.LOW)
    elif(motor_number==2):
        if(direction==1):
            print ("Turning motor2 forward",motion_time)
            GPIO.output(Motor2A,GPIO.HIGH)
            GPIO.output(Motor2B,GPIO.LOW)
            GPIO.output(Motor2E,GPIO.HIGH)
            time.sleep(motion_time)
            GPIO.output(Motor2E,GPIO.LOW)
        elif(direction==0):
            print ("Turning motor2 backwards",motion_time)
            GPIO.output(Motor2A,GPIO.LOW)
            GPIO.output(Motor2B,GPIO.HIGH)
            GPIO.output(Motor2E,GPIO.HIGH)
            time.sleep(motion_time)
            GPIO.output(Motor2E,GPIO.LOW)
    pubnub.publish().channel(channel).message({'type':'info','what':'motor','number':motor_number,'direction':direction,'time':motion_time}).sync()
            

#Control led light which (pinNumber of led and state on or off)
def led_light(pin_number,newState):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number,GPIO.OUT)
    GPIO.output(pin_number,newState)
    pubnub.publish().channel(channel).message({'type':'info','what':'light','pin':pin_number,'state':newState}).sync()

#Function to control alarm buzzer
def alarm_handler(pin_number,newState):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number,GPIO.OUT)
    GPIO.output(pin_number,newState)
    pubnub.publish().channel(channel).message({'type':'info','what':'alarm','pin':pin_number,'state':newState}).sync()
        
#Function to send new data about temp and humidity
def temp_handler():
    temp=23
    humidity=50
    for x in range(0,10):
        result = tempSensor.read()
        if result.is_valid():
            temp = result.temperature
            humidity = result.humidity
    pubnub.publish().channel(channel).message({'type':'info','what':'temp','pin':temp,'state':humidity}).sync()


#Control door open/close
def door_handler(door_number,newState):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(door_number,GPIO.OUT)
    pwm = GPIO.PWM(door_number,50)
    pwm.start(7.0)
    #zamykanie drzwi 
    if(newState==False):
        pwm.ChangeDutyCycle(2.5)    # 0 stopni zamkniete drzwi
        time.sleep(1)
        pubnub.publish().channel(channel).message({'type':'info','what':'door','pin':door_number,'state':newState}).sync()

    #otwieranie drzwi
    elif(newState==True):
        pwm.ChangeDutyCycle(7.0)    #Neutral otwarte drzwi
        time.sleep(1)
        pubnub.publish().channel(channel).message({'type':'info','what':'door','pin':door_number,'state':newState}).sync()
    

    #pwm.ChangeDutyCycle(12.5)   #180 stopni
  
    
    

