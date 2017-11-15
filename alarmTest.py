import RPi.GPIO as GPIO
import os
import time
import sys
import json
import dht11
import datetime
import thread
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from gpiozero import MotionSensor

GPIO.setmode(GPIO.BCM)
GPIO.setup(11,GPIO.OUT)
GPIO.output(11,0)
