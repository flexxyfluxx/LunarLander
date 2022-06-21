# __init__.py

from java.lang import RuntimeException
from pyminisim import *
from ch.aplu.jgamegrid import GameGrid
import time


BUTTON_A = "A"
BUTTON_B = "B"
BUTTONS = (BUTTON_A, BUTTON_B) 

def panic(n):
    """Enter a panic mode. Requires restart. Pass in an arbitrary integer <= 255 to indicate a status."""
    raise NotImplementedError("Execute your program on the Calliope.")

def reset():
    """Restart the board."""
    raise NotImplementedError("Execute your program on the Calliope.")

def running_time():
    """Return the number of milliseconds since the board was switched on or restarted."""
    raise NotImplementedError("Execute your program on the Calliope.")

def temperature():
    """Return the temperature of the Calliope in degrees Celcius."""
    raise NotImplementedError("Execute your program on the Calliope.")

class MicroBitAnalogDigitalPin:
    def read_analog(self):
        """Read the voltage applied to the pin, and return it as an integer between 0 (meaning 0V) and 1023 (meaning 3.3V)."""
        raise NotImplementedError("Execute your program on the Calliope.")

    def write_analog(self, value):
        """Output a PWM signal on the pin, with the duty cycle proportional to the provided value. The value may be either an integer or a floating point number between 0 (0% duty cycle) and 1023 (100% duty)."""
        raise NotImplementedError("Execute your program on the Calliope.")

    def set_analog_period(self, period):
        """Set the period of the PWM signal being output to period in milliseconds. The minimum valid value is 1ms."""
        raise NotImplementedError("Execute your program on the Calliope.")

    def set_analog_period_microseconds(self, period):
        """Set the period of the PWM signal being output to period in microseconds. The minimum valid value is 256s."""
        raise NotImplementedError("Execute your program on the Calliope.")

class MicroBitTouchPin:
    def is_touched(self):
        """Return True if the pin is being touched with a finger, otherwise return False."""
        raise NotImplementedError("Execute your program on the Calliope.")
  

def _check():
    if _sim.isDisposed():
        raise RuntimeException("Java frame disposed") 

def sleep(t):
    """Wait for n milliseconds. One second is 1000 milliseconds."""
    _check()    
    time.sleep(t / 1000)

def buttonHandler(buttonIndex):
    label = BUTTONS[buttonIndex]
    if label == 'A':
        button_a._pressed()
    if label == 'B':
        button_b._pressed()

def pinHandler(pinIndex):
    # events on pins not used
    pass
#    print "pin press event on pin", pinIndex

GameGrid.disposeAll()
_ledSize = 7
_sim = PyMiniSim(buttonHandler, pinHandler)

import displayclass
display = displayclass.Display()
from image import Image

import button
button_a = button.Button(BUTTON_A)
button_b = button.Button(BUTTON_B)

import pin
# valid pins only
pin0 = pin.MicroBitDigitalPin(0)
pin1 = pin.MicroBitDigitalPin(1)
pin2 = pin.MicroBitDigitalPin(2)
pin3 = pin.MicroBitDigitalPin(3)
pin4 = pin.MicroBitDigitalPin(4)
pin5 = pin.MicroBitDigitalPin(5)
pin6 = pin.MicroBitDigitalPin(6)
pin7 = pin.MicroBitDigitalPin(7)
pin8 = pin.MicroBitDigitalPin(8)
pin9 = pin.MicroBitDigitalPin(9)
pin10 = pin.MicroBitDigitalPin(10)
pin11 = pin.MicroBitDigitalPin(11)
pin12 = pin.MicroBitDigitalPin(12)
pin13 = pin.MicroBitDigitalPin(13)
pin14 = pin.MicroBitDigitalPin(14)
pin15 = pin.MicroBitDigitalPin(15)
pin16 = pin.MicroBitDigitalPin(16)
pin19 = pin.MicroBitDigitalPin(19)
pin20 = pin.MicroBitDigitalPin(20)


import accel
accelerometer = accel.Accelerometer()

