# This file contains various bookkeeping info for lasync
# 1. import packages
# 2. the numbers of hardware GPIO pins
# 3. useful variables

#import statements
import RPi.GPIO as GPIO
from time import sleep
import datetime
import tkMessageBox
import tkFont
from Tkinter import *
import tkFileDialog

#set the GPIO pin configuration to be BOARD
GPIO.setmode(GPIO.BOARD)

# These are the Pins that the photodiode circuits will be 
# attached to in order to detect if a laser is being shined
# on them or not
# One thing to note is that you can vary the "sensititvity" of the
# photodiode circuit by puting a different size resistor in series with it.
# The higher the resistance, the lower light intensity needs to be shined on
# the diode in order for it to be considered on.
d1 = 11
d2 = 13
overhead = 15

# Pin for output to PIV
piv = 32

# Pin for input of info from the LOWST
lowst = 16

# Setup all the output pins
GPIO.setup(piv, GPIO.OUT)

# Setup all the input pins. I use pull up resistors for safety.
GPIO.setup(d1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(d2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(overhead, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(lowst, GPIO.IN, pull_up_down = GPIO.PUD_UP)

#useful variables
armtime = datetime.datetime.now()
starttime = datetime.datetime.now()
endtime = datetime.datetime.now()
motiondetected = datetime.datetime.now()
initialdir = '/home/pi/Desktop/lasync/outputs'
global f
