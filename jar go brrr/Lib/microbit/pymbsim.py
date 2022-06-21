# pymbsim.py
# Version 1.03 - July 3, 2018

from ch.aplu.mbsim import *
from ch.aplu.jgamegrid import GGMouse

class PyMbSim(MbSim):
    def __init__(self, buttonHandler, pinHandler):
        self.buttonHandler = buttonHandler
        self.pinHandler = pinHandler

    def mouseTouched(self, actor, mouse, spot):
        MbSim.mouseTouched(self, actor, mouse, spot)
        if mouse.getEvent() == GGMouse.lPress:
            idx = self.buttonToIndex(actor)
            if (idx != -1):
                self.buttonHandler(idx)
#        idx = self.pinToIndex(actor)
#        if (idx != -1):
#            print "pin", idx

    

