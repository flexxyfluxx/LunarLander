# Display.py
# Remote mode
'''
The 7 segments have the following binary values
           1
           -
     32 |     |2

          64
           -
     16 |     |4
           -
           8

The decimal points use value 128 with digit 1, 2 or 3
'''

from RobotInstance import RobotInstance


# ------------------------   Class Display  -------------------------------------------
class Display():
    '''
    Abstraction of the 4 digit 7-segment display attached to the I2C port.
    If no display is found, all methods return immediately.
    '''
    def __init__(self):
        '''
        Creates a display instance either from class Display4tronix or DisplayDidel.
        Because the 4tronix display is multiplexed (one digit shown after
        the other, a display thread is used to display all 4 digits in a rapid succession.
        '''
        self.device = "display"
        robot = RobotInstance.getRobot()
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._partsToRegister.append(self)
        else:
            self._setup(robot)

    def _setup(self, robot):
        robot.sendCommand(self.device + ".create")
        self.robot = robot

    def clear(self):
        '''
        Turns all digits off. Stops a running display thread.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".clear")

    def showText(self, text, pos = 0,  dp = [0, 0, 0, 0]):
        '''
        Displays 4 characters of the given text. The text is considered to be prefixed and postfixed by spaces
        and the 4 character window is selected by the text pointer pos that determines the character displayed at the
        leftmost digit, e.g. (_: empty):
        showText("AbCdEF") -> AbCd
        showText("AbCdEF", 1) -> bCdE
        showText("AbCdEF", -1) ->_AbC
        showText("AbCdEF", 4) -> EF__
        To display a character and its decimal point, use the dp parameter [most right dp,...,most left dp] and
        set the decimal point values to 1. Because the 4tronix display is multiplexed (one digit shown after
        the other, a display thread is started now to display all 4 digits in a rapid succession
        (if it is not yet started).
        @param text: the text to display (list, tuple, string or integer)
        @param pos: the start value of the text pointer (character index positioned a leftmost digit)
        @param dp: a list with four 1 or 0, if the decimal point is shown or not
        @return: True, if successful; False, if the display is not available,
        text or dp has illegal type or one of the characters can't be displayed
        '''
        self._checkRobot()
        if not (type(text) == int or type(text) == list or type(text) == str):
            return
        if type(text) == int:
            text = str(text)
        d =  [0] * 4
        for i in range(min(4, len(dp))):
            d[i] = dp[i]

        self.robot.sendCommand(self.device + ".showText." + text + "." + str(pos) + "." + \
           str(d[0]) + ", " + str(d[1]) + ", " + str(d[2]) + ", " + str(d[3]))

    def scrollToLeft(self):
        '''
        Scrolls the scrollable text one step to the left.
        @return: the number of characters remaining at the right
        '''
        self._checkRobot()
        return int(self.robot.sendCommand(self.device + ".scrollToLeft"))

    def scrollToRight(self):
        '''
        Scrolls the scrollable text one step to the left.
        @return: the number of characters remaining at the left
        '''
        self._checkRobot()
        return int(self.robot.sendCommand(self.device + ".scrollToRight"))

    def setToStart(self):
        '''
        Shows the scrollable text at the start position.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".setToStart")

    def showTicker(self, text, count = 1, speed = 2, blocking = False):
        '''
        Shows a ticker text that scroll to left until the last 4 characters are displayed.
        @param text: the text to display, if short than 4 characters, scrolling is disabled
        @param count: the number of repetitions (default: 1). For count == 0, infinite duration,
        stopped by calling stopTicker()
        @param speed: the speed number of scrolling operations per sec (default: 2)
        @param blocking: if True, the method blocks until the ticker has finished; otherwise
         it returns immediately (default: False)
        '''
        self._checkRobot()
        if blocking:
            param = "1"
        else:
            param = "0"
        self.robot.sendCommand(self.device + ".showTicker." + text + "." + \
                    str(count) + "." + str(speed) + "." + param)

    def stopTicker(self):
        '''
        Stops a running ticker.
        The method blocks until the ticker thread is finished and isTickerAlive() returns False.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".stopTicker")

    def isTickerAlive(self):
        '''
        @return: True, if the ticker is displaying; otherwise False
        '''
        self._checkRobot()
        rc = self.robot.sendCommand(self.device + ".isTickerAlive")
        if rc == "0":
            return False
        return True

    def showBlinker(self, text, dp = [0, 0, 0, 0], count = 3, speed = 1, blocking = False):
        '''
        Shows a blinking text for the given number of times and blinking speed.
        @param text: the text to display, if short than 4 characters, scrolling is disabled
        @param count: the number of repetitions (default: 3). For count = 0, infinite duration,
        may be stopped by calling stopBlinker().
        @param speed: the speed number of blinking operations per sec (default: 1)
        @param blocking: if True, the method blocks until the blinker has finished; otherwise
        it returns immediately (default: False)
        '''
        self._checkRobot()
        d =  [0] * 4
        for i in range(min(4, len(dp))):
            d[i] = dp[i]
        if blocking:
            param = "1"
        else:
            param = "0"
        self.robot.sendCommand(self.device + ".showBlinker." + text + "." + \
                str(d[0]) + ", " + str(d[1]) + ", " + str(d[2]) + ", " + str(d[3]) +  "."  + \
                str(count) + "." + str(speed) + "." + param)

    def stopBlinker(self):
        '''
        Stops a running blinker.
        The method blocks until the blinker thread is finished and isBlinkerAlive() returns False.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".stopBlinker")

    def isBlinkerAlive(self):
        '''
        @return: True, if the blinker is displaying; otherwise False
        '''
        self._checkRobot()
        rc = self.robot.sendCommand(self.device + ".isBlinkerAlive")
        if rc == "0":
            return False
        return True

    def isAvailable(self):
        '''
        @return: True, if the display is detetectd on the I2C interface; otherwise False
        '''
        self._checkRobot()
        rc = self.robot.sendCommand(self.device + ".isAvailable")
        if rc == "0":
            return False
        return True

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")
