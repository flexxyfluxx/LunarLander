# Robot.py
# Remote mode
# TigerJython version


import socket, sys, time
from threading import Thread, Lock
from Tools import *
from SensorThread import SensorThread
from RobotInstance import RobotInstance
from ch.aplu.raspi import *
import thread


class RaspiException(Exception):
    pass

def onClose():
    robot = RobotInstance.getRobot()
    if  robot == None:
        return
    robot.exit()

class KeyListener(ButtonKeyListener):
    def buttonPressed(self, keyCode):
        robot = RobotInstance.getRobot()
        if robot == None:
            return
        if keyCode == 27:  # ESCAPE
            robot.escapeHit = True
            if robot._buttonEvent != None:
                robot._buttonEvent(SharedConstants.BUTTON_PRESSED)
        elif keyCode == 10:    # ENTER
            robot.enterHit = True
        elif keyCode == 37:  # CURSOR_LEFT
            robot.leftHit = True
        elif keyCode == 38:  # CURSOR_UP
            robot.upHit = True
        elif keyCode == 39:  # CURSOR_RIGHT
            robot.rightHit = True
        elif keyCode == 40:   # CURSOR_DOWN
            robot.downHit = True

    def buttonReleased(self, keyCode):
        robot = RobotInstance.getRobot()
        if robot == None:
            return
        if keyCode == 27:  # ESCAPE
           if robot._buttonEvent != None:
              robot._buttonEvent(SharedConstants.BUTTON_RELEASED)

    def buttonLongPressed(self, keyCode):
        robot = RobotInstance.getRobot()
        if robot == None:
            return
        if keyCode == 27:  # ESCAPE
           if robot._buttonEvent != None:
              robot._buttonEvent(SharedConstants.BUTTON_LONGPRESSED)


# -------------------------------- global constants -------------------------
receiverTimeout = 10

# -------------------------------- class Response ---------------------------
class Response():
    OK = "0"
    SEND_FAILED = "-1"
    ILLEGAL_METHOD = "-2"
    ILLEGAL_INSTANCE = "-3"
    CMD_ERROR = "-4"
    ILLEGAL_PORT = "-5"
    CREATION_FAILED = "-6"

# -------------------------------- class Receiver ---------------------------
class Receiver(Thread):
    def __init__(self, robot):
        Thread.__init__(self)
        self.robot = robot
                  
    def run(self):
        Tools.debug("Receiver thread started")
        while self.robot.isReceiverRunning:
            try:
                self.robot.isReceiverUp = True
                self.robot.receiverResponse = self.readResponse()
            except:    
                Tools.debug("Exception in Receiver.run()")
                self.robot.isReceiverRunning = False
                self.robot.closeConnection()
        Tools.debug("Receiver thread terminated")

    def readResponse(self):
        Tools.debug("Calling readResponse")
        bufSize = 4096
        data = ""
        while (not self.robot.isBinaryReply and not "\n" == data[-1:]) or \
            (self.robot.isBinaryReply and not "\xff\xd9\n" in data[-3:]):
            # eof tag for jpeg files and the added \n,
            # we are not sure 100% that this sequence is never embedded in image
                # but it is very improbable to fit the last three bytes of the 4096 size block
            try:
                reply = self.robot.sock.recv(bufSize)
            except:
                raise Exception("Exception from blocking sock.recv()")
            data += reply
        if not self.robot.isBinaryReply:
           data = data.decode("UTF-8")
           data = data[:-1]  # Remove trailing \n
        self.robot.isBinaryReply = False
        return data

# ------------------------   Class Robot   -------------------------------------------------
class Robot(object):
    '''
    Class that creates or returns a single MyRobot instance.
    '''
    def __new__(cls, ipAddress = "", buttonEvent = None):
        if RobotInstance.getRobot() == None:
            r = MyRobot(ipAddress, buttonEvent)
            RobotInstance.setRobot(r)
            for parts in RobotInstance._partsToRegister:
                parts._setup(r)
            return r
        else:
            return RobotInstance.getRobot()

# -------------------------------- class Robot --------------------------
class MyRobot():
    _myInstance = None
    def __init__(self, ipAddress = "", buttonEvent  = None):
        if MyRobot._myInstance != None:
            raise Exception("Only one instance of MyRobot allowed")

        self.panel = ConnectPanel.create()
        if ipAddress == "":
            ipAddress_port = self.panel.askIPAddress()
            if ipAddress_port == "":
                raise RaspiException("No IP address given.")
        else:
            ipAddress_port = ipAddress
        ipList = ipAddress_port.split(":")
        self.ipAddress = ipList[0]
        if len(ipList) == 2:
            self.port = int(ipList[1])
        else:
            self.port = SharedConstants.PORT
        self.isBinaryReply = False
        self.isReceiverUp = False
        self.isReceiverRunning = False
        self.isExited = False
        self.buttonHit = False
        self.escapeHit = False
        self.enterHit = False
        self.upHit = False
        self.downHit = False
        self.leftHit = False
        self.rightHit = False
        self.sensorThread = None
        self._buttonEvent = buttonEvent
        self.isConn = False
        self.lock = Lock()
        self.panel.show()
        self.panel.addCloseListener(onClose)
        self.panel.addButtonKeyListener(KeyListener())
        msg = "Connecting to " + self.ipAddress + ":" + str(self.port) + "..."
        print msg,
        self.panel.setText(msg)
        if self.connect():
            print "Connection established."
            self.panel.showConnect(self.ipAddress + ":" + str(self.port))
            Tools.delay(4000) # wait until "Conn" timed message has finished
        else:
            self.panel.showFail(self.ipAddress, self.port)
            raise RaspiException("Connection failed.")
        MyRobot._myInstance = self
        Tools.delay(2000)

    def registerSensor(self, sensor):
        if self.sensorThread == None:
            self.sensorThread = SensorThread()
            self.sensorThread.start()
        self.sensorThread.add(sensor)

    def startReceiver(self):
        Tools.debug("Starting Receiver thread")
        self.isReceiverRunning = True
        receiver = Receiver(self)
        receiver.start()
        while not self.isReceiverUp:
           time.sleep(0.001)
        time.sleep(0.1)

    def sendCommand(self, cmd):
        self.lock.acquire()
        Tools.debug("sendCommand() with cmd = " + cmd)
        if not self.isConn:
            raise RaspiException("Exception in Robot: sendCommand)() failed (Connection closed).")
            return Response.SEND_FAILED
        try:
            self.receiverResponse = None
            cmd += "\n";  # Append \n
            self.sock.sendall(cmd)
            reply = self.waitForReply()  # Throws exception if timeout
            self.lock.release()
            return reply    
        except:
            Tools.debug("Exception in sendCommand(): " + str(sys.exc_info()[1]))
            self.closeConnection()

        Tools.debug("Not connected. Returned: SEND_FAILED")
        self.lock.release()
        return Response.SEND_FAILED

    def waitForReply(self):
        Tools.debug("Calling waitForReply")
        startTime = time.clock()
        while self.isConn and self.receiverResponse == None and time.clock() - startTime < receiverTimeout:
            time.sleep(0.01)
        if self.receiverResponse == None:
            raise RaspiException("Exception in Robot: waitForReply failed.")
        Tools.debug("Response = " + self.receiverResponse)
        return self.receiverResponse
 
    def closeConnection(self):
        if not self.isConn:
            return
        self.isConn = False
        Tools.debug("Closing socket")
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.ipAddress, self.port))
            self.isConn = True
        except Exception, err:
#            print Exception, err
            Tools.debug("Connection failed.")
            return False
        self.startReceiver()
        return True

    def exit(self):
        if self.isExited:
            return
        if self.sensorThread != None:
            self.sensorThread.stop()
            self.sensorThread.join(2000)
        self.isExited = True
        self.closeConnection()
        self.escapeHit = True  # Take it out of isEscapeHit()
        self.buttonHit = True  # Take it out of isButtonHit()
        msg = "Connection closed."
        print msg
        self.panel.setText(msg)
        Tools.delay(5000)
        self.panel.dispose()

    def isConnected(self):
        Tools.delay(1)
        return self.isConn

    def getVersion(self):
        return self.sendCommand("robot.getVersion")

    def getIPAddresses(self):
        return self.sendCommand("robot.getIPAddresses")

    def getCurrentDevices(self):
        return self.sendCommand("robot.getCurrentDevices")

    def setSoundVolume(self, volume):
        return self.sendCommand("robot.setSoundVolume." + str(volume))

    def playTone(self, frequency, duration):
        return self.sendCommand("robot.playTone." + str(int(frequency + 0.5)) + "." + str(int(duration + 0.5)))

    def initSound(self, soundFile, volume):
        return self.sendCommand("robot.initSound." + soundFile + "." + str(int(volume)))

    def playSound(self):
        return self.sendCommand("robot.playSound")

    def stopSound(self):
        return self.sendCommand("robot.stopSound")

    def fadeooutSound(self, time):
        return self.sendCommand("robot.fadeoutSound." + str(int(time)))

    def playSound(self):
        return self.sendCommand("robot.playSound")

    def pauseSound(self):
        return self.sendCommand("robot.pauseSound")

    def resumeSound(self):
        return self.sendCommand("robot.resumeSound")

    def rewindSound(self):
        return self.sendCommand("robot.rewindSound")

    def isSoundPlaying(self):
        rc = self.sendCommand("robot.isSoundPlaying")
        if rc == "1":
           return True
        return False

    def isButtonHit(self):
        Tools.delay(1)
        if self.buttonHit:
            self.buttonHit = False
            return True
        rc = self.sendCommand("robot.isButtonHit")
        if rc == "1":
            return True
        return False

    def isEscapeHit(self):
        Tools.delay(1)
        if self.escapeHit:
            self.escapeHit = False
            return True
        return False

    def isEnterHit(self):
        Tools.delay(1)
        if self.enterHit:
            self.enterHit = False
            return True
        return False

    def isUpHit(self):
        Tools.delay(1)
        if self.upHit:
            self.upHit = False
            return True
        return False

    def isDownHit(self):
        Tools.delay(1)
        if self.downHit:
            self.downHit = False
            return True
        return False

    def isLeftHit(self):
        Tools.delay(1)
        if self.leftHit:
            self.leftHit = False
            return True
        return False

    def isRightHit(self):
        Tools.delay(1)
        if self.rightHit:
            self.rightHit = False
            return True
        return False

    def addButtonListener(self, listener):
        self._buttonEvent = listener









