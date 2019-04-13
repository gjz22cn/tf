#!/usr/bin/python
import sys
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
args = sys.argv
pin_1 = 18 # GPIO PIN 17
pin_2 = 23 # GPIO PIN 17
pin_3 = 24 # GPIO PIN 17
pin_4 = 25 # GPIO PIN 17
ctl = args[1] #Argument 1 for ON/OFF
if (int(ctl) == 1):
    GPIO.setup(pin_1, GPIO.OUT)
    GPIO.output(pin_1,GPIO.HIGH)
    GPIO.setup(pin_2, GPIO.OUT)
    GPIO.output(pin_2,GPIO.HIGH)
    GPIO.setup(pin_3, GPIO.OUT)
    GPIO.output(pin_3,GPIO.HIGH)
    GPIO.setup(pin_4, GPIO.OUT)
    GPIO.output(pin_4,GPIO.HIGH)

if (int(ctl) == 0):
    GPIO.setup(pin_1, GPIO.OUT)
    GPIO.output(pin_1, GPIO.LOW)
    GPIO.setup(pin_2, GPIO.OUT)
    GPIO.output(pin_2, GPIO.LOW)
    GPIO.setup(pin_3, GPIO.OUT)
    GPIO.output(pin_3, GPIO.LOW)
    GPIO.setup(pin_4, GPIO.OUT)
    GPIO.output(pin_4, GPIO.LOW)
