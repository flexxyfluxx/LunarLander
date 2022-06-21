# pyoxosim.py
# Version 1.01 - July 4, 2018

from ch.aplu.oxosim import *
from ch.aplu.jgamegrid import GGMouse

class PyOxoSim(OxoSim):
    def __init__(self, clickHandler):
        self.cb = clickHandler

    def mouseTouched(self, actor, mouse, spot):
        OxoSim.mouseTouched(self, actor, mouse, spot)
        if mouse.getEvent() == GGMouse.lClick:
            idx = self.buttonToIndex(actor)
            if (idx != -1):
                self.cb(idx)
      

    

