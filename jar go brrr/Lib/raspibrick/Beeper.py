# Beeper.java
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

class Beeper():
    '''
    Class that represents a beeper.
    '''
    def __init__(self, pin = 40):
        '''
        Creates a beeper instance attached to the given GPIO port.
        @param pin: the GPIO port number (default: 40)
        '''
        self._checkRobot()
        self.device = "beeper"
        self.robot = RobotInstance.getRobot()
        self.robot.sendCommand(self.device + ".create." + str(pin))

    def turnOn(self):
        '''
        Turns the beeper on.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".turnOn")

    def turnOff(self):
        '''
        Turns the beeper off.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".turnOff")

    def start(self, onTime, offTime, count = 0, blocking = False):
        '''
        Starts beeping. The beeping period is offTime + onTime. 
        May be stopped by calling stop(). If blocking is False, the
        function returns immediately while the blinking goes on. The blinking is stopped by setColor().
        @param onTime: the time in ms in on state
        @param offTime: the time in ms in off state
        @param count: total number of on states; 0 for endlessly (default)
        @param blocking: if True, the method blocks until the beeper has finished; otherwise
         it returns immediately (default: False)
        '''
        self._checkRobot()
        blockingStr = "1" if blocking else "0"
        self.robot.sendCommand(self.device + ".start." + 
           str(onTime) + "." + 
           str(offTime) + "." +
           str(count) + "." +
	   str(blockingStr))

    def stop(self):
        '''
        Stops beeping.
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".stop")

    def setOffTime(self, offTime):
        '''
        Sets the time the speaker is off.
        @param offTime: the offTime in ms
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".setOffTime." + str(offTime))

    def setOnTime(self, onTime):
        '''
        Sets the time the speaker is on.
        @param onTime: the onTime in ms
        '''
        self._checkRobot()
        self.robot.sendCommand(self.device + ".setOnTime." + str(onTime))

    def beep(self, count = 1):
        '''
        Emits a short beep the given number of times. Blocking until the beeps are played.
        @param count: the number of beeps
        '''
        self.start(60, 120, count, True)

    def isBeeping(self):
        '''
        @return: True, if the beeper is active; otherwise False
        '''
        time.sleep(0.001)
        rc = self.robot.sendCommand(self.device + ".isBeeping")
        v = True if rc == "True" else False
        return v

   

    
    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")
