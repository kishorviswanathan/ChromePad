#!/usr/local/bin/python
import struct
import time
import sys
import uinput
import subprocess

kbd = subprocess.Popen("grep -E  'Handlers|EV=' /proc/bus/input/devices | grep -B1 'EV=120013' | grep -Eo 'event[0-9]+'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read().replace("\n","")

infile_path = "/dev/input/" + kbd

#long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

#open file in binary mode
in_file = open(infile_path, "rb")

events = (
        uinput.BTN_A,
        uinput.BTN_B,
        uinput.BTN_X,
        uinput.BTN_Y,
        uinput.BTN_TL,
        uinput.BTN_TR,
        uinput.BTN_SELECT,
        uinput.BTN_START,
        uinput.ABS_X + (-5, 5, 0, 0),
        uinput.ABS_Y + (-5, 5, 0, 0)
        )
        
buttons = {
        38  : uinput.BTN_A,
        28  : uinput.BTN_A,
        25  : uinput.BTN_B,
        1   : uinput.BTN_B,
        37  : uinput.BTN_X,
        24  : uinput.BTN_Y,
        4   : uinput.BTN_TL,
        10  : uinput.BTN_TR,
        36  : uinput.BTN_START,
        33  : uinput.BTN_SELECT
    }
axes = {
        106 : [+5,0], #D-PAD Right
        32  : [+5,0],
        105 : [-5,0], #D-PAD Left
        30  : [-5,0],
        103 : [0,-5], #D-PAD Up
        17  : [0,-5],
        108 : [0,+5], #D-PAD Down
        31  : [0,+5],
}

print "+---------------------------+"
print "|         ChromePad         |"
print "|           KEYMAP          |"
print "+---------------------------+"
print "| W/UP ARROW  | D PAD UP    |"
print "| S/DWN ARROW | D PAD DOWN  |"
print "| A/LFT ARROW | D PAD LEFT  |"
print "| D/RT ARROW  | D PAD RIGHT |"
print "| L/ENTER     | A           |"
print "| P/ESC       | B           |"
print "| K           | X           |"
print "| O           | Y           |"
print "| 3           | LT          |"
print "| 9           | RT          |"
print "| F           | SELECT      |"
print "| J           | START       |"
print "+---------------------------+"

prevcode = -1
prevval = -1
with uinput.Device(events) as device:
    print "ChromePad Started. Start playing !!"
    event = in_file.read(EVENT_SIZE)
    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
        if (type != 0 or code != 0 or value != 0) and (type == 1 and (prevcode != code or prevval != value)):
            if (code in axes):
                device.emit(uinput.ABS_X, axes[code][0] * value, syn=False)
                device.emit(uinput.ABS_Y, axes[code][1] * value)
            elif(code in buttons):
                if value == 2 or value == 0:
                    device.emit(buttons[code],int(value/2))
                else:
                    device.emit_click(buttons[code])
            prevcode = code
            prevval = value
        try:
                event = in_file.read(EVENT_SIZE)
        except:
                print "\nExiting ChromePad..."
                exit()

in_file.close()
