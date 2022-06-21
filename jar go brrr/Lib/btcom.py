# btcom.py
# TJ version
# Author: AP

'''
Library that implements a event-based Bluetooth client-server system in contrast to the standard stream-based systems.
Messages are sent in byte blocks (may be UTF-8 or ASCII encoded strings). The null charactor is used as 
End-of-Transmission indicator. The Bluetooth RFCOMM protocol is used.

Dependencies: Java Bluecove library: bluecove-2.1.1-SNAPSHOT.jar, bluecove-gpl-2.1.1.jar
'''

from threading import Thread
import thread
import socket
import time
import sys
from ch.aplu.bluetooth import *
from java.io import *
from javax.microedition.io import *
from javax.bluetooth import *

BTCOM_VERSION = "1.02 - April 12, 2017"

# ================================== Server ================================
# ---------------------- class BTServer ------------------------
class BTServer(Thread):
    '''
    Class that represents a Bluetooth server.
    '''
    isVerbose = False
    CONNECTED = "CONNECTED"
    LISTENING = "LISTENING"
    TERMINATED = "TERMINATED"
    MESSAGE = "MESSAGE"

    def __init__(self, serviceName, stateChanged, isVerbose = False):
        '''
        Creates a Bluetooth server that listens for a connecting client. 
        The server runs in its own thread, so the
        constructor returns immediately. State changes invoke the callback
        onStateChanged(state, msg) where state is one of the following strings:
        "LISTENING", "CONNECTED", "MESSAGE", "TERMINATED". msg is a string with
        further information: LISTENING: empty, CONNECTED: Bluetooth name (MAC address), MESSAGE: 
        message received, TERMINATED: empty. The server uses an internal handler 
        thread to detect incoming messages.
        @param serviceName: the service name the server is exposing
        @param stateChanged: the callback function to register
        @param isVerbose: if true, debug messages are written to System.out, default: False
        '''
        Thread.__init__(self)
        self.serviceName = serviceName
        self.stateChanged = stateChanged
        BTServer.isVerbose = isVerbose
        self.isClientConnected = False
        self.socketHandler = None
        self.clientSocket = None
        self.istream = None
        self.ostream = None
        self.start()

    def run(self):
        BTServer.debug("BTServer thread started")
        connectionUrl = "btspp://localhost:68EE141812D211D78EED00B0D03D76EC;name=" + self.serviceName
        BTServer.debug("Connection URL: " + connectionUrl)
        self.serverSocket = Connector.open(connectionUrl)
        self.isServerRunning = True
        self.isTerminating = False        
        try:
            self.stateChanged(BTServer.LISTENING, "")
        except Exception, e:
            print "Caught exception in BTServer.LISTENING:", e
        while self.isServerRunning:
            BTServer.debug("Call acceptAndOpen()")
            try:
                self.clientSocket = self.serverSocket.acceptAndOpen()  # Blocking
            except:
                BTServer.debug("Exception from acceptAndOpen()")
                self.isServerRunning = False
            if not self.isServerRunning:    
                break
            BTServer.debug("Returned from acceptAndOpen()")
            rd = RemoteDevice.getRemoteDevice(self.clientSocket)
            self.remoteName = rd.getFriendlyName(False)
            self.remoteAddress = rd.getBluetoothAddress()
            address = ""
            for n in range(6):
                address += self.remoteAddress[2*n:2*n+2] + ":"
            address = address[:-1]    
            BTServer.debug("Accepted connection from " + self.remoteName +
                    " with address " + address)
            try: 
                self.stateChanged(BTServer.CONNECTED, self.remoteName + " (" + address + ")")
            except Exception, e:
                print "Caught exception in BTServer.CONNECTED:", e

            self.istream = DataInputStream(self.clientSocket.openInputStream())
            self.ostream = DataOutputStream(self.clientSocket.openOutputStream())
            self.isClientConnected = True
            self.socketHandler = ServerHandler(self)
            self.socketHandler.start()
            
        self._closeClient()    
        try:
            self.stateChanged(BTServer.TERMINATED, "")
        except Exception, e:
            print "Caught exception in BTServer.TERMINATED:", e
        BTServer.debug("Server thread terminated")

    def _closeClient(self):
        if self.socketHandler != None:
            self.socketHandler.isSocketHandlerRunning = False
        try:
            self.istream.close()
        except:
            pass    
        try:
            self.ostream.close()
        except:
            pass    
        try:
            self.clientSocket.close()
        except:
            pass    

    def disconnect(self):
        '''
        Closes the connection with the client and enters
        the LISTENING state
        '''
        BTServer.debug("Calling Server.disconnect()")
        if self.isClientConnected and not self.isTerminating:
            self.isClientConnected = False
            try:
                self.stateChanged(BTServer.LISTENING, "")
            except Exception, e:
                print "Caught exception in BTServer.LISTENING:", e
            BTServer.debug("Close client socket now")
            self._closeClient()

    def sendMessage(self, msg):
        '''
        Sends the information msg to the client (as String, the character \0 (ASCII 0) serves as end of
        string indicator, it is transparently added and removed)
        @param msg: the message to send
        '''
        BTServer.debug("sendMessage() with msg = " + msg)
        if not self.isClientConnected:
            BTClient.debug("sendMessage(): Connection closed.")
            return
        try:
            self.ostream.writeBytes(msg + "\0")
            self.ostream.flush()
        except:
            BTServer.debug("sendMessage(): Connection lost.")
            self.disconnect(None)

    def terminate(self):
        '''
        Terminates the server (finishs the listening state).
        '''
        BTServer.debug("Calling terminate()")
        self.isTerminating = True
        self._closeClient()    
        self.serverSocket.close()

    def isConnected(self):
        '''
        Returns True, if a client is connected to the server.
        @return: True, if the communication link is established
        '''
        return self.isClientConnected
    
    def isTerminated(self):
        '''
        Returns True, if the server is in TERMINATED state.
        @return: True, if the server thread is terminated
        '''
        return not self.isServerRunning

    @staticmethod
    def debug(msg):
        if BTServer.isVerbose:
            print "   BTServer-> " + msg
 
    @staticmethod
    def getVersion():
        '''
        Returns the library version.
        @return: the current version of the library
        '''
        return BTCOM_VERSION
   
# ---------------------- class ServerHandler ------------------------
class ServerHandler(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self.server = server

    def run(self):
        BTClient.debug("ServerHandler thread started")
        self.isSocketHandlerRunning = True
        bufSize = 8192
        try:
            data = bytearray()
            import jarray
            buf = jarray.zeros(bufSize, "b")
            while self.isSocketHandlerRunning:
                inBlock = True
                while inBlock:
                    count = self.server.istream.read(buf)
                    if count == -1:
                        raise Exception("Returning from istream.read() with count = -1")
                    data.extend(buf[0:count])
                    if '\0' in data:
                        junk = data.split('\0')  # more than 1 message may be received if
                                                 # transfer is fast. data: xxxx\0yyyyy\0zzz\0
                        for i in range(len(junk) - 1):
                            BTServer.debug("Received message: " + str(junk[i]) + " len: " + str(len(junk[i])))
                            if len(junk[i]) > 0:
                                try:
                                    self.server.stateChanged(BTServer.MESSAGE, str(junk[i]))
                                except Exception, e:
                                    print "Caught exception in BTServer.MESSAGE:", e
                            else:
                                BTServer.debug("Got empty message as EOT")
                                BTServer.debug("ServerHandler thread terminated")
                                self.server.disconnect()
                                return     
                        inBlock = False
                        data = bytearray(junk[len(junk) - 1])  # remaining bytes        
        except:  # Happens if client is disconnecting
            BTServer.debug("Exception from blocking read(), Msg: " + str(sys.exc_info()[1]))
            self.server.disconnect()  
        BTServer.debug("ServerHandler thread finished")


# ================================== Client ================================
# -------------------------------- class BTClient --------------------------
class BTClient():
    '''
    Class that represents a Bluetooth socket based client. To connect a client via Bluetooth,
    the Bluetooth MAC address (12 hex characters) and the Bluetooth port (channel) of the server
    must be known (server info). All other server information is irrelevant (Bluetooth friendly name, Bluetooth service name),
    but the server info may be retrieved by a Bluetooth search from the server name or the service name.
    '''
    isVerbose = False
    CONNECTING = "CONNECTING"
    CONNECTION_FAILED = "CONNECTION_FAILED"
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    MESSAGE = "MESSAGE"

    def __init__(self, stateChanged, isVerbose = False):
        '''
        Creates a Bluetooth client prepared for a connection with a
        BTServer. The client uses an internal handler thread to detect incoming messages.
        State changes invoke the callback
        onStateChanged(state, msg) where state is one of the following strings:
        "CONNECTING", "CONNECTED", "CONNECTION_FAILED", "DISCONNECTED", "MESSAGE". msg is a string with
        additional information: CONNECTING: serverInfo, CONNECTED: serverInfo, 
        CONNECTION_FAILED: serverInfo, DISCONNECTED: empty, MESSAGE: message received
        @param stateChanged: the callback function to register
        @param isVerbose: if true, debug messages are written to System.out
        '''
        self.isClientConnected = False
        self.isClientConnecting = False
        self.serviceName = ""
        self.macAddress = ""
        self.channel = -1
        self.stateChanged = stateChanged
        self.inCallback = False
        BTClient.isVerbose = isVerbose
                  
    def sendMessage(self, msg):
        '''
        Sends the information msg to the server (as String, the character \0
        (ASCII 0) serves as end of string indicator, it is transparently added
        and removed).  
        @param msg: the message to send
        '''
        BTClient.debug("sendMessage() with msg = " + msg)
        if not self.isClientConnected:
            BTClient.debug("sendMessage(): Connection closed.")
            return
        try:
            self.ostream.writeBytes(msg + "\0")
            self.ostream.flush()
        except:
            BTClient.debug("sendMessage(): Connection reset by peer.")
            self.disconnect(None)
            
    def connect(self, serverInfo, timeout):
        '''
        Performs a connection trial to the server with given serverInfo. If the connection trial fails, 
        it is repeated until the timeout (in s) is reached.
        @param serverInfo: a tuple ("nn:nn:nn:nn:nn:nn", channel) with the Bluetooth MAC address string 
        (12 hex characters, upper or lower case, separated by :) and  Bluetooth channel (integer),
        e.g. ("B8:27:EB:04:A6:7E", 1)
        @param timeout: the maximum time for the connection trial (in s)
        @return: True, if connection is established; otherwise False
        '''
        self.isClientConnectiong = True
        maxNbRetries = 10   
        try:
            self.stateChanged(BTClient.CONNECTING, serverInfo)
        except Exception, e:
            print "Caught exception in BTClient.CONNECTING:", e
        nbRetries = 0
        startTime = time.time()
        rc = False
        while (not rc) and time.time() - startTime <  timeout and nbRetries < maxNbRetries:
            BTClient.debug("Starting connect #" + str(nbRetries))
            rc = self._connect(serverInfo)
            if rc == False:
                nbRetries += 1
                time.sleep(3)
        BTClient.debug("connect() returned " + str(rc) + " after " + str(nbRetries) + " retries")
        if rc:         
            BTClient.debug("Connection established")
            self.isClientConnected = True
            self.isNormalDisconnect = True
            try:
                self.stateChanged(BTClient.CONNECTED, serverInfo )
            except Exception, e:
                print "Caught exception in BTClient.CONNECTED:", e
            ClientHandler(self)        
        else:
            BTClient.debug("Connection failed")
            self.isClientConnected = False
            try:
               self.stateChanged(BTClient.CONNECTION_FAILED, serverInfo)
            except Exception, e:
               print "Caught exception in BTClient.CONNECTION_FAILED:", e
        self.isClientConnectiong = False
        return rc 
    
    def _connect(self, serverInfo):
        self.macAddress = serverInfo[0].replace(":", "")
        self.channel = serverInfo[1]
        url = "btspp://" + self.macAddress + ":" + str(self.channel)
        BTClient.debug("Trying to connect with connection url: " + str(url))
        try:
            self.clientSocket = Connector.open(url)
            self.istream = DataInputStream(self.clientSocket.openInputStream())
            self.ostream = DataOutputStream(self.clientSocket.openOutputStream())
        except:
            BTClient.debug("Exception from Connector.open().\n     Msg: " + str(sys.exc_info()[1]))
            return False
        return True

    def findServer(self, serverName, timeout):
        '''
        Perform a device inquiry for the given server name.
        @param timeout: the maximum time in seconds to search
        @return: a tuple with the Bluetooth MAC address and the Bluetooth channel; None if inquiry failed
        '''
        self.serverName = serverName
        nbRetries = 0
        startTime = time.time()
        rc = None
        while rc == None and time.time() - startTime <  timeout:
            BTClient.debug("Starting inquire #" + str(nbRetries))
            rc = self._inquireMAC(serverName, True)
            if rc == None:
                nbRetries += 1
                time.sleep(2)
        return rc   
    
    def findService(self, serviceName, timeout):
        '''
        Perform a service inquiry for the given service name.
        @param timeout: the maximum time in seconds to search
        @return: a tuple with the Bluetooth MAC address and the Bluetooth channel; None if inquiry failed
        '''
        nbRetries = 0
        startTime = time.time()
        rc = None
        while rc == None and time.time() - startTime <  timeout:
            BTClient.debug("Starting inquire #" + str(nbRetries))
            rc = self._inquireMAC(serviceName, False)
            if rc == None:
                nbRetries += 1
                time.sleep(2)
        return rc

    def _inquireMAC(self, name, isServerName):
        global btf, serviceInfo, isServiceSearchFinished
        isServiceSearchFinished = False
        BTClient.debug("Create BluetoothFinder()")
        uuid_RFCOMM = int(0x03)
        uuids = [uuid_RFCOMM]
        serviceInfo = []
        btf = BluetoothFinder(uuids, False, MyBluetoothResponder())
        BTClient.debug("Searching for RFCOMM devices")
        while not isServiceSearchFinished:
            time.sleep(0.01)
        if len(serviceInfo) == 0:
            return None
        for i in range(len(serviceInfo)):
            info = serviceInfo[i]
            BTClient.debug("serviceInfo #" + str(i) + ": " + str(info))
            if isServerName:
                infoIndex = 0
            else:     
                infoIndex = 1
            if info[infoIndex] == name: 
                connectionUrl = info[2]
                BTClient.debug(name + " found. connectionUrl = " + connectionUrl)
                address = connectionUrl[8:20]
                self.macAddress = ""
                for i in range(6):
                    self.macAddress += address[2*i:2*i + 2] + ":"
                self.macAddress = self.macAddress[:-1]    
                self.channel = int(connectionUrl[21:connectionUrl.index(';')])
                return self.macAddress, self.channel
        return None
      
    def disconnect(self, endOfTransmission = ""):
        '''
        Closes the connection with the server. The endOfTransmission message is sent to the 
        server to notify the disconnection.
        @param endOfTransmission: the message sent to the server (appended by \0)
        Default: "", None: no notification sent
        '''
        if self.inCallback:  # two threads may call in rapid sequence
            return
        self.inCallback = True
        BTClient.debug("Client.disconnect()")
        if not self.isClientConnected:
            BTClient.debug("Connection already closed")
            return
        if endOfTransmission != None:
            self.sendMessage(endOfTransmission)
        self.isClientConnected = False
        BTClient.debug("Closing socket")
        self._closeClient()
        try:
            self.stateChanged(BTClient.DISCONNECTED, "")
        except Exception, e:
            print "Caught exception in BTClient.DISCONNECTED:", e
        self.inCallback = False

    def isConnecting(self):
        '''
        Returns True of client is connnecting to the server.
        @return: True, if the client performs a connection trial
        '''
        return self.isClientConnecting
 
    def isConnected(self):
        '''
        Returns True of client is connnected to the server.
        @return: True, if the connection is established
        '''
        return self.isClientConnected
    
    def getMacAddress(self):
        '''
        Returns the Bluetooth MAC address in format "nn:nn:nn:nn:nn::nn"
        '''
        return self.macAddress

    def getChannel(self):
        '''
        Returns the Bluetooth channel.
        '''
        return self.channel

    def _closeClient(self):
        try:
            self.istream.close()
        except:
            pass    
        try:
            self.ostream.close()
        except:
            pass    
        try:
            self.clientSocket.close()
        except:
            pass    

    @staticmethod
    def debug(msg):
        if BTClient.isVerbose:
            print "   BTClient-> " + msg

    @staticmethod
    def getVersion():
        '''
        Returns the library version.
        @return: the current version of the library
        '''
        return TCPCOM_VERSION

# -------------------------------- class ClientHandler ---------------------------
class ClientHandler(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self.client = client
        self.start()
                
    def run(self):
        BTClient.debug("ClientHandler thread started")
        bufSize = 8192
        try:
            data = bytearray()
            import jarray
            buf = jarray.zeros(bufSize, "b")
            while True:
                inBlock = True
                while inBlock:
                    count = self.client.istream.read(buf)
                    if count == -1:
                        raise Exception("Returning from istream.read() with count = -1")
                    data.extend(buf[0:count])
                    if '\0' in data:
                        junk = data.split('\0')  # more than 1 message may be received if
                                                 # transfer is fast. data: xxxx\0yyyyy\0zzz\0
                        for i in range(len(junk) - 1):
                            BTClient.debug("Received message: " + str(junk[i]) + " len: " + str(len(junk[i])))
                            if len(junk[i]) > 0:
                                try:
                                    self.client.stateChanged(BTClient.MESSAGE, str(junk[i]))
                                except Exception, e:
                                    print "Caught exception in BTClient.MESSAGE:", e
                        inBlock = False
                        data = bytearray(junk[len(junk) - 1])  # remaining bytes        
        except:  # Happens if client is disconnecting
            BTClient.debug("Exception from blocking read(), Msg: " + str(sys.exc_info()[1]))
            self.client.disconnect()  
        BTClient.debug("ClientHandler thread finished")
        
class MyBluetoothResponder(BluetoothResponder):
    def notifyBluetoothDeviceSearch(self, deviceTable):
        global reply, isServiceSearchFinished
        if deviceTable.size() > 0:
            BTClient.debug("Found: " + str(deviceTable.size()) + " devices")
            for i in range(deviceTable.size()):
                di = deviceTable.elementAt(i)
                dev = di.getRemoteDevice()
                deviceName = btf.getDeviceName(dev)
                dc = di.getDeviceClass()
                majorDC = dc.getMajorDeviceClass()
                minorDC = dc.getMinorDeviceClass()
                BTClient.debug("Device found. Name: " + deviceName)
                BTClient.debug("Major Device Class: " +  str(majorDC))
                BTClient.debug("Minor Device Class: " +  str(minorDC))
            BTClient.debug("Searching for RFCOMM services")
            isServiceSearchFinished = False
        else:
           BTClient.debug("No device found")
           isServiceSearchFinished = True
           reply = ""
           

    def notifyBluetoothServiceSearch(self, serviceTable):
        global serviceInfo, isServiceSearchFinished
        if serviceTable.size() > 0:
            BTClient.debug("Found: " + str(serviceTable.size()) + " services")
            for i in range(serviceTable.size()):
                si = serviceTable.elementAt(i)
                dev = si.getRemoteDevice()
                sr = si.getServiceRecord()

                # determine services of the following host: 
                deviceName = btf.getDeviceName(dev)
                BTClient.debug("Service of host "  + deviceName)
                de = sr.getAttributeValue(0x0100)
                if de != None:
                    serviceName = de.getValue()
                else:
                    serviceName = "none"
                BTClient.debug("   Service name " + serviceName)
                serviceUrl = sr.getConnectionURL(0, False)
                BTClient.debug("   Connection URL: " + serviceUrl)
                serviceInfo.append((deviceName, serviceName, serviceUrl))
        else:
            BTClient.debug("No services found")
        isServiceSearchFinished = True  
  
