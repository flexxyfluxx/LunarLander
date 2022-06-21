# raspisim.py
# AP
# Version 1.01, April 29, 2017

from ch.aplu.raspisim import *
from java.awt import Color, Point
from enum import enum
from ch.aplu.jgamegrid import GameGrid

GameGrid.setClosingMode(GameGrid.DisposeOnClose)

MOTOR_LEFT = 0
MOTOR_RIGHT = 1

LED_FRONT = 0
LED_LEFT = 1
LED_REAR = 2
LED_RIGHT = 3

IR_CENTER = 0
IR_LEFT = 1
IR_RIGHT = 2
IR_LINE_LEFT = 3
IR_LINE_RIGHT = 4

LS_FRONT_LEFT = 0
LS_FRONT_RIGHT = 1
LS_REAR_LEFT = 2
LS_REAR_RIGHT = 3

if Robot.getGameGrid() != None:
   Robot.getGameGrid().dispose()


RobotContext().init()

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


class OLED1306():
    def __init__(self, bkImagePath = None, type = 64, inverse = False):
        pass
        
    def dim(self, enable):
       pass
        
    def setBkImage(self, bkImagePath):
       pass
         
    def setFont(self, ttfFile, fontSize = 10):
       pass

    def setFontSize(self, fontSize):
       pass

    def clear(self):
       pass
        
    def erase(self):
       pass
                    
    def setText(self, text, lineNum = 0, fontSize = None, indent = 0):
        pass

    def getFontSize(self):
        return -1
    
    def getLineHeight(self):
        return -1

    def repaint(self):
        pass

    def showImage(self, imagePath):  
        pass
        
    def println(self, text):
        pass
        
    def setNumberOfLines(self, nbLines):
        pass
        
    def setInverse(self, inverse):
        pass
        
    def startBlinker(self, count = 3, offTime = 1000, onTime = 1000, blocking = False):
        pass
                             
    def stopBlinker(self):
        pass

    def isBlinking(self):
        return False

    def isDeviceAvailable(self):
        return True  # simulated 
