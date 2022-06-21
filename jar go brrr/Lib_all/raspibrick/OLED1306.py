# OLED1306.py
# Remote mode

'''
 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code777
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
 '''

from RobotInstance import RobotInstance
from Tools import Tools
import time

class OLED1306():
    '''
    Class that represents a OLED display.
    '''
    def __init__(self):
        '''
        Creates a OLED instance for the SSD1306 based chip.
        '''
        self._checkRobot()
        self.device = "oled"
        self.robot = RobotInstance.getRobot()
        self.robot.sendCommand(self.device + ".create")

    def println(self, text):
        '''
        Shows the given text with automatic line scrolling.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".println.'" + text + "'")

    def setFontSize(self, fontSize):
        '''
        Sets a new font size of current font.
        @fontSize: the new font size
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".setFontSize." + str(fontSize))


    def clear(self):
        '''
        Erases the display and clears the text buffer.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".clear")

    def setText(self, text, lineNum = 0, fontSize = None, indent = 0):
        '''
        Displays text at given line left adjusted.
        The old text of this line is erased, other text is not modified
        The line distance is defined by the font size (text height + 1).
        If no text is attributed to a line, the line is considered to consist of a single space
        character with the font size of the preceeding line.
        The position of the text cursor is not modified.
        Text separated by \n is considered as a  multiline text. In this case lineNum is the line number of the
        first line.
        @param text: the text to display. If emtpy, text with a single space character is assumed.
        @param lineNum: the line number where to display the text (default: 0)
        @param fontSize: the size of the font (default: None, set to current font size)
        @indent: the line indent in pixels (default: 0)
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".setText.'" + text + "'." +
                  str(lineNum) + "." + str(fontSize) + "." + str(indent))

       
    def startBlinker(self, count = 3, offTime = 1000, onTime = 1000, blocking = False):
        '''
        Blicks the entire screen for given number of times (off-on periods). 
        @param count: the number of blinking (default: 3)
        @param offTime: the time the display is erased (in ms, default: 1000)
        @param onTime: the time the display is shown (in ms, default: 1000)
        @param blocking: if True, the function blocks until the blinking is finished; otherwise
        it returns immediately
        '''
        self._checkRobot()
        blockingStr = '1' if blocking else "0"
        self.robot.sendCommand(self.device + ".startBlinker." +
                  str(count) + "." + str(offTime) + "." + str(onTime) +  
                  "." + blockingStr)
                             
    def stopBlinker(self):
        '''
        Stops a running blinker.
        The method blocks until the blinker thread is finished and isBlinkerAlive() returns False.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".stopBlinker")

    def isBlinking(self):
        '''
        @return: True, if the blinker is displaying; otherwise False
        '''
        time.sleep(0.001)
        rc = self.robot.sendCommand(self.device + ".isBlinking")
        v = True if rc == "True" else False
        return v

    def setInverse(self, inverse):
        '''
        @param inverse: if True, the background is white and the text is black; 
        otherwise the background is black and the text  is white (default)
        '''
        self._checkRobot()
        inverseStr = "1" if inverse else "0"
        self.robot.sendCommand(self.device + ".setInverse." + inverseStr)


    
    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")
