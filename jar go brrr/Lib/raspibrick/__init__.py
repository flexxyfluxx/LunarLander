# __init__.py

import raspibrick.SharedConstants
from raspibrick.Robot import Robot
from raspibrick.UltrasonicSensor import UltrasonicSensor
from raspibrick.Display import Display
from raspibrick.Gear import Gear
from raspibrick.Motor import Motor
from raspibrick.ServoMotor import ServoMotor
from raspibrick.Beeper import Beeper
from raspibrick.Led import Led
from raspibrick.InfraredSensor import InfraredSensor
from raspibrick.Camera import Camera
from raspibrick.LightSensor import LightSensor
from raspibrick.OLED1306 import OLED1306
from raspibrick.Tools import *
from raspibrick.RobotInstance import RobotInstance
from raspibrick.RobotContext import RobotContext
from raspibrick.Obstacle import Obstacle
from raspibrick.Target import Target
from raspibrick.Torch import Torch
from raspibrick.Shadow import Shadow

# globals
MOTOR_LEFT = SharedConstants.MOTOR_LEFT
MOTOR_RIGHT = SharedConstants.MOTOR_RIGHT
IR_CENTER = SharedConstants.IR_CENTER
IR_LEFT = SharedConstants.IR_LEFT
IR_RIGHT = SharedConstants.IR_RIGHT
IR_LINE_LEFT = SharedConstants.IR_LINE_LEFT
IR_LINE_RIGHT = SharedConstants.IR_LINE_RIGHT
LED_FRONT = SharedConstants.LED_FRONT
LED_LEFT = SharedConstants.LED_LEFT
LED_REAR = SharedConstants.LED_REAR
LED_RIGHT = SharedConstants.LED_RIGHT
LS_FRONT_LEFT = SharedConstants.LS_FRONT_LEFT
LS_FRONT_RIGHT = SharedConstants.LS_FRONT_RIGHT
LS_REAR_LEFT = SharedConstants.LS_REAR_LEFT
LS_REAR_RIGHT = SharedConstants.LS_REAR_RIGHT


def getKey():
    '''
    Waits for a key stroke.
    A key stroke may generate 1, 2, 3 or 4 characters,
    e.g. cursor up: x,y,z with ord(x) = 27, ord(y) = 91, ord(z) = 65
    @return: one character (string) of key sequence
    '''
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ord(ch) == 0x03:  # Ctrl-C
        raise KeyboardInterrupt
    return ch

def readKey():
    '''
    Single character input. Read cursor keys.
    @return: one character (string) for normal keys, special value for cursor keys:
     # 16:Up, 17:Down, 18:Right, 19:Left
    '''
    ch1 = getKey()
    if ord(ch1) == 126:  # ~ used for special key, ignore
        return readKey()
    if ord(ch1) != 0x1B:  # not special key
        return ch1
    ch2 = getKey()
    if ord(ch2) != 0x5B:  # not [
        return ch1
    ch3 = getKey()
    if ord(ch3) != 0x31:
        print "third", ord(ch3)
        return chr(0x10 + ord(ch3) - 65)


def _doExit():
    robot = RobotInstance.getRobot()
    if robot != None:
        robot.exit()
    
registerExitFunction(_doExit)
registerStopFunction(_doExit)

def isButtonHit():
    robot = RobotInstance.getRobot()
    if robot != None:
       return robot.isButtonHit()
    return False

def isEnterHit():
    robot = RobotInstance.getRobot()
    if robot != None:
       return robot.isEnterHit()
    return False

def isEscapeHit():
    robot = RobotInstance.getRobot()
    if robot != None:
       return robot.isEscapeHit()
    return False

def isUpHit():
    robot = RobotInstance.getRobot()
    if robot != None:
       return robot.isUpHit()
    return False

def isDownHit():
    robot = RobotInstance.getRobot()
    if robot != None:
       return robot.isDownHit()
    return False

def isLeftHit():
    robot = RobotInstance.getRobot()
    if robot != None:
       return robot.isLeftHit()
    return False

def isRightHit():
    robot = RobotInstance.getRobot()
    if robot != None:
       return robot.isRightHit()
    return False
