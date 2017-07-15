# This file contains the code for the TKinter GUI
# as well as the methods that it implements.

#import bookkeeping info
from bookkeeping_lasync import *

# Opens a file with the current time as its name
def opener():
    global f
    try:
        fileName = dirlabel["text"] + "/" + str(datetime.datetime.now()).replace(":","_") + '.txt'
        f = open(fileName,'w')
        print "file opened: " + fileName
    except IOError:
        print "Directory does not exist"

# use to safely write to f as long as it has been instantiated
# dont think I ended up using it in my code though
def write(s):
    global f
    f.write(s)

# This will make up the bulk of the procedure.
# This method will be run after the system has been armed and will
# do the following things...
# 1)continuously check to see if either of the laser beams have broken.
# 2)if either of the beams have been broken, it will send out the signal
#   to start the PIV machine, record the time at which the beam was broken,
#   and provide an output to the user to show the motion was detected.
# 3)on each log statement, this method will keep track of where the lowst
#   pistons are.
# 4)Once the PIV system has been triggered, this program will take note of
#   each laser pulse and record the time of each event.
# PARAMETERS - three photodiodes to detect the lasers (d1,d2,do)
# out: sends the signal to PIV machine
# lowst: gets data from the lowst
def laserLoop(i1, i2, i3, out):
    while 1:
        try:
            laser1 =  GPIO.input(i1)
            laser2 =  GPIO.input(i2)
            if laser1:
                las1["bg"] = "red"
            else:
                las1["bg"] = "white"
            if laser2:
                las2["bg"] = "red"
            else:
                las2["bg"] = "white"

            #print str(init) + "\n"
            if y["bg"] == "yellow":
                #print "inside init\n"
                if las1["text"] == "lock" and laser1 == 0:
                    GPIO.output(out, True)
                    r["bg"] = "red"
                    motiondetected = datetime.datetime.now()
                elif las2["text"] == "lock" and laser2 == 0:
                    GPIO.output(out, True)
                    r["bg"] = "red"
                    motiondetected = datetime.datetime.now()
                else:
                    GPIO.output(out, False)
                lowstPos = GPIO.input(lowst)
                PIVLaser = GPIO.input(i3)
                if PIVLaser:
                    b["bg"] = "blue"
                else:
                    b["bg"] = "white"
                now = datetime.datetime.now()
                f.write(str(now) + " " + str(lowstPos) + " " + str(laser1) + " " + str(laser2) + " " + str(PIVLaser) + "\n")
            win.update()
        except RuntimeError:
            print "breaking out of loop"
            break

# this is the arming Metod.
# Procedure: When arm button is pressed, check to see if a laser is alligned.
# If it is, lock that laser.  If it isnt, print an error message.
def arm():
    print "Arm Button Pressed\n"
    isArmed = 0
    if  las1["bg"] == "red":
        las1["text"] = 'lock'
        isArmed = 1
    if las2["bg"] == "red":
        las2["text"] = 'lock'
        isArmed = 1
    if isArmed:
        g["bg"] = "green"
        armtime = datetime.datetime.now()
        print "\nSystem Armed!\n\n Press 'START' when ready to begin...\n\n"
    else:
        tkMessageBox.showinfo("Laser Error", "Make sure that your lasers are alligned properly.")
        g["bg"] = "white"

# This executes when the user presses the start button or the stop buttton.
# It records the start time of the experiment, initiates the main procedure
# and then changes the button to a stop button to wait for the user to stop
# the experiment.
def startstop():
    if startButton["text"] == "START":
        print "Start Buttton Pressed"
        if (las1["bg"] == "red" and las1["text"] == "lock") or (las2["bg"] == "red" and las2["text"] == "lock"):
            start_bookkeeping()
        else:
            if tkMessageBox.askyesno("Start", "Do you want to start without armed lasers?"):
                start_bookkeeping()
            else:
                startButton["text"] = "START"
                y["bg"] = "white"
    else:
        stop_bookkeeping()

# The bookkeeping stuff necessary when user presses Start.
# To be used in the startstop() method.
def start_bookkeeping():
    opener()
    write("Data Format: 'time stamp' 'Lowst Pos(on=1,off=0)' 'laser1(on=1,off=0)' 'laser2(on=1,off=0)' 'PIV laser(on=1,off=0)'\n\n")
    y["bg"] = "yellow"
    starttime = datetime.datetime.now()
    print("Experiment Started!")
    f.write(str(starttime) + " Experiment Started\n\n")
    startButton["text"] = "STOP"

# The bookkeeping stuff necessary when user presses Stop.
# To be used in the startstop() method.
def stop_bookkeeping():
    print "Stop Button Pressed"
    stoptime = datetime.datetime.now()
    startButton["text"] = "START"
    f.close()
    y["bg"] = "white"
    g["bg"] = "white"
    b["bg"] = "white"
    r["bg"] = "white"
    las1["text"] = ""
    las2["text"] = ""

#The method used to get the directory the user wants to save their files in
def getdir():
    print "Browse Button Pressed"
    prevdir = dirlabel["text"]
    curdir = str(tkFileDialog.askdirectory())
    if curdir == "()" or curdir == "":
        curdir = prevdir
    dirlabel["text"] = curdir
    

# This method is called when the user presses the exit button
# and it calls the various cleanup methods 
def exitProgram():
    print("Exit Button Pressed")
    GPIO.cleanup()

def on_closing():
    if tkMessageBox.askyesno("Quit", "Do you want to quit?"):
        print("Exit Button Pressed")
        #I left this bug on purpose so i would remember it
        #remember also to delete exit button
        try:
            f.close()
            print "Closing File..."
        except NameError:
            print "No file open on closing."
        GPIO.cleanup()


#----------------------------------------------------------------------------------
# Here is where I set up the widgets for TKinter GUI.  I instantiate each button and
# then use the place method to place it with respect to the parent win

#Set up the GUI
win = Tk()

myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')
f2 = tkFont.Font(family = 'Helvetica', size = 16, weight = 'bold')
f3 = tkFont.Font(family = 'Helvetica', size = 14)

win.title("LAsync")
win.geometry('800x480')

exitButton = Button(win, text = "Exit", font = myFont, command = exitProgram)
exitButton.place(anchor = "s", relwidth= .3, relheight = .152, relx = .5, rely = .96)
exitButton.config(highlightbackground="green")

las1 = Label(win, bg = "white")
las1.place(anchor = "nw", relwidth= .152, relheight = .152, relx = .148, rely = .04)

armButton = Button(win, text = "Arm", font = myFont, command = arm)
armButton.place(anchor = "n", relwidth= .3, relheight = .152, relx = .5, rely = .04)

las2 = Label(win, bg = "white")
las2.place(anchor = "nw", relwidth= .152, relheight = .152, relx = .7, rely = .04)

g = Label(win, bg = "white")
g.place(anchor = "nw", relwidth= .3, relheight = .152, relx = .025, rely = .424)

y = Label(win, bg = "white")
y.place(anchor = "nw", relwidth= .3, relheight = .152, relx = .35, rely = .424)

r = Label(win, bg = "white")
r.place(anchor = "nw", relwidth= .3, relheight = .152, relx = .675, rely = .424)

b = Label(win, bg = "white")
b.place(anchor = "n", relwidth= .3, relheight = .152, relx = .5, rely = .616)

startButton = Button(win, text = "START", font = myFont, command = startstop)
startButton.place(anchor = "nw", relwidth= .3, relheight = .152, relx = .025, rely = .232)

dirlabel = Label(win, text = initialdir, font = f3, wraplength = 200)
dirlabel.place(anchor = "nw", relwidth= .3, relheight = .152, relx = .35, rely = .232)

browseButton = Button(win, text = "Browse", font = myFont, command = getdir)
browseButton.place(anchor = "nw", relwidth= .3, relheight = .152, relx = .675, rely = .232)

# This marks the end of setting up the GUI
#------------------------------------------------------------------------------------------

