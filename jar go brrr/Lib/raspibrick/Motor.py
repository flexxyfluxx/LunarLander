# Motor.py
# Remote mode

'''
 This software is part of the raspibrick module.
 It is Open Source Free Software, so you may
 - run the code for any purpose
 - study how the code works and adapt it to your needs
 - integrate all or parts of the code in your own programs
 - redistribute copies of the code
 - improve the code and release your improvements to the public
 However the use of the code is entirely your responsibility.
 '''

from Tools import Tools
import SharedConstants
from RobotInstance import RobotInstance

# ------------------------   Class MotorState  ----------------------------------------------
class MotorState():
    FORWARD = 0
    BACKWARD = 1
    STOPPED = 2
    UNDEFINED = 3

# ------------------------   Class Motor  ---------------------------------------------------
class Motor():
    '''
    Class that represents a motor.
    '''
    def __init__(self, id):
        '''
        Creates a motor instance with given id.
        @param id: 0 for left motor, 1 for right motor
        '''
        self.state = MotorState.UNDEFINED
        self.id = id
        self.device = "mot" + str(id)
        self.speed = SharedConstants.MOTOR_DEFAULT_SPEED
        robot = RobotInstance.getRobot()
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._partsToRegister.append(self)
        else:
            self._setup(robot)

    def _setup(self, robot):
        robot.sendCommand(self.device + ".create")
        robot.sendCommand(self.device + ".setSpeed." + str(self.speed))
        self.robot = robot

    def forward(self):
        '''
        Starts the forward rotation with preset speed.
        The method returns immediately, while the rotation continues.
          '''
        self._checkRobot()
        if self.state == MotorState.FORWARD:
            return
        self.robot.sendCommand(self.device + ".forward")
        self.state = MotorState.FORWARD

    def backward(self):
        '''
        Starts the backward rotation with preset speed.
        The method returns immediately, while the rotation continues.
        '''
        self._checkRobot()
        if self.state == MotorState.BACKWARD:
            return
        self.robot.sendCommand(self.device + ".backward")
        self.state = MotorState.BACKWARD

    def stop(self):
        '''
        Stops the motor.
        (If motor is already stopped, returns immediately.)
        '''
        self._checkRobot()
        if self.state == MotorState.STOPPED:
            return
        self.robot.sendCommand(self.device + ".stop")
        self.state = MotorState.STOPPED

    def setSpeed(self, speed):
        '''
        Sets the speed to the given value (arbitrary units).
        The speed will be changed to the new value at the next movement call only.
        The speed is limited to 0..100.
        @param speed: the new speed 0..100
        '''
    def setSpeed(self, speed):
        self._checkRobot()
        speed = int(speed)
        if self.speed == speed:
            return
        self.speed = speed
        self.robot.sendCommand(self.device + ".setSpeed." + str(speed))
        self.state = MotorState.UNDEFINED

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")


