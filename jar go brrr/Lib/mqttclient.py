# mqttclient.py
# -*- coding: utf-8 -*-

from threading import Thread
from paho.mqtt.client import Client, MQTT_ERR_SUCCESS
import thread
import random
import string
from tcpcom import HTTPServer

MQTTCLIENT_VERSION = "1.16 - Feb. 3, 2018"

# -------------------------- Class MessageThread ----------------------------
class _MessageThread(Thread):
    def __init__(self, client, messageReceived, topic, payload):
        Thread.__init__(self)
        self.client = client
        self.messageReceived = messageReceived
        self.topic = topic
        self.payload = payload
        self.start()
        
    def run(self):
        try:
            self.messageReceived(self.topic, self.payload)
        except Exception, e:        
            self.client._debug("Exception in message callback: " + str(e))

# -------------------------- Class MQTTClient ----------------------------
class MQTTClient(Thread):
    '''
    Class that represents a MQTT client based on paho-mqtt package.
    '''
    def __init__(self, messageReceived = None, username = "", password = ""):
        '''
        Creates a MQTTClient that publishes and/or subcribes MQTT topics. Messages from subcribed topics trigger the 
        given messageReceived function. The client does not yet connect to a MQTT broker.
        @param messageReceived: the callback function with parameters topic, msg triggerd by incoming messages
        running in a separate thread. If None, no message notifications are triggered, e.g. for a client that only publishes topics.
        @param username: the username used to log into the MQTT broker (empty, if no user authentication is necessary)
        @param password: the password used to log into the MQTT broker (empty, if no user authentication is necessary)
        '''
        Thread.__init__(self)
        self.username = username
        self.password = password
        self.messageReceived = messageReceived
        self.verbose = False
        self.log = False
        self.client = Client()
        self.client.on_message = self._onMessage
        self.client.on_log = self._onLog
        if username != "":
            self.client.username_pw_set(username, password)
            
    def run(self):            
        self._debug("MQTTHander thread started")
        self.client.loop_forever()
        self._debug("MQTTHandler thread terminated")
        
    def setVerbose(self, verbose):
        '''
        Enables/disables logger messages printed to stdout.
        @param verbose: if True, the logger messages are enabled; otherwise disabled
        '''    
        self.verbose = verbose

    def connect(self, host, port = 1883, keepalive = 60):
        '''
        Starts a connection trial to the given MQTT broker at given port (default: 1883).
        @host: the IP address of the broker
        @port: the port where the broker is listening (default: 1883)
        @param keepalive: maximum period in seconds between communications with the broker. 
        If no other messages are exchanged, time period for ping messages to the broker (default: 60 s)
        @return: True, if the connection is successful; otherwise False
        '''
        self.host = host
        self.port = port
        self._debug("connect() with host: " + host + " port: " + str(port) + " keepalive: " + str(keepalive))
        try:
            self.client.connect(host, port, keepalive)
        except:
            return False
        if self.messageReceived != None:
            self.start() # start thread only if necessary get message callbacks
        return True

    def disconnect(self):
        '''
        Disconnects the client from the broker.
        '''
        self._debug("disconnect()")
        self.client.disconnect()

    def publish(self, topic, payload, qos = 0, retain = False):
        '''
        Sends a message with given topic and payload to the broker.
        @param topic: the topic that the message should be published on (string)
        @param payload: the message to send. An int or float will converted it to a string. 
        @param qos: the quality of service level to use (number 0, 1, 2) (default: 0)
        @param retain: if True, the message is the “last known good”/retained message for the topic (default: False)
        '''
        self._debug("publish() with topic: '" + topic + "' payload: " + str(payload) + " qos: " + str(qos))
        infot = self.client.publish(topic, payload, qos, retain)
        if infot.rc != MQTT_ERR_SUCCESS:
            return False
        try:
            infot.wait_for_publish()
        except:
            self._debug("wait_for_publish() throwed exception")
            return False
        return True

    def subscribe(self, topic, qos = 0):
        '''
        Subscribes the client to one or more topics.
        @param topic: a string or a list of tuples of format (topic, qos)
        @param qos: the quality of service level (number 0, 1, 2) (default: 0); not used, if topic is a list of tuples
        '''
        self._debug("subscribe() with topic: '" + topic + "' qos: " + str(qos))
        self.client.subscribe(topic, qos)
        
        def unsubscribe(self, topic):
            '''
            Unsubscribes the client for one or more topics.
                topic
                    a single string or a list of strings
            '''
            self.client.unsubscribe(topic)
        
    # ------------------- Callbacks -------------------------------------------
    def _onMessage(self, client, obj, msg):
        self._debug("onMessage() topic: '" + msg.topic + "' qos: " + str(msg.qos) + " payload: " + msg.payload)
        if self.messageReceived != None:
            _MessageThread(self, self.messageReceived, msg.topic, msg.payload)

    def _onLog(self, client, obj, level, msg):
        self._debug("onLog() msg: " + msg)

    def _debug(self, msg):
        if self.verbose:
            print("   MQTTClient-> " + msg)


# -------------------------- Class GameClient ----------------------------
# 'Has-a' MQTTClient

class GameClient:   
    '''
    Class that exposes a MQTT client specially designed for a two players game.
    '''
    def __init__(self, stateChanged, messageReceived, topic = "/ch/aplu/mqtt/gameclient"):
        '''
        Creates a GameClient instance to handle game state information and message exchange.
        @param stateChanged: a callback function stateChanged(state) that is triggered when the game state is
        modified. state values: 'CONNECTING' (while connecting to the broker), 'CONNECTED' (if connected to broker, but
        waiting for a partner), 'READY' (both players ready to play, 'DISCONNECTED' (the partner disconnected)
        @param messageReceived: a callback function messageReceived(msg) triggered when a message arrived
        @param topic: the MQTT topic to use for data exchange (default: /ch/aplu/mqtt/gameclient)
        '''
        # random id
        self.myId = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
        self.stateChanged = stateChanged
        self.messageReceived = messageReceived
        self.topic = topic
        self.state = "IDLE"
        self.myName = ""
        self.partnerName = ""
        self.partnerIP = ""
        self.m = MQTTClient(messageReceived = self._onMessageReceived)

    def setName(self, name):
        '''
        Sets the name that is communicated to the partner when entering the READY state.
        @param name: the name of this player
        '''
        self.myName = name
        
    def connect(self, host, port = 1883):
        '''
        Enganges a connection trial to the MQTT broker.
        @param host: the IP address of the broker
        @param port: the IP port of the broker (default: 1883)
        '''
        self.state = "CONNECTING"
        self.stateChanged(self.state)
        if self.m.connect(host, port):
            self.m.subscribe(self.topic)
            self.sendMessage("_ENTERED," + self.myName + "," + HTTPServer.getServerIP())
            self.state = "CONNECTED"
            self.stateChanged(self.state)
            return True
        self.state = "DISCONNECTED"
        self.stateChanged(self.state)
        return False
    
    def disconnect(self):
        '''
        Disconnects the MQTT client from the broker. Sends a "DISCONNECT" message to the partner.
        '''
        self.state = "DISCONNECTED"
        self.stateChanged(self.state)
        self.sendMessage("DISCONNECT")
        self.m.disconnect()
    
    def sendMessage(self, text):
        '''
        Sends a message to the partner.
        @param text: a message string
        '''
        self.m.publish(self.topic, text + "@" + self.myId)
        
    def getState(self):
        '''
        Returns the current state. One of 'IDLE', 'CONNECTING', 'CONNECTED', 'READY', 'DISCONNECTED'.
        '''
        return self.state    
    
    def getPartnerName(self):
        '''
        Gets the game partner's name that is communicated by the partner when entering the READY state.
        Empty if not yet ready.
        '''
        return self.partnerName

    def getPartnerAddress(self):
        '''
        Gets the game partner's IP address that is communicated by the partner when entering the READY state.
        Empty if not yet ready.
        '''
     
        return self.partnerIP

    def _onMessageReceived(self, topic, msg):
        message, id = msg.split('@')
        if id == self.myId:
            return
        if message[0:8] == "_ENTERED":
            info = message.split(',')
            self.partnerName = info[1]
            self.partnerIP = info[2]
            if self.state == "CONNECTED":
                self.sendMessage("_ENTERED," + self.myName + "," + HTTPServer.getServerIP())
                self.state = "READY"
                self.stateChanged(self.state)
        else:
            self.messageReceived(message)

def __main():    
    host = "broker.dynns.com"
    
    def onMessageReceived(msg):
        print "msg:", msg

    def onStateChanged(state):
        print "state:", state
    
    client = GameClient(onStateChanged, onMessageReceived)
    if client.connect(host):
        msgDlg("Running. OK to stop.")
        client.disconnect()
    else:
        print "Connection to broker failed"

#__main()    

