# button.py
# Simulation version
# Version 1.01 - June 27, 2018

import time
from oxosnake import _sim, _clickCallbacks

class Button():
    def __init__(self, buttonLabel, buttonClicked = None):
        self._buttonLabel = buttonLabel
        btnIndex = _sim.labelToIndex(buttonLabel)
        _clickCallbacks[btnIndex] = buttonClicked
        
    def wasPressed(self):
        time.sleep(0.01)  # in case of narrow loops
        return _sim.wasButtonPressed(self._buttonLabel)
    
    def isPressed(self):
        time.sleep(0.01)  # in case of narrow loops
        return _sim.isButtonPressed(self._buttonLabel)
        
