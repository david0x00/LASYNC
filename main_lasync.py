# Welcome to the Laser Syncronization System (LAsync).
# This code was written by David Null in the summer 
# of 2016 for the Hydrosystems Lab.  This system will be able 
# to synchronize the timing of an experiment as well as
# be able to detect the movement of an object by recognizing
# a break in the beam of a laser.  Once motion is detected,
# a signal will be sent to the PIV system to start
# capturing images. This code can be modified to suit many
# different experiments.

#import gui
from gui_and_methods_lasync import *

#enter main procedures
win.protocol("WM_DELETE_WINDOW", on_closing)
laserLoop(d1, d2, overhead, piv)
