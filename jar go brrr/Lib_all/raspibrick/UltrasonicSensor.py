# UltrasonicSensor.py
# Remote mode

from RobotInstance import RobotInstance
from Tools import Tools

class UltrasonicSensor():
    '''
    Class that represents an ultrasonic sensor.
    '''

    def __init__(self, **kwargs):
        '''
        Creates a ultrasonic sensor.
        '''
        self.device = "uss"
        self.sensorState = "FAR"
        self.sensorType = "UltrasonicSensor"
        self.triggerLevel = 20.0
        self.nearCallback = None
        self.farCallback = None
        for key in kwargs:
            if key == "near":
                self.nearCallback = kwargs[key]
            elif key == "far":
                self.farCallback = kwargs[key]
        robot = RobotInstance.getRobot()
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._partsToRegister.append(self)
        else:
            self._setup(robot)

    def _setup(self, robot):
        robot.sendCommand("uss.create")
        if self.nearCallback != None or self.farCallback != None:
            robot.registerSensor(self)

    def getValue(self):
        '''
        Returns the current distance (in cm).
        @rtype: float
        '''
        self._checkRobot()
        return float(RobotInstance.getRobot().sendCommand(self.device + ".getValue"))

    def getTriggerLevel(self):
        return self.triggerLevel

    def setTriggerLevel(self, level):
        self.triggerLevel = level

    def getSensorState(self):
        return self.sensorState

    def setSensorState(self, state):
        self.sensorState = state

    def getSensorType(self):
        return self.sensorType

    def onNear(self, v):
        if self.nearCallback != None:
            self.nearCallback(v)

    def onFar(self, v):
        if self.farCallback != None:
            self.farCallback(v)

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")

        
