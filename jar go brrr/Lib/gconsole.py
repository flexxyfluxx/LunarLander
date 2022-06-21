# gconsole.py
# AP
# Version 2.0, June 5, 2017

from ch.aplu.util import GConsole, Position, Size
from java.awt import Font
from java.awt.event import KeyEvent
from sys import exit
from enum import enum

_c = None

class WindowNotInitialized(Exception): pass

def isConsoleValid():
   if _c == None: 
      raise WindowNotInitialized("Use \"makeConsole()\" to create the a GConsole window.")

def makeConsole(*args):
   global _c
   _c = do(GConsole, args)
   _c.setClosingMode(GConsole.ClosingMode.ReleaseOnClose)
   return _c

def do(fun, args):
   y = None
   if len(args) == 0:
      y = fun()
   elif len(args) == 1:
      y = fun(args[0])
   elif len(args) == 2:
      y = fun(args[0], args[1])
   elif len(args) == 3:
      y = fun(args[0], args[1], args[2])
   elif len(args) == 4:
      y = fun(args[0], args[1], args[2], args[3])
   elif len(args) == 5:
      y = fun(args[0], args[1], args[2], args[3], args[4])
   elif len(args) == 6:
      y = fun(args[0], args[1], args[2], args[3], args[4], args[5])
   elif len(args) == 7:
      y = fun(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
   elif len(args) == 8:
      y = fun(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])
   else:
      raise ValueError("Illegal number of arguments")
   if y != None:
      return y

def gprint(*args):
   isConsoleValid()
   do(_c.print, args)

def gprintln(*args):
   isConsoleValid()
   do(_c.println, args)

def clear():
   isConsoleValid()
   _c.clear()

def getString():
   isConsoleValid()
   return _c.readLine()

def getFloat():
   isConsoleValid()
   return _c.getDouble()

def getInt():
   isConsoleValid()
   return _c.getInt()

def getKeyCode():
   isConsoleValid()
   return _c.getKeyCode()

def getKeyCodeWait():
   isConsoleValid()
   return _c.getKeyCodeWait()

def getKey():
   isConsoleValid()
   key = _c.getKeyInt()
   if key > 255:
      return ""
   else:    
      return str(chr(key))

def getKeyWait():
   isConsoleValid()
   key = _c.getKeyWaitInt()
   if key > 255:
      return ""
   else:    
      return str(chr(key))

def getModifiers():
   isConsoleValid()
   return _c.getLastModifiers()

def getModifiersText():
   isConsoleValid()
   return _c.getLastModifiersText()

def hide():
   isConsoleValid()
   _c.hide()

def dispose():
   isConsoleValid()
   _c.dispose()

def isDisposed():
   isConsoleValid()
   return _c.isDisposed()

def kbhit():
   isConsoleValid()
   return _c.kbhit()

def setTitle(title):
   isConsoleValid()
   _c.setTitle(title)

def show():
   isConsoleValid()
   _c.show()

def showHorizontalScrollBar(b):
   isConsoleValid()
   _c.showHorizontalScrollBar(b)

def showVerticalScrollBar(b):
   isConsoleValid()
   _c.showVerticalScrollBar(b)

def delay(time):
   isConsoleValid()
   _c.delay(time)

def addExitListener(exitListener):
   isConsoleValid()
   _c.addExitListener(exitListener)