# pyminisim.py
# Version 1.00 - Dec 3, 2018

from ch.aplu.minisim import *
from ch.aplu.jgamegrid import GGMouse

class PyMiniSim(MiniSim):
    def __init__(self, buttonHandler, pinHandler):
        self.buttonHandler = buttonHandler
        self.pinHandler = pinHandler

    def mouseTouched(self, actor, mouse, spot):
        MiniSim.mouseTouched(self, actor, mouse, spot)
        if mouse.getEvent() == GGMouse.lPress:
            idx = self.buttonToIndex(actor)
            if (idx != -1):
                self.buttonHandler(idx)
#        idx = self.pinToIndex(actor)
#        if (idx != -1):
#            print "pin", idx

    

