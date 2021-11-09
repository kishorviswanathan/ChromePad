#!/usr/bin/env python3
import struct
import uinput
from subprocess import Popen, PIPE

kbd = Popen(
    "grep -E  'Handlers|EV=' /proc/bus/input/devices | grep -B1 'EV=120013' | grep -Eo 'event[0-9]+'",
    shell=True,
    stdout=PIPE,
    encoding='utf8'
).stdout.read().replace("\n", "")

infile_path = "/dev/input/" + kbd

# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

# open file in binary mode
in_file = open(infile_path, "rb")

events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_TL,
    uinput.BTN_TR,
    uinput.ABS_X + (-1, 1, 0, 0),
    uinput.ABS_Y + (-1, 1, 0, 0),
    uinput.ABS_Z + (-1, 1, 0, 0),
    uinput.ABS_RZ + (-1, 1, 0, 0),
)

buttons = {
    38: uinput.BTN_A,
    28: uinput.BTN_A,
    25: uinput.BTN_B,
    1: uinput.BTN_B,

    37: uinput.BTN_X,
    24: uinput.BTN_Y,

    4: uinput.BTN_TL,
    10: uinput.BTN_TR,
}
axes0 = {
    32: [1, 0],     # Right
    30: [-1, 0],    # Left
    17: [0, -1],    # Up
    31: [0, 1],     # Down
}

axes1 = {
    106: [1, 0],    # Right
    105: [-1, 0],   # Left
    103: [0, -1],   # Up
    108: [0, 1],    # Down
}

print("+---------------------------+")
print("|         ChromePad         |")
print("|           KEYMAP          |")
print("+---------------------------+")
print("| W           | L STICK UP  |")
print("| S           | L STICK DWN |")
print("| A           | L STICK LFT |")
print("| D           | L STICK RHT |")
print("| UP ARROW    | R STICK UP  |")
print("| DWN ARROW   | R STICK DWN |")
print("| LFT ARROW   | R STICK LFT |")
print("| RT ARROW    | R STICK DWN |")
print("| L/ENTER     | A           |")
print("| P/ESC       | B           |")
print("| K           | X           |")
print("| O           | Y           |")
print("| 3           | LT          |")
print("| 9           | RT          |")
print("+---------------------------+")

prevcode = -1
prevval = -1
with uinput.Device(events) as device:
    print("ChromePad Started. Start playing !!")
    event = in_file.read(EVENT_SIZE)
    while event:
        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
        if (type != 0 or code != 0 or value != 0) and (type == 1 and (prevcode != code or prevval != value) and value != 2):
            if (code in axes0):
                x, y = axes0[code]
                if y == 0:
                    device.emit(uinput.ABS_X, x * value)
                else:
                    device.emit(uinput.ABS_Y, y * value)
            elif (code in axes1):
                x, y = axes1[code]
                if y == 0:
                    device.emit(uinput.ABS_Z, x * value)
                else:
                    device.emit(uinput.ABS_RZ, y * value)
            elif(code in buttons):
                device.emit(buttons[code], value)
            prevcode = code
            prevval = value
        try:
            event = in_file.read(EVENT_SIZE)
        except:
            print("\nExiting ChromePad...")
            exit()

in_file.close()
