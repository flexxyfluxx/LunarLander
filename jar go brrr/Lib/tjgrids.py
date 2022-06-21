#
#  This module provides a playground-grid with a small figurine in it
#  like e.g. a PacMan or a Turtle. The figure can move around inside
#  the grid unless its path is blocked by black cells.
#
#  Example:
#  ------------------------------------------------------------------
#
#  from tjgrids import *
#  def onStep():
#      if getCell() == 4:
#          print "Goal reached!"
#          stop()   
#      elif canGoForward():
#          forward()
#      else:
#          right()
#
#  setCell(5, 6, 4)
#  start(onStep)
#
#  ------------------------------------------------------------------
#
#  (c) 2013-2017, T. Kohn
#  jython.tobiaskohn.ch
#
#  Last updated: JUNE-18-2017
#
from tigerjython.utils import JythonGrid, JythonGridWindow, GridFigure
from time import sleep

_mainfigure = None
_maingrid = None
__mainwindow = None
__automode = False
__std_waittime = 0.125

_clones = []
_dying = []

_on_key_pressed = None
_on_mouse_pressed = None
_on_figure_moved = None

class Color:
    BLOCK = 0x0001
    RED = 0x0002
    ORANGE = 0x0003
    YELLOW = 0x0004
    GREEN_YELLOW = 0x0005
    GREEN = 0x0006
    CYAN = 0x0007
    BLUE = 0x0008
    MAGENTA = 0x0009
    BLACK = 0x000A
    DARK_GRAY = 0x000B
    LIGHT_GRAY = 0x000C
    WHITE = 0x000D
    SALMON = 0x000E
    BROWN = 0x000F
    CHOCOLATE = 0x0010
    MAROON = 0x0011
    GOLDEN_ROD = 0x0012
    GOLD = 0x0013
    OLIVE = 0x0014
    DARK_GREEN = 0x0015
    SEA_GREEN = 0x0016
    DARK_CYAN = 0x0017
    ROYAL_BLUE = 0x0018
    NAVY = 0x0019
    PURPLE = 0x001A
    INDIGO = 0x001B
    
    DOT = 0x0080
    EMPTY = 0x0000

def getFigure():
    global _mainfigure
    return _mainfigure

def getGrid():
    global _maingrid
    return _maingrid

def getGridWindow():
    global __mainwindow
    return __mainwindow

# Create the figure, window etc.
def __createGrid(showWindow = True):
    """Create the main window with the grid inside it."""
    global _maingrid, __mainwindow
    __mainwindow = JythonGridWindow()
    _maingrid = __mainwindow.grid()
    _install_handlers()
    if showWindow:
        __mainwindow.show()
    
def __createFigure():
    """Create a figure which will move around within the grid."""
    global _mainfigure, _maingrid
    if _maingrid == None:
        __createGrid()
    _mainfigure = GridFigure(_maingrid)
    _clones.append(_mainfigure)
    _maingrid.addFigure(_mainfigure)

def _cloneFigure():
    global _maingrid
    if _mainfigure != None:
        f = _mainfigure.clone()
        _clones.append(f)
        _maingrid.addFigure(f)
        return f
    else:
        return None
    
def _removeFigure(figure):
    if figure in _clones:
        figure.hide()
        _clones.remove(figure)
        _maingrid.removeFigure(figure)
        if figure == _mainfigure:
            _switchToClone(0)

def _switchToClone(index):
    global _mainfigure
    if type(index) is int and 0 <= index < len(_clones):
        _mainfigure = _clones[index]
    elif index in _clones:
        _mainfigure = index
    return _mainfigure
                    
def makeGrid(*args):
    global _mainfigure, _maingrid, __mainwindow
    __createGrid(False)
    if len(args) == 1:
        _maingrid.loadFromFile(args[0])
        fig = _maingrid.getFirstFigure()
        if fig != None:
            _clones.append(fig)
            _mainfigure = fig
    elif len(args) == 2:
        _maingrid.setSize(args[0], args[1])
    elif len(args) == 3:
        _maingrid.setSize(args[0], args[1], args[2])
    __mainwindow.show()
    
def makeTurtle(*args):
    makeGrid(*args)
    setShape("turtle")
    __wait()
    
def saveToFile(filename):
    global _maingrid
    if _maingrid != None:
        _maingrid.saveToFile(filename)
    
def setBackground(index):
    global _maingrid
    if _maingrid is None:
        makeGrid()
    _maingrid.setBaseColor(index)
    
def fillWithFodder():
    if _maingrid is None:
        makeGrid()
    _maingrid.addFodderToAll(0)
    
# Move the figure. If necessary, create it first.
def __wait():
    global __automode, __std_waittime
    if not __automode:
        sleep(__std_waittime)

def forward(s = 1):
    global _mainfigure, __automode
    if _mainfigure == None:
        __createFigure()
    if _mainfigure != None:
        if not __automode:
            for i in xrange(s):
                _mainfigure.forward(1)
                __wait()
        else:
            _mainfigure.forward(s)

def back(s = 0):
    global _mainfigure
    if _mainfigure == None:
        __createFigure()
    if _mainfigure != None:
        _mainfigure.back(s)
        __wait()
        
def undo():
    _mainfigure.undo()
traceBack = undo

def left(*args):
    global _mainfigure
    if _mainfigure == None:
        __createFigure()
    if _mainfigure != None:
        if len(args) == 1:
            angle = int((args[0] + 45) / 90)
            for i in range(angle):
                _mainfigure.turnLeft()
        else:
            _mainfigure.turnLeft()
        __wait()

def right(*args):
    global _mainfigure
    if _mainfigure == None:
        __createFigure()
    if _mainfigure != None:
        if len(args) == 1:
            angle = int((args[0] + 45) / 90)
            for i in range(angle):
                _mainfigure.turnRight()
        else:
            _mainfigure.turnRight()
        __wait()

def moveTo(x, y):
    global _mainfigure
    if _mainfigure == None:
        __createFigure()
    if _mainfigure != None:
        _mainfigure.moveTo(x, y)
        
def setPos(x, y):
    global _mainfigure
    if _mainfigure == None:
        __createFigure()
    if _mainfigure != None:
        _mainfigure.setPos(x, y)
        
def getX():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.posX()
    else:
        return -1
        
def getY():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.posY()
    else:
        return -1
        
def goForward():
    forward(1)
    
def goLeft():
    left()
    forward(1)
    
def goRight():
    right()
    forward(1)
        
# Receive the current values of cells around the figure
# or set the value of the cell below the figure.
def getCell(*args):
    global _mainfigure, _maingrid
    if len(args) == 0:
        if _mainfigure != None:
            return _mainfigure.getCell()
        else:
            return 0
    elif len(args) == 2:
        if _maingrid != None:
            return _maingrid.getCellValue(args[0], args[1])
        else:
            return 0
    else:
        return 0
        
def isCell(*args):
    if len(args) == 1:
        return getCell() == args[0]
    if len(args) == 3:
        return getCell(args[0], args[1]) == args[2]
    return 0
        
def setCell(*args):
    global _mainfigure, _maingrid
    if len(args) == 0 or len(args) == 1:
        if len(args) == 1:
            value = args[0]
        else:
            value = 1
        if _mainfigure == None:
            __createFigure()
        if _mainfigure != None:
            _mainfigure.setCell(value)
    elif len(args) == 2 or len(args) == 3:
        if len(args) == 3:
            value = args[2]
        else:
            value = 1
        if _maingrid == None:
            __createGrid()
        if _maingrid != None:
            _maingrid.setCellValue(args[0], args[1], value)

def toggleCell(*args):
    global _mainfigure
    if len(args) == 0:
        if _mainfigure == None:
            __createFigure()
        if _mainfigure != None:
            _mainfigure.toggleCell()
    elif len(args) == 2:
        if _maingrid == None:
            __createGrid()
        if _maingrid != None:
            _maingrid.toggleCellValue(args[0], args[1])
        
def getCellForward():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.getCellForward()
    else:
        return 0

def getCellLeft():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.getCellLeft()
    else:
        return 0

def getCellRight():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.getCellRight()
    else:
        return 0

def getCellBack():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.getCellBack()
    else:
        return 0
        
def canGo(*args):
    global _mainfigure
    if _mainfigure != None:
        if len(args) == 0:
            return _mainfigure.canGo()
        elif len(args) == 2:
            return _mainfigure.canGo(args[0], args[1])
    else:
        return False
        
def canGoForward():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.canGoForward()
    else:
        return False
    
def canGoLeft():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.canGoLeft()
    else:
        return False
    
def canGoRight():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.canGoRight()
    else:
        return False
    
def canGoBack():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.canGoBack()
    else:
        return False

def hasFodder():
    return _mainfigure.hasFodder()

def hasFodderForward():
    return _mainfigure.hasFodderForward()

def hasFodderLeft():
    return _mainfigure.hasFodderLeft()

def hasFodderRight():
    return _mainfigure.hasFodderRight()

def hasFodderBack():
    return _mainfigure.hasFodderBack()

def canGoAnywhere():
    global _mainfigure
    if _mainfigure != None:
        return _mainfigure.canGoAnywhere()
    else:
        return False

# Show or hide the figure.
def show():
    global _mainfigure
    if _mainfigure == None:
        __createFigure()
    if _mainfigure != None:
        _mainfigure.show()
        
def hide():
    global _mainfigure
    if _mainfigure != None:
        _mainfigure.hide()
        
def setShape(s, clr = None):
    global _mainfigure, _maingrid
    if _mainfigure == None:
        __createFigure()
    if _mainfigure != None:
        _mainfigure.setShape(s)
        if clr is not None:
            c = _maingrid.indexToColor(clr)
            _mainfigure.setColor(c)

def clone():
    return _cloneFigure()

def showPath():
    if _mainfigure != None:
        _mainfigure.showPath()
        
# Use "start(onStep)" to start a simple animation where
# the figure can act, based upon the given method.
__canGo = True
__waittime = 0.3

def speed(value):
    global __waittime, __std_waittime
    if 1 <= value <= 20:
        __waittime = int(40 / value) / 20
        __std_waittime = __waittime
    elif value in [0, -1]:
        __waittime = 0
        __std_waittime = 0

def start(onStep = None):
    global __canGo, _maingrid, __mainwindow, __automode, _dying
    if _maingrid == None:
        __createGrid()
    if onStep != None and _maingrid != None:
        __canGo = True
        __automode = True
        while __canGo:
            if not _maingrid.isPaused():
                if len(_clones) > 1:
                    for C in _clones:
                        _switchToClone(C)
                        onStep()
                    _switchToClone(0)
                elif canGoAnywhere():
                    onStep()
                else:
                    break
                if len(_dying) > 0:
                    for f in _dying:
                        if len(_clones) > 0:
                            _removeFigure(f)
                        else:
                            stop()
                    _dying = []
            if not __mainwindow.visible():
                break
            sleep(__waittime)
    __automode = False

def startOnEnter(onStep = None):
    global _maingrid, _mainfigure
    if _maingrid == None:
        __createGrid()
    if _mainfigure == None:
        __createFigure()
    if _maingrid != None and onStep != None:
        _maingrid.waitForEnter()
        start(onStep)
            
def stop():
    global __canGo, __automode
    __canGo = False
    __automode = False
    
def die():
    if __automode and _mainfigure not in _dying:
        _dying.append(_mainfigure)

def killAllOthers():
    global _dying
    if __automode and len(_clones) > 0:
        for f in _clones:
            if f != _mainfigure:
                _dying.append(f)

def mark():
    return _mainfigure.mark()

def markLeft():
    return _mainfigure.markLeft()

def markRight():
    return _mainfigure.markRight()
    
def returnToMark():
    return _mainfigure.returnToMark()

def eat():
    _mainfigure.eat()
    
def autoEat():
    _mainfigure.setAutoEat(True)

# Events

def setOnClick(handler):
    global _maingrid
    if _maingrid == None:
        __createGrid
    if _maingrid != None:
        _maingrid.setOnMouseClick(handler)

def setOnKey(handler):
    global _maingrid
    if _maingrid == None:
        __createGrid
    if _maingrid != None:
        _maingrid.setOnKeyTyped(handler)

def setOnMoved(handler):
    global _maingrid
    if _maingrid == None:
        __createGrid
    if _maingrid != None:
        _maingrid.setOnFigureMoved(handler)

def _install_handlers():
    global _on_key_pressed
    global _on_mouse_pressed
    global _on_figure_moved
    if _on_key_pressed != None:
        setOnKey(_on_key_pressed)
    if _on_mouse_pressed != None:
        setOnClick(_on_mouse_pressed)
    if _on_figure_moved != None:
        setOnMoved(_on_figure_moved)
        
def onClick(f):
    global _maingrid
    global _on_mouse_pressed
    if _maingrid == None:
        _on_mouse_pressed = f
    else:
        setOnClick(f)
    return f
    
def onKey(f):
    global _maingrid
    global _on_key_pressed
    if _maingrid == None:
        _on_key_pressed = f
    else:
        setOnKey(f)
    return f
    
def onMoved(f):
    global _maingrid
    global _on_figure_moved
    if _maingrid == None:
        _on_figure_moved = f
    else:
        setOnMoved(f)
    return f