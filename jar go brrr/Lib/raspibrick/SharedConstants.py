# SharedConstants.py
# Remote mode

'''
Constants and defaults for the RaspiBrick libray based on Pi2Go (full version) from 4tronix.

 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
'''


'''
History:

V1.00 - Oct 2015: - First public release
V1.01 - Oct 2015: - Added: Button long press event
V1.02 - Dec 2015: - Modified: methods of class Display
'''


# Be careful: Too many debugging messages may influence running behavior
DEBUG = False

PORT = 1299

# Motor IDs
MOTOR_LEFT = 0
MOTOR_RIGHT = 1

# Infrared IDs
IR_CENTER = 0
IR_LEFT = 1
IR_RIGHT = 2
IR_LINE_LEFT = 3
IR_LINE_RIGHT = 4

# LED IDs
LED_FRONT = 0
LED_LEFT = 1
LED_REAR = 2
LED_RIGHT = 3

# Light sensor IDs
LS_FRONT_LEFT = 0
LS_FRONT_RIGHT = 1
LS_REAR_LEFT = 2
LS_REAR_RIGHT = 3

# Default speeds
MOTOR_DEFAULT_SPEED = 40
GEAR_DEFAULT_SPEED = 30

# Button event constants
BUTTON_PRESSED = 1
BUTTON_RELEASED = 2
BUTTON_LONGPRESSED = 3

# Event poll delay (ms)
POLL_DELAY = 50

ABOUT = "2003-2015 Aegidius Pluess\n" + \
         "OpenSource Free Software\n" + \
         "http://www.aplu.ch\n" + \
         "All rights reserved"
VERSION = "1.01 - Oct 2015"

