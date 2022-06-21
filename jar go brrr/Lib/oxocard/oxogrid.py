# oxogrid.py
# Simulation version
# Version 1.02 - Feb 19, 2019

from java.lang import RuntimeException
import time
from random import randint
from math import sin, cos, radians, pi
from pixfont import font, font3x5
from globals import *
from oxocard import _sim

_pList = []
def getRandomPos():
    global _pList
    if len(_pList) == 0:
        _pList = [n for n in range(64)]
    r = randint(0, len(_pList) - 1)    
    m = _pList[r]
    del _pList[r]
    return m % 8, m // 8

# ---------------------- class OxoGrid -----------------------------------
class OxoGrid:
    _isRepaintEnabled = True
    _instance = None
    
    def __init__(self):
        self._dimFactor = 1
        self._w = 24
        self._h = 24
        self._origin = [8, 8] # default position   
        self._buf = [[0 for k in range(self._w)] for i in range(self._h)]     
        OxoGrid._instance = self

    def clear(self, *args):
        if len(args) == 0:
            self.clear(0)
            return
        for i in range(0, self._h):
            for k in range(0, self._w):
                self._buf[i][k] = self._toColorInt(args[0])
        if OxoGrid._isRepaintEnabled:
            self._repaint()
            
    def clearWindow(self, *args):
        if len(args) == 0:
            self.clearWindow(0)
            return
        for i in range(0, 8):
            for k in range(0, 8):
                m = i + self._origin[1]
                n = k + self._origin[0]
                self._buf[m][n] = self._toColorInt(args[0])
        if OxoGrid._isRepaintEnabled:
            self._repaint()
            
    def clearFrame(self, frameNumber, *args):
        if len(args) == 0:
            self.clearFrame(frameNumber, 0)
            return
        for i in range(0, 8):
            for k in range(0, 8):
                m = i + self._frameToOrigin(frameNumber)[1]
                n = k + self._frameToOrigin(frameNumber)[0]
                self._buf[m][n] = self._toColorInt(args[0])
        if OxoGrid._isRepaintEnabled:
            self._repaint()

    def setOrigin(self, *args):
        self._origin = self._toPoint(*args)
        if OxoGrid._isRepaintEnabled:
            self._repaint()

    def getOrigin(self, *args):
        return self._origin[:]

    def setFrame(self, frameNumber):
        self._origin = self._frameToOrigin(frameNumber)
        if OxoGrid._isRepaintEnabled:
            self._repaint()
        
    def dim(self, factor):
        self._dimFactor = factor
        if OxoGrid._isRepaintEnabled:
            self._repaint()

    def translate(self, vector):
        tmp = [[0 for k in range(self._w)] for i in range(self._h)]
        for i in range(self._h):
            for k in range(self._w):
                x = k - vector[0]
                y = i - vector[1]
                if 0 <= x < self._w and 0 <= y < self._h:
                    tmp[i][k] = self._buf[y][x]
                else:
                    tmp[i][k] = 0
        self._buf = tmp
        if OxoGrid._isRepaintEnabled:
            self._repaint()

    def rotate(self, centerx, centery, angle):
        centerx += self._origin[0]
        centery += self._origin[1]
        angle= radians(-angle)
        tmp = [[0 for k in range(self._w)] for i in range(self._h)]
        for i in range(self._h):
            for k in range(self._w):
                x = k - centerx
                y = i - centery
                x1 = int(round(cos(angle) * x - sin(angle) * y) + centerx)
                y1 = int(round(sin(angle) * x + cos(angle) * y) + centery)
                if 0 <= x1 < self._w and 0 <= y1 < self._h:
                    tmp[i][k] = self._buf[y1][x1]
                else:
                    tmp[i][k] = 0
        self._buf = tmp
        if OxoGrid._isRepaintEnabled:
            self._repaint()

    @staticmethod
    def enableRepaint(enable):
        OxoGrid._isRepaintEnabled = enable

    @staticmethod
    def repaint():
        if OxoGrid._instance != None:
            OxoGrid._instance._repaint()

    def _repaint(self):
        time.sleep(0.01) # let the process yield, otherwise watchdog is complaining
        for i in range(0, 8):
            for k in range(0, 8):
                m = i + self._origin[1]
                n = k + self._origin[0]
                index = 8 * i + k + 1
                if 0 <= m < self._h and 0 <= n < self._w:
                    color = makeColor(self._buf[m][n])
                    _sim.set(index, color)
                else:
                    _set(index, 0) 

    def dot(self, x, y, c):
        self._toBuf(x, y, self._toColorInt(c))
        if OxoGrid._isRepaintEnabled:
            self._repaint()
            
    def getColor(self, *args):
        return intToRGB(self.getColorInt(*args))
    
    def getColorInt(self, *args):
        pt = self._toPoint(*args)
        if 0 <= pt[0] < self._w and 0 <= pt[1] < self._h:
            i = pt[0] + self._origin[0]
            k = pt[1] + self._origin[1]
            return self._buf[k][i]
        return 0        
    
    def line(self, x, y, dir, length, c):
        if length <= 0:
            return
        enabled =  OxoGrid._isRepaintEnabled
        OxoGrid._isRepaintEnabled = False
        dir = dir % 8
        count = 0
        while True:
            self.dot(x, y, c)
            count += 1
            if count == length:
                break
            if dir == 0:
                x += 1
            elif dir == 1:
                x += 1
                y -= 1
            elif dir == 2:
                y -= 1
            elif dir == 3:
                x -= 1
                y -= 1
            elif dir == 4:
                x -= 1
            elif dir == 5:
                x -= 1
                y += 1
            elif dir == 6:
                y += 1
            elif dir == 7:
                x += 1
                y += 1
        OxoGrid._isRepaintEnabled = enabled
        if enabled:        
            self._repaint()

    def arrow(self, x, y, dir, length, c):
        if length <= 0 or dir < 0:
            return
        enabled =  OxoGrid._isRepaintEnabled
        OxoGrid._isRepaintEnabled = False
        dir = dir % 8
        self.line(x, y, dir, length, c)
        a = pi / 4 * dir
        if dir % 2 == 0:
            r = length - 1
        else:
            r = 1.41 * (length - 1)
        x1 = int(round(x + r * cos(-a)))
        y1 = int(round(y + r * sin(-a)))
        if dir == 0:
            p1 = x1 - 1, y - 1
            p2 = x1 - 1, y + 1
        elif dir == 1:
            p1 = x1 - 1, y1
            p2 = x1, y1 + 1
        elif dir == 2:
            p1 = x1 - 1, y1 + 1
            p2 = x1 + 1, y1 + 1
        elif dir == 3:
            p1 = x1, y1 + 1
            p2 = x1 + 1, y1 
        elif dir == 4:
            p1 = x1 + 1, y1 + 1
            p2 = x1 + 1, y1 - 1
        elif dir == 5:
            p1 = x1 + 1, y1
            p2 = x1, y1 - 1
        elif dir == 6:
            p1 = x1 + 1, y1 - 1
            p2 = x1 - 1, y1 - 1
        elif dir == 7:
            p1 = x1, y1 - 1
            p2 = x1 - 1, y1 
        self.dot(p1[0], p1[1], c)
        self.dot(p2[0], p2[1], c)        
        OxoGrid._isRepaintEnabled = enabled
        if enabled:        
            self._repaint()
        
    def rectangle(self, ulx, uly, w, h, c):
        c = self._toColorInt(c)
        for x in range(ulx, ulx + w):
            self._toBuf(x, uly, c)
            self._toBuf(x, uly + h - 1, c)
        for y in range(uly, uly + h):
            self._toBuf(ulx, y, c)
            self._toBuf(ulx + w - 1, y, c)
        if OxoGrid._isRepaintEnabled:
            self._repaint()

    def fillRectangle(self, ulx, uly, w, h, c):
        c = self._toColorInt(c)
        for y in range(uly, uly + h):
            for x in range(ulx, ulx + w):
                self._toBuf(x, y, c)
        if OxoGrid._isRepaintEnabled:
            self._repaint()

    def circle(self, xcenter, ycenter, r, c):
        d = -r
        x = r
        y = 0
        while True:
            for a in [-x, x]:
               for b in [-y, y]:
                    self._toBuf(a + xcenter, b + ycenter, self._toColorInt(c))
                    self._toBuf(b + xcenter, a + ycenter, self._toColorInt(c))
            d = d + 2 * y + 1
            y = y + 1
            if d > 0:
                d = d - 2 * x + 2
                x = x - 1
            if y > x:
                break
        if OxoGrid._isRepaintEnabled:
            self._repaint()
    
    def fillCircle(self, xcenter, ycenter, r, c):
        b = OxoGrid._isRepaintEnabled 
        OxoGrid._isRepaintEnabled = False
        for z in range(0, r + 1):
            self.circle(xcenter, ycenter, z, c)
        OxoGrid._isRepaintEnabled = b
        if OxoGrid._isRepaintEnabled:
            self._repaint()

    def image(self, matrix):
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                self._toBuf(x, y, self._toColorInt(matrix[y][x]))
        if OxoGrid._isRepaintEnabled:
            self._repaint()

    def getArray(self):
        buf = []
        for i in range(self._h):
           line = self._buf[i][:] 
           buf.append(line)
        return tuple(buf)
    
    def insertBigChar(self, char, charColor, bgColor):
        self.image(self._bigCharToMatrix(char, charColor, bgColor))


    def bigTextScroll(self, text, textColor = (255, 255, 255), bgColor = (0, 0, 0), speed = 8):
        self._textScroll(text, textColor, bgColor, speed, False)
        
    def smallTextScroll(self, text, textColor = (255, 255, 255), bgColor = (0, 0, 0), speed = 5):
        self._textScroll(text, textColor, bgColor, speed, True)
        
    def display(self, chars, textColor = (255, 255, 255), bgColor = (0, 0, 0)):
        self._insertSmallCharsWithSign(chars, textColor, bgColor)     

    # --------------- static methods ------------------    
    @staticmethod
    def _reduce(c, r):
        if c == 0:
            return 0
        blue = ((c & 255) + 1) // 2
        if blue > 0:
            blue =  max(1, int(blue / r + 0.5))
        green = (((c >> 8) & 255) + 1) // 2
        if green > 0:
            green = max(1, int(green / r + 0.5))
        red = (((c >> 16) & 255) + 1) // 2
        if red > 0:    
            red = max(1, int(red / r + 0.5))
        return (red << 16) + (green << 8) + blue

    def dispose(self):
        if OxoGrid._instance != None:
            self._buf = None
            OxoGrid._instance = None

    # --------------- private methods ------------------    
    def _toBuf(self, x, y, c):
        i = x + self._origin[0]
        k = y + self._origin[1]
        if 0 <= i < self._w and 0 <= k < self._h:
            self._buf[k][i] = c

    def _toColorInt(self, c):
        if type(c) in [list, tuple] and len(c) == 3:
            return (c[0] << 16) + (c[1] << 8) + c[2]
        return c

    def _toPoint(self, *args):
        if len(args) == 2:
            return (args[0], args[1])
        return args[:]
    
    def _frameToOrigin(self, frameNumber):
        x = (frameNumber % 3) * 8
        y = (frameNumber // 3) * 8
        return (x, y)
    
    def _bigCharToMatrix(self, char, charColor, bgColor):                    
        if type(char) == int:
            char = str(char)
        matrix = []
        a = font[ord(char) - 33]
        for i in range(8):
            hex = a[i]
            matrix.append(self._hexToLine(hex, charColor, bgColor))
        return matrix
 
    def _smallCharsToMatrix(self, chars, charColor, bgColor):
        chars = str(chars.upper())
        a = [0] * 2
        n = min(len(chars), 2)
        for i in range(n):
            k = ord(chars[i]) - 32
            if k >= 0 and k < len(font3x5):
                a[i] = font3x5[k]
            else:
                a[i] = 0
                
        bgC = rgbToInt(bgColor)
        digit0 = self._toDigit(a[0], charColor, bgColor)
        digit1 = self._toDigit(a[1], charColor, bgColor)
        matrix = [[bgC for k in range(8)] for i in range(8)]
        for i in range(5):
            for k in range(3):
                matrix[i + 1][k] = digit0[i][k] 
                matrix[i + 1][k + 4] = digit1[i][k]
        return matrix

    def _textScroll(self, text, textColor, bgColor, speed, small):
        if len(text) == 0:
            return
        isRepaint = OxoGrid._isRepaintEnabled
        OxoGrid._isRepaintEnabled = True
        if len(text) == 1:
            if small:
                self.display(text, textColor, bgColor)
            else:
                self.insertBigChar(text, textColor, bgColor)
        elif len(text) == 2 and small:
            self.display(text, textColor, bgColor)
        else:
            self._scrollBuf = [None] * 8 # 8 lines with 16 columns
            speed = min(12, speed)
            speed = max(1, speed)
            dt = (10**((14 - speed) / 4)) / 1000
            if small:
                if len(text) % 2 == 1:
                    text = " " + text
                m1 = self._smallCharsToMatrix(text[0] + text[1], textColor, bgColor)
                m2 = self._smallCharsToMatrix(text[2] + text[3], textColor, bgColor)
            else:
                m1 = self._bigCharToMatrix(text[0], textColor, bgColor)
                m2 = self._bigCharToMatrix(text[1], textColor, bgColor)
            n = 1
            while True:
                for i in range(8):
                    self._scrollBuf[i] = m1[i] + m2[i]
                for _ in range(8):    
                    self._showScrollBuf()
                    time.sleep(dt)
                    self._shiftLeft()
                m1 = m2
                n += 1
                if small:    
                    if n == len(text) // 2:
                        break
                    m2 = self._smallCharsToMatrix(text[2 * n] + text[2 * n + 1], textColor, bgColor)
                else:
                    if n == len(text):
                        break
                    m2 = self._bigCharToMatrix(text[n], textColor, bgColor)

        OxoGrid._isRepaintEnabled = isRepaint
    
    def _toDigit(self, intCode, charColor, bgColor):
        digitList = [[bgColor for k in range(3)] for i in range(5)]
        mask = 1
        for i in range(5):
            for k in range(3):
                if mask & intCode != 0:
                    digitList[i][k] = charColor
                mask *= 2
        return digitList    
    
    def _hexToLine(self, hex, textColor, bgColor):
        line = [bgColor] * 8
        mask = 1
        for k in range(8):
            line[k] = textColor if ((hex & mask) != 0) else bgColor
            mask = 2 * mask
        return line

    def _hexToLine1(self, hex, textColor, bgColor):
        line = [bgColor] * 3
        mask = 4
        for k in range(3):
            line[k] = textColor if ((hex & mask) != 0) else bgColor
            mask = mask // 2
        return line

    def _shiftLeft(self):
        for i in range(8):  # rows
            a = self._scrollBuf[i][:]
            a =  a[1:] + [0]
            for k in range(16):
                self._scrollBuf[i][k] = a[k]

    def _showScrollBuf(self):
        matrix = [0] * 8
        for i in range(8):
            matrix[i] = self._scrollBuf[i][0:8]
        self.image(matrix)

    def _insertSmallCharsWithSign(self, chars, charColor, bgColor):
        sign = False
        if type(chars) == int and chars < 0:
            sign = True
            chars = -chars
        isEnabled = OxoGrid._isRepaintEnabled
        OxoGrid._isRepaintEnabled = False
        self.image(self._smallCharsToMatrix(str(chars), charColor, bgColor))
        if sign:
            self.line(0, 7, 0, 3, charColor)
        OxoGrid._isRepaintEnabled = isEnabled
        if OxoGrid._isRepaintEnabled:
            self._repaint()

# ------------ global wrapper -------------------      
_grid = OxoGrid()

def _check():
    if _sim.isDisposed():
        raise RuntimeException("Java frame disposed") 

def dot(x, y, color):
    _check()
    _grid.dot(x, y, color)

def dispose():
    _grid.dispose()

def clear(*args):
    _check()
    _grid.clear(*args)
    
def clearWindow(*args):
    _check()
    _grid.clearWindow(*args)
    
def clearFrame(frame, *args):
    _check()
    _grid.clearFrame(*args)
    
def setOrigin(*args):
    _check()
    _grid.setOrigin(*args)

def getOrigin():
    _check()
    return _grid.getOrigin()

def setFrame(frameNumber):
    _check()
    _grid.setFrame(frameNumber)

def dim(dimFactor):
    _check()
    _grid.dim(dimFactor)    

def getColor(*args):
    _check()
    return _grid.getColor(*args)    

def getColorInt(*args):
    _check()
    return _grid.getColorInt(*args)    

def line(x, y, dir, length, color):
    _check()
    _grid.line(x, y, dir, length, color)

def arrow(x, y, dir, length, color):
    _check()
    _grid.arrow(x, y, dir, length, color)

def rectangle(ulx, uly, w, h, color):
    _check()
    _grid.rectangle(ulx, uly, w, h, color)

def fillRectangle(ulx, uly, w, h, color):
    _check()
    _grid.fillRectangle(ulx, uly, w, h, color)

def circle(xcenter, ycenter, r, color):
    _check()
    _grid.circle(xcenter, ycenter, r, color)

def fillCircle(xcenter, ycenter, r, color):
    _check()
    _grid.fillCircle(xcenter, ycenter, r, color)

def image(matrix, *args):
    _check()
    _grid.image(matrix, *args)

def translate(vector):
    _check()
    _grid.translate(vector)

def rotate(centerx, centery, angle):   
    _check()
    _grid.rotate(centerx, centery, angle)

def insertBigChar(char, charColor = (255, 255, 255), bgColor = (0, 0, 0)):
    _check()
    _grid.insertBigChar(char, charColor, bgColor)
   
def display(chars, charColor = (255, 255, 255), bgColor = (0, 0, 0)):
    _check()
    _grid.display(chars, charColor, bgColor)     

def smallTextScroll(text, textColor = (255, 255, 255), bgColor = (0, 0, 0), speed = 5):
    _check()
    _grid.smallTextScroll(text, textColor, bgColor, speed)

def bigTextScroll(text, textColor = (255, 255, 255), bgColor = (0, 0, 0), speed = 8):
    _check()
    _grid.bigTextScroll(text, textColor, bgColor, speed)
    
def getArray():
    _check()
    return _grid.getArray()

def enableRepaint(enable):
    OxoGrid.enableRepaint(enable)

def repaint():
    OxoGrid.repaint()

