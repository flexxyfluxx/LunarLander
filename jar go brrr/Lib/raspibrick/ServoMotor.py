# ServoMotor.py
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

class ServoMotor():
    '''
    Class that represents a servo motor.
    '''
    def __init__(self, id, home, inc):
        '''
        Creates a servo motor instance and sets it at home position. For most servos:
        home = 300, inc = 2. Id 0: S12 header, 1: S13 header, 2: S14 header, 3: S15 header.
        @param id: the id of the motor (0..3)
        @param home: the PWM duty cycle for the home position (0..4095)
        @param inc: the increment factor (inc_duty/inc_position)
        '''
        self.id = id
        self.device = "svo" + str(id)
        robot = RobotInstance.getRobot()
        self.home = home
        self.inc = inc
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._partsToRegister.append(self)
        else:
            self._setup(robot)

    def _setup(self, robot):
        robot.sendCommand(self.device + ".create." + str(self.home) + "." + str(self.inc))

    def setPos(self, position):
        '''
        Sets the relative position of the servo motor.
        @param position: the position with respect to home and using the inc_duty/inc_position factor
        For most servo motors in range -200 .. 200
        '''
        self._checkRobot()
        RobotInstance.getRobot().sendCommand(self.device + ".setPos" + "." + str(position))

    def setPosAbs(self, position):
        '''
        Sets the absolute position of the servo motor.
        @param position: the position in arbitrary units in range 0..4095 (determines PWM duty cycle)
        For most servo motors in range 100..500
        '''
        self._checkRobot()
        RobotInstance.getRobot().sendCommand(self.device + ".setPosAbs" + "." + str(position))

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")
