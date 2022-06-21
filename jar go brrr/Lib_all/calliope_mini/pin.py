# pin.py
# Version 1.00 - July 2, 2018

from calliope_mini import _sim
import time

class MicroBitDigitalPin:   
    def __init__(self, pinNumber):
        self._pinNumber = pinNumber

    def read_digital(self):
        """Return 1 if the pin is high, and 0 if it is low."""
        time.sleep(0.01)  # in case of narrow loops
        return 1 if _sim.isPinActive(self._pinNumber) else 0

    def write_digital(self, value):
        """Set the pin to high if value is 1, or to low, if it is 0."""
        state = True if value == 1 else False
        _sim.setPinActive(self._pinNumber, state)

