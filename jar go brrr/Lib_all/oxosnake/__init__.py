# __init__.py
# Version 1.05 - June 27, 2018

from pyoxosim import *
from ch.aplu.jgamegrid import GameGrid
from ch.aplu.util import Monitor, X11Color
from javax.swing import JColorChooser
from globals import *

def getRandomX11Color():
   return X11Color.getRandomColorStr()

	
def askColor(title, defaultColor):
   if isinstance(defaultColor, str):
      return JColorChooser.showDialog(None, title, X11Color.toColor(defaultColor))
   else:
      return JColorChooser.showDialog(None, title, defaultColor)
  

_clickCallbacks = [None] * 6

def clickHandler(buttonIndex):
   if _clickCallbacks[buttonIndex] != None:
       label = BUTTONS[buttonIndex]
       _clickCallbacks[buttonIndex](label)

GameGrid.disposeAll()
_sim = PyOxoSim(clickHandler)
from button import *
from snake import *
