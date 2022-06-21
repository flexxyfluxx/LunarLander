# Camera.py
# Remote mode

from RobotInstance import RobotInstance

class Camera():
    '''
    Class that represents the Raspberry Pi camera.
    '''

    def __init__(self):
        '''
        Creates an instance of a camera.
        '''
        self.device = "cam"
        robot = RobotInstance.getRobot()
        if robot == None:  # deferred registering, because Robot not yet created
            RobotInstance._partsToRegister.append(self)
        else:
            self._setup(robot)

    def _setup(self, robot):
        robot.sendCommand(self.device + ".create")
        self.robot = robot

    def captureAndSave(self, width, height, filename):
        '''
        Takes a camera picture with given picture size and stores is
        in JPEG format on the remote device.
        The picture resolution is width x height (max: 5 MPix)
        @param width: the width of the picture in pixels (max: 2592)
        @param height: the height of the picture in pixels (max: 1944)
        @param filename: a valid filename in the remote file space, e.g. /home/pi/shot1.jpg
        '''
        self._checkRobot()
        filename = filename.replace(".", "`") # . is used as command separator
        self.robot.sendCommand(self.device + ".captureAndSave."
                               + str(width) + "." + str(height) + "." + filename)

    def captureAndTransfer(self, width, height):
        '''
        Performs a camera capture with given resolution width x height in pixels.
        The camera picture is hold in memory on the remote device and transferred in JPEG format
        to the local device.
        @return: Binary data holding the jpeg formated image (as string).
        @rtype: str
        '''
        self._checkRobot()
        self.robot.isBinaryReply = True
        return self.robot.sendCommand(self.device + ".captureJPEG." + str(width) + "." + str(height))

    def saveData(self, data, filename):
        '''
        Writes the given string data into a binary file.
        @param data: the image data (as string) to store
        @param filename: a valid filename in the local file space
        '''
        file = open(filename, "wb")
        file.write(data)
        file.close()

    def _checkRobot(self):
        if RobotInstance.getRobot() == None:
            raise Exception("Create Robot instance first")

        
