# accelerometer.py
# Simulation version
# Version 1.01 - July 11, 2018

from oxocard import _sim, _setTapCallback
import thread
import time
from math import atan2, asin, sqrt, degrees

_click_callback = None

class Accelerometer():
    SINGLE_CLICK_X = 0x01
    DOUBLE_CLICK_X = 0x02
    SINGLE_CLICK_Y = 0x04
    DOUBLE_CLICK_Y = 0x08
    SINGLE_CLICK_Z = 0x10
    DOUBLE_CLICK_Z = 0x20
   
    _instance = None
    _trigger_level = 0
    _rearm_time = 0
    _click_config = 0

    _instance = None

    def __init__(self, *args):
        if len(args) != 1 or args[0] != "$$$xxxprivate":
            raise Exception("Use factory method create() to return a single instance")
        _setTapCallback(self._onTap)
        self._isRunning = False
        self._clicked = False
    
    def getX(self):
        return _sim.getAccelX()

    def getY(self):
        return _sim.getAccelY()

    def getZ(self):
        return _sim.getAccelZ()

    def getValues(self):
        return tuple(_sim.getAccelValues().tolist())

    def getTemperature(self):
        return _sim.getTemperature()
    
    def wasClicked(self):
        tmp = self._clicked
        self._clicked = False
        return tmp
    
    def getPitch(self):
        a = self.getValues()
        print "pitch", a
        pitch = atan2(a[1], a[2])
        return -int(degrees(pitch))
    
    def getRoll(self):
        a = self.getValues()
        print "roll", a
        anorm = sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])
        if anorm == 0:
            return 0
        roll = asin(a[0] / anorm)
        return int(degrees(roll))
    
    def dispose(self):
        pass

    @staticmethod
    def create(click_callback = None, **kwargs):
        global _click_callback
        _click_callback = click_callback    
        Accelerometer._trigger_level = 10
        Accelerometer._rearm_time = 0.2
        Accelerometer._click_config = Accelerometer.SINGLE_CLICK_X | Accelerometer.SINGLE_CLICK_Y | Accelerometer.SINGLE_CLICK_Z
        for key in kwargs:
            if key == 'trigger_level': # in range 1..100,  1: highest sensitivity, 100: lowest sensitiviy; default: 10
                Accelerometer._trigger_level = max(1, kwargs[key])  # not supported in simulation mode
            if key == 'rearm_time': # time in s until sensor is rearmed; default: 0.2
                Accelerometer._rearm_time = kwargs[key]
            if key == 'click_config': # click configuration; default CLICK_X | CLICK_Y | CLICK_Z
                Accelerometer._click_config = kwargs[key]
        if Accelerometer._instance == None:
            Accelerometer._instance = Accelerometer("$$$xxxprivate")
            _sim.createAccelerometer()
        return Accelerometer._instance
    
    def _onTap(self, isSingleClick, index):
        if self._isRunning and isSingleClick:
            return
        if isSingleClick:
            if index == 0 and Accelerometer._click_config & 0x01:
                if _click_callback != None:
                    _click_callback()
                self._clicked = True
            elif index == 1 and Accelerometer._click_config & 0x04:
                if _click_callback != None:
                    _click_callback()
                self._clicked = True
            elif index == 2 and Accelerometer._click_config & 0x10:
                if _click_callback != None:
                    _click_callback()
                self._clicked = True
        else: 
            if index == 0 and Accelerometer._click_config & 0x02:
                if _click_callback != None:
                    _click_callback()
            elif index == 1 and Accelerometer._click_config & 0x08:
                if _click_callback != None:
                    _click_callback()
            elif index == 2 and Accelerometer._click_config & 0x20:
                if _click_callback != None:
                    _click_callback()
        thread.start_new_thread(self._run, ())
        
    def _run(self):
        self._isRunning = True
        time.sleep(max(0.1 , Accelerometer._rearm_time))
        self._isRunning = False
        
        
