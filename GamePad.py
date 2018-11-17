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

event = in_file.read(EVENT_SIZE)

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
        37  : uinput.BTN_X,
        24  : uinput.BTN_Y,
        4   : uinput.BTN_TL,
        10  : uinput.BTN_TR,
        36  : uinput.BTN_START,
        33  : uinput.BTN_SELECT
    }

prevcode = -1
prevval = -1
with uinput.Device(events) as device:
    print "-----------------------------"
    print "|       Virtual GamePad     |"
    print "|           KEYMAP          |"
    print "-----------------------------"
    print "| W/UP ARROW  | D PAD UP    |"
    print "| S/DWN ARROW | D PAD DOWN  |"
    print "| A/LFT ARROW | D PAD LEFT  |"
    print "| D/RT ARROW  | D PAD RIGHT |"
    print "| L/ENTER     | A           |"
    print "| P           | B           |"
    print "| K           | X           |"
    print "| O           | Y           |"
    print "| 3           | LT          |"
    print "| 9           | RT          |"
    print "| F           | SELECT      |"
    print "| J           | START       |"
    print "-----------------------------"
    print "Running..."
    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
        if (type != 0 or code != 0 or value != 0) and (type == 1 and (prevcode != code or prevval != value)):
            x = value * 5
            if code == 106 or code == 32: #D-PAD Right
                device.emit(uinput.ABS_X, +x, syn=False)
                device.emit(uinput.ABS_Y, 0)
            elif code == 105 or code == 30: #D-PAD Left
                device.emit(uinput.ABS_X, -x, syn=False)
                device.emit(uinput.ABS_Y, 0)
            elif code == 103 or code == 17: #D-PAD Up
                device.emit(uinput.ABS_Y, -x, syn=False)
                device.emit(uinput.ABS_X, 0)
            elif code == 108 or code == 31: #D-PAD Down
                device.emit(uinput.ABS_Y, +x, syn=False)
                device.emit(uinput.ABS_X, 0)
            elif(code in buttons):
                if value == 2 or value == 0:
                    device.emit(buttons[code],int(value/2))
                else:
                    device.emit_click(buttons[code])
            prevcode = code
            prevval = value
    
        event = in_file.read(EVENT_SIZE)

in_file.close()
