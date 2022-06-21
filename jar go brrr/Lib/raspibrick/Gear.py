# Gear.py
# Remote mode

from RobotInstance import RobotInstance
import SharedConstants

# ------------------------   Class GearState  ----------------------------------------------
class GearState():
    FORWARD = 0
    BACKWARD = 1
    STOPPED = 2
    LEFT = 3
    RIGHT = 4
    LEFTARC = 5
    RIGHTARC = 6
    UNDEFINED = 7

# ------------------------   Class Gear   --------------------------------------------------
class Gear():
    '''
    Class that represents the combination of two motors on an axis
    to perform a car-like movement.
    '''

    def __init__(self):
        self.state = GearState.UNDEFINED
        self.speed = SharedConstants.GEAR_DEFAULT_SPEED
        self.arcRadius = 0
        self.device = "gear"
        robot = RobotInstance.getRobot()
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._partsToRegister.append(self)
        else:
            self._setup(robot)

    def _setup(self, robot):
        robot.sendCommand(self.device + ".create")
        robot.sendCommand(self.device + ".setSpeed." + str(self.speed))
        self.robot = robot

    def setSpeed(self, speed):
        self._checkRobot()
        speed = int(speed)
        if self.speed == speed:
            return
        self.speed = speed
        self.robot.sendCommand(self.device + ".setSpeed." + str(speed))
        self.state = GearState.UNDEFINED

    def forward(self, duration = 0):
        self._checkRobot()
        if self.state == GearState.FORWARD:
            return
        if duration == 0:
            self.robot.sendCommand(self.device + ".forward")
            self.state = GearState.FORWARD
        else:
            self.robot.sendCommand(self.device + ".forward." + str(duration))
            self.state = GearState.STOPPED

    def backward(self, duration = 0):
        self._checkRobot()
        if self.state == GearState.BACKWARD:
            return
        if duration == 0:
            self.robot.sendCommand(self.device + ".backward")
            self.state = GearState.BACKWARD
        else:
            self.robot.sendCommand(self.device + ".backward." + str(duration))
            self.state = GearState.STOPPED

    def left(self, duration = 0):
        self._checkRobot()
        if self.state == GearState.LEFT:
            return
        if duration == 0:
            self.robot.sendCommand(self.device + ".left")
            self.state = GearState.LEFT
        else:
            self.robot.sendCommand(self.device + ".left." + str(duration))
            self.state = GearState.STOPPED

    def right(self, duration = 0):
        self._checkRobot()
        if self.state == GearState.RIGHT:
            return
        if duration == 0:
            self.robot.sendCommand(self.device + ".right")
            self.state = GearState.RIGHT
        else:
            self.robot.sendCommand(self.device + ".right." + str(duration))
            self.state = GearState.STOPPED

    def leftArc(self, radius, duration = 0):
        self._checkRobot()
        radius = int(1000 * radius)
        if duration == 0:
            if self.state == GearState.LEFTARC and radius == self.arcRadius:
                return
            self.arcRadius = radius
            self.robot.sendCommand(self.device + ".leftArcMilli." + str(radius))
            self.state = GearState.LEFTARC
        else:
            self.robot.sendCommand(self.device + ".leftArcMilli." + str(radius) + "." + str(duration))
            self.state = GearState.STOPPED

    def rightArc(self, radius, duration = 0):
        self._checkRobot()
        radius = int(1000 * radius)
        if duration == 0:
            if self.state == GearState.RIGHTARC and radius == self.arcRadius:
                return
            self.arcRadius = radius
            self.robot.sendCommand(self.device + ".rightArcMilli." + str(radius))
            self.state = GearState.RIGHTARC
        else:
            self.robot.sendCommand(self.device + ".rightArcMilli." + str(radius) + "." + str(duration))
            self.state = GearState.STOPPED

    def stop(self):
        self._checkRobot()
        if self.state == GearState.STOPPED:
            return
        self.robot.sendCommand(self.device + ".stop")
        self.state = GearState.STOPPED
        
    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")
