# button.py
# Version 1.00 - July 2, 2018

from calliope_mini import _sim
import time

class Button:
    def __init__(self, buttonLabel):
        self._buttonLabel = buttonLabel
        self._count = 0

    def is_pressed(self):
        """Returns True if the specified button button is pressed, and False otherwise."""
        time.sleep(0.01)  # in case of narrow loops
        return _sim.isButtonPressed(self._buttonLabel)

    def was_pressed(self):
        """Returns True or False to indicate if the button was pressed since the device started or the last time this method was called."""
        time.sleep(0.01)  # in case of narrow loops
        return _sim.wasButtonPressed(self._buttonLabel)

    def get_presses(self):
        """Returns the running total of button presses, and resets this total to zero before returning."""
        count = self._count
        self._count = 0
        return count
    
    def _pressed(self):
        self._count += 1
 
 
