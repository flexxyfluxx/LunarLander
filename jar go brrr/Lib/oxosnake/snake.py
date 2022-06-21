# snake.py
# Simulation version
# Version 1.02 - June 26, 2018

'''
   Differences to real mode:
     - dim will not change brightness (always dim = 1)
     - reduce brightness factor divided by 10
'''

from utils import Vector
import time
from random import randint
from java.lang import RuntimeException
from oxosnake import _sim

_pList = []
def getRandomPos():
    global _pList
    if len(_pList) == 0:
        _pList = [n for n in range(64)]
    r = randint(0, len(_pList) - 1)    
    m = _pList[r]
    del _pList[r]
    return m % 8, m // 8

def inTouch(*args):
    s1 = args[0]
    s2 = args[1]
    if not (s1._isVisible and s2._isVisible):
        return False
    it1 = s1._items    
    it2 = s2._items
    for v in it1:
        for w in it2:
            if v == w:
                return True
    return False

class Snake:
    _directions = (Vector(0, -1), Vector(1, -1), Vector(1, 0), Vector(1, 1), 
                  Vector(0, 1), Vector(-1, 1), Vector(-1, 0), Vector(-1, -1))
    
    _params = ('size', 'headColor', 'tailColor', 'traceColor', 'bgColor', 'pos', 'heading', 
               'hidden', 'speed', 'penDown', 'name', 'dim')
    
    _snakes = []  # last snake is draw last (on top of others)
    _buf = [[0 for k in range(8)] for i in range(8)]     
    _background = [[-1 for k in range(8)] for i in range(8)]
    _dimFactor = 1
    _penColor = (0, 0, 255)
    _bgColor = (0, 0, 0)
    _repaintEnabled = True

    
    def __init__(self, **kwargs):
        # --------- Defaults -----------
        self._name = "Monty"
        self._size = 4
        self.setHeading(0)
        headPos = Vector(1, 4)
        speed = 50
        self._headColor = (255, 0, 0)
        self._tailColor = (0, 200, 0)
        self._penDown = False
        self._isVisible = True
       # --------- End of defaults -----------
        self._trace = []
        for key in kwargs:
            if key not in Snake._params:
                print("Illegal named parameter '" + key + "' ignored")
            if key == 'name':
                self._name = kwargs[key]
            if key == 'size':
                self._size = max(1, kwargs[key])
            elif key == 'headColor':
                self._headColor = kwargs[key]
            elif key == 'tailColor':
                self._tailColor = kwargs[key]
            elif key == 'bgColor':
                Snake._bgColor = kwargs[key]
            elif key == 'traceColor':
                Snake._penColor = kwargs[key]
            elif key == 'pos':
                headPos = Vector(kwargs[key])
            elif key == 'heading':
                self.setHeading(kwargs[key])
            elif key == 'speed':
                speed = min(max(1, kwargs[key]), 100)
            elif key == 'hidden':
                self._isVisible = not kwargs[key]
            elif key == 'penDown':
                self._penDown = kwargs[key]
            elif key == 'dim':
                Snake._dimFactor = max(1, kwargs[key])
                print("dim parameter has no effect in simulation mode.")
        self.setSpeed(speed)
        self._items = [0] * self._size
        for i in range(self._size):
            self._items[i] = headPos.add(self._dirVec.mult(-i))
        Snake._snakes.append(self)    
        Snake._repaint() 
        
    def setSpeed(self, speed):
        if speed < 100:
            self._delay = 1 - speed * 0.01
        else:
            self._delay = 0.005
        
    def spot(self, *args):
        x = getX()
        y = getY()
        self.dot(x, y, *args)
    
    def dot(self, x, y, *args):
        if len(args) == 1:
            color = args[0]
        elif len(args) == 3:
            color = (args[0], args[1], args[2])
        else:
            return
        if 0 <= x < 8 and 0 <= y < 8:
            Snake._background[x][y] = color
            Snake._repaint()    

    def dim(self, dimFactor):
        print("dim() has no effect in simulation mode.")
        Snake._dimFactor = max(1, dimFactor)
        Snake._repaint()
        
    def forward(self, *args):
        Snake._setOnTop(self)
        if len(args) == 0:
            self._oneStep(True)
        else:
            steps = args[0]
            if not self._repaintEnabled and self._delay != None: 
                time.sleep(self._delay)
            for _ in range(steps):
                self._oneStep(self._repaintEnabled)
    
    def _oneStep(self, wait):        
        if self._delay != None and wait:
            time.sleep(self._delay)
        nextHead = self._items[0].add(self._dirVec)
        if self._penDown:
            index = self._indexOf(nextHead)
            if index != -1:
                del self._trace[index]
            if Snake._posInPlayground(nextHead):
                self._trace.append((nextHead, self._penColor))
        self._items = [nextHead] + self._items[:-1]    
        Snake._repaint()

    def setName(self, name):
            self._name = name

    def getName(self):
            return self._name
          
    def left(self, angle):
        if angle < 0:
            self.right(-angle)
            return
        self._dir -= int(angle)
        self._dir = self._dir % 360
        self._dirVec = Snake._toDirVec(self._dir)
        Snake._setOnTop(self)

    def right(self, angle):
        if angle < 0:
            self.left(-angle)
            return
        self._dir += int(angle)
        self._dir = self._dir % 360
        self._dirVec = Snake._toDirVec(self._dir)
        Snake._setOnTop(self)
  
    def getX(self):
        return self._items[0][0]

    def getY(self):
        return self._items[0][1]
    
    def setX(self, x):
        self.setPos(x, self.getY())

    def setY(self, y):
        self.setPos(self.getX(), y)
    
    def setHeading(self, dir):
        self._dir = int(dir) % 360
        self._dirVec = Snake._toDirVec(self._dir)

    def getHeading(self):
        return self._dir
        
    def penDown(self):
        head = self._items[0]
        index = self._indexOf(head)
        if index != -1:
            del self._trace[index]
        if Snake._posInPlayground(head):    
            self._trace.append((head, Snake._penColor))
        self._penDown = True

    def penUp(self):
        self._penDown = False
        
    def clean(self):
        self._trace = []
        if self._penDown:
            pos = self._items[0]
            if Snake._posInPlayground(pos):
                self._trace.append((pos, Snake._penColor))
        Snake._repaint()
        
    def setHeadColor(self, *args):
        if len(args) == 3:
            self._headColor = (args[0], args[1], args[2])
        else:
            self._headColor = args[0][:] 
        Snake._repaint()
        
    def setTailColor(self, *args):
        if len(args) == 3:
            self._tailColor = (args[0], args[1], args[2])
        else:
            self._tailColor = args[0][:] 
        Snake._repaint()

    def setPenColor(self, *args):
        if len(args) == 3:
            Snake._penColor = (args[0], args[1], args[2])
        else:
            Snake._penColor = args[0][:] 
        Snake._repaint()

    def shortenTail(self):
        if self._size == 1:
            return
        self._items.pop()
        self._size -= 1
        Snake._repaint()
 
    def growTail(self):
        # only visible at next forward
        self._items.append(Vector(10, 10)) #outside
        self._size += 1
        
    def getSize(self):
        return self._size    
    
    def intersect(self):
        for i in range(1, self._size):
            if self._items[0][0] == self._items[i][0] and self._items[0][1] == self._items[i][1]:
               return True
        return False
    
    def inPlayground(self):
        for item in self._items:
            if Snake._posInPlayground(item):
                return True
        return False
    
    def headInPlayground(self):
        return Snake._posInPlayground(self._items[0])

    def show(self):
        self._isVisible = True
        Snake._setOnTop(self)
        Snake._repaint()

    def hide(self):
        self._isVisible = False
        Snake._repaint()

    def hidden(self):
        return not self._isVisible
        
    def setPos(self, *args):
        if len(args) == 2:
            pos = Vector(args[0], args[1])
        else: 
            pos = Vector(args[0])
        displacement = pos.sub(self._items[0])
        for i in range(len(self._items)):
            self._items[i] = self._items[i].add(displacement)
        if self._penDown:
            self._trace.append((self._items[0], Snake._penColor))
        Snake._setOnTop(self)
        Snake._repaint()
        
    def getPos(self):
        return tuple(self._items[0])
 
    def setBgColor(self, *args):
        if len(args) == 3:
            Snake._bgColor = (args[0], args[1], args[2])
        else:
            Snake._bgColor = args[0][:] 
        Snake._repaint()    

  
    @staticmethod
    def enableRepaint(enable):
        Snake._repaintEnabled = enable            
        
    @staticmethod        
    def repaint():
        time.sleep(0.01) # let the process yield, otherwise watchdog is complaining
        Snake._clear(Snake._bgColor)    
        for i in range(8):
            for k in range(8):
                c = Snake._background[i][k]
                if c != -1:
                    Snake._dot(i, k, c)
        for snake in Snake._snakes:
            for item in snake._trace:
                pos = item[0]
                color = item[1]
                Snake._dot(pos[0], pos[1], color)
            if snake._isVisible:    
                for i in range(snake._size - 1, -1, -1):
                    if i == 0:
                        Snake._dot(snake._items[i][0], snake._items[i][1], snake._headColor)
                    else:
                        Snake._dot(snake._items[i][0], snake._items[i][1], snake._tailColor)
        for i in range(0, 8):
            for k in range(0, 8):
                index = 8 * i + k + 1
                color = makeColor(Snake._buf[i][k])
                _sim.set(index, color) 

    @staticmethod
    def dispose():
        _cList = None
        _pList = None
        Snake._buf = None
        Snake._background = None

# ------------ private methods ------------------      
    def _indexOf(self, vector):
        for i in range(len(self._trace)):
            if self._trace[i][0] == vector:
                return i
        return -1    

    @staticmethod
    def _posInPlayground(vector):
        if 0 <= vector[0] < 8 and 0 <= vector[1] < 8:
            return True
        return False
    
    @staticmethod
    def _dot(x, y, c):
        Snake._toBuf(x, y, Snake._toColorInt(c))

    @staticmethod
    def _toBuf(x, y, c):
        if 0 <= x < 8 and 0 <= y < 8:
            Snake._buf[y][x] = c

    @staticmethod
    def _toColorInt(c):
        if type(c) in [list, tuple] and len(c) == 3:
            return (c[0] << 16) + (c[1] << 8) + c[2]
        return c

    @staticmethod
    def _clear(c):
        for i in range(0, 8):
            for k in range(0, 8):
                Snake._buf[i][k] = Snake._toColorInt(c)
   
    @staticmethod
    def _repaint():
        if _sim.isDisposed():
            raise RuntimeException("Java frame disposed") 
        if Snake._repaintEnabled:
            Snake.repaint()

    @staticmethod        
    def _toDirVec(a):
        a += 22
        a = a // 45
        if a == 8:
            a = 0
        return Snake._directions[a]
    
    @staticmethod
    def _setOnTop(snake):
        # move snake at end of list (if not yet there)
        if Snake._snakes[-1] != snake:
            Snake._snakes.remove(snake)
            Snake._snakes.append(snake)
                                    
# ------------ global wrapper -------------------      
def _check():
    if _snake == None:
        print("Call makeSnake() to use the snake")
        raise RuntimeException("Java frame disposed") 
    if _sim.isDisposed():
        raise RuntimeException("Java frame disposed") 

def makeSnake(**kwargs):
    global _snake
    _snake = Snake(**kwargs)

def forward(*args):
    _check()
    _snake.forward(*args)

def left(angle):
    _check()
    _snake.left(angle)

def right(angle):
    _check()
    _snake.right(angle)

def dim(dimFactor):
    _check()
    _snake.dim(dimFactor)

def getName():
    _check()
    return _snake.getName()

def setName(name):
    _check()
    _snake.setName(name)

def setSpeed(speed):
    _check()
    _snake.setSpeed(speed)
    
def setBgColor(*args):
    _check()
    _snake.setBgColor(*args)

def getX():
    _check()
    return _snake.getX()

def getY():
    _check()
    return _snake.getY()

def getPos():
    _check()
    return _snake.getPos()
    
def setX(x):
    _check()
    _snake.setX(x)

def setY(y):
    _check()
    _snake.setY(y)

def getPos():
    _check()
    return _snake.getPos()

def setPos(*args):
    _check()
    return _snake.setPos(*args)

def setHeading(dir):
    _check()
    _snake.setHeading(dir)

def getHeading():
    _check()
    return _snake.getHeading()
    
def heading(*args):
    _check()
    return _snake.heading(*args)

def penDown():
    _check()
    _snake.penDown()
    
def penUp():
    _check()
    _snake.penUp()

def clean():
    _check()
    _snake.clean()

def getSize():
    _check()
    _snake.getSize()
                
def setHeadColor(*args):
    _check()
    _snake.setHeadColor(*args)
            
def setTailColor(*args):
    _check()
    _snake.setTailColor(*args)

def setPenColor(*args):
    _check()
    _snake.setPenColor(*args)
        
def shortenTail():
    _check()
    _snake.shortenTail()

def growTail():
    _check()
    _snake.growTail()

def intersect():
    _check()
    return _snake.intersect()

def inPlayground():
    _check()
    return _snake.inPlayground()
    
def headInPlayground():
    _check()
    return _snake.headInPlayground()

def show():
    _check()
    _snake.show()
    
def hide():
    _check()
    _snake.hide()

def hidden():
    _check()
    return _snake.hidden()

def spot(*args):
    _check()
    _snake.spot(*args)

def dot(x, y, *args):
    _check()
    _snake.dot(x, y, *args)

def enableRepaint(enable):
    Snake.enableRepaint(enable)

def repaint():
    Snake.repaint()

def sleep(t):
    if _sim.isDisposed():
        raise RuntimeException("Java frame disposed") 
    time.sleep(t)
    
_snake = None
