# __init__.py
# Version 1.05 - July 11, 2018

from pyoxosim import *
from time import sleep
from ch.aplu.jgamegrid import GameGrid
from ch.aplu.util import Monitor, X11Color
from javax.swing import JColorChooser
from globals import *
from java.lang import RuntimeException

def _check():
    if _sim.isDisposed():
        raise RuntimeException("Java frame disposed") 

def getRandomX11Color():
   return X11Color.getRandomColorStr()

def sleep(t):
    _check()    
    time.sleep(t)    

def askColor(title, defaultColor):
   if isinstance(defaultColor, str):
      return JColorChooser.showDialog(None, title, X11Color.toColor(defaultColor))
   else:
      return JColorChooser.showDialog(None, title, defaultColor)
  
_buttonClickCallbacks = [None] * 6
_tapCallback = None

def _setTapCallback(cb):
    global _tapCallback
    _tapCallback = cb
    
def _buttonClickHandler(buttonIndex):
   if _buttonClickCallbacks[buttonIndex] != None:
       label = BUTTONS[buttonIndex]
       _buttonClickCallbacks[buttonIndex](label)
       
def _tapHandler(isSingleClick, tapIndex):
    if _tapCallback != None:
        _tapCallback(isSingleClick, tapIndex)
        
GameGrid.disposeAll()
_sim = PyOxoSim(_buttonClickHandler, _tapHandler)
from button import *
from oxogrid import *
from accelerometer import *


