# pyoxosim.py
# Version 1.02 - July 11, 2018

from ch.aplu.oxosim import *
from ch.aplu.jgamegrid import GGMouse

class PyOxoSim(OxoSim):
    def __init__(self, clickHandler, tapHandler):
        self.clickCallback = clickHandler
        self.tapCallback = tapHandler

    def mouseTouched(self, actor, mouse, spot):
        OxoSim.mouseTouched(self, actor, mouse, spot)
        if mouse.getEvent() == GGMouse.lClick:
            idx = self.buttonToIndex(actor)
            if (idx != -1):
                self.clickCallback(idx)
                
    def accelValuesChanged(self, values):
        pass
#        print "Accel Values:", values             
      
    def temperatureChanged(self, temperature):
        pass
#        print "Temp", temperature             
    
    def singleClick(self, index):
        self.tapCallback(True, index)    

    def doubleClick(self, index):    
        self.tapCallback(False, index)    

