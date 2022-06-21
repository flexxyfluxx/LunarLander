# displayclass.py
# Version 1.7 - Sep 6, 2019

from microbit import _sim, _ledSize, pixfont, image
import time
from java.lang import RuntimeException
import thread
from java.lang import Thread
from java.lang.Thread import UncaughtExceptionHandler

class _ShowThread(Thread):
    def __init__(self, instance, iterable, loop, delay, clr):
        self.instance = instance
        self.iterable = iterable
        self.loop = loop
        self.delay = delay
        self.clr = clr
        
    def run(self):
        while True:
           self.instance._showIterable(self.iterable, self.loop, self.delay, self.clr)

class _ScrollThread(Thread):
    def __init__(self, instance, text, loop, delay, monospace):
        self.instance = instance
        self.text = text
        self.loop = loop
        self.delay = delay
        self.monospace = monospace
        
    def run(self):
        self.instance._scroll(self.text, self.loop, self.delay, self.monospace)

class _MyUncaughtExceptionHandler(UncaughtExceptionHandler):
    def uncaughtException(self, t, e):
        pass    

def _check():
    if _sim.isDisposed():
        raise RuntimeException("Java frame disposed") 

class Display:
    _isRepaintEnabled = True
    _pList = []

# --------------- public methods ----------------------------        
    def __init__(self, ledSize = 7):   # ctor
        self._ledSize = ledSize
        self._w = 15
        self._h = 15
        self._origin = [5, 5] # default position   
        self._buf = [[0 for k in range(self._w)] for i in range(self._h)]     

    def on(self):
        """Use on() to turn on the display."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def off(self):
        """Use off() to turn off the display (thus allowing you to re-use the GPIO pins associated with the display for other purposes)."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def is_on(self):
        """Returns True if the display is on, otherwise returns False."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def set_pixel(self, x, y, v):
        """Set the brightness of the LED at column x and row y to value, which has to be an integer between 0 and 9."""
        _check()
        self._toBuf(x, y, v)
        if Display._isRepaintEnabled:
            self.repaint()

    def clear(self, *args):
        """Set the brightness of all LEDs to 0 (off)."""
        _check()
        if len(args) == 0:
            self.clear(0)
            return
        for i in range(0, self._h):
            for k in range(0, self._w):
                self._buf[i][k] = self._toColorInt(args[0])
        if Display._isRepaintEnabled:
            self.repaint()
 
    def clearWindow(self, *args):
        _check()
        if len(args) == 0:
            self.clearWindow(0)
            return
        for i in range(0, 5):
            for k in range(0, 5):
                m = i + self._origin[1]
                n = k + self._origin[0]
                self._buf[m][n] = self._toColorInt(args[0])
        if Display._isRepaintEnabled:
            self.repaint()
            
    def clearFrame(self, frameNumber, *args):
        _check()
        if len(args) == 0:
            self.clearFrame(frameNumber, 0)
            return
        for i in range(0, 5):
            for k in range(0, 5):
                m = i + self._frameToOrigin(frameNumber)[1]
                n = k + self._frameToOrigin(frameNumber)[0]
                self._buf[m][n] = self._toColorInt(args[0])
        if Display._isRepaintEnabled:
            self.repaint()

    def setOrigin(self, *args):
        _check()
        self._origin = self._toPoint(*args)
        if Display._isRepaintEnabled:
            self.repaint()

    def getOrigin(self, *args):
        _check()
        return self._origin[:]

    def setFrame(self, frameNumber):
        _check()
        self._origin = self._frameToOrigin(frameNumber)
        if Display._isRepaintEnabled:
            self.repaint()

    def translate(self, vector):
        _check()
        tmp = [[0 for k in range(self._w)] for i in range(self._h)]
        for i in range(self._w):
            for k in range(self._h):
                x = k - vector[0]
                y = i - vector[1]
                if 0 <= x < self._w and 0 <= y < self._h:
                    tmp[i][k] = self._buf[y][x]
                else:
                    tmp[i][k] = 0
        self._buf = tmp
        if Display._isRepaintEnabled:
            self.repaint()

    def rotate(self, centerx, centery, angle):
        _check()
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
        if Display._isRepaintEnabled:
            self.repaint()

    def repaint(self):
        _check()
        for i in range(0, 5):
            for k in range(0, 5):
                m = i + self._origin[1]
                n = k + self._origin[0]
                if 0 <= m < self._h and 0 <= n < self._w:
                    _sim.setPixel(k, i, self._buf[m][n], _ledSize)
                else:
                   _sim.setPixel(k, i, 0, _ledSize)
            
    def show(self, *args, **kwargs):
        """Display images or letters from the iterable in sequence, with delay milliseconds between them."""
        _check()
        if len(args) == 0:
            return
        if isinstance(args[0], image.Image) and len(kwargs) == 0:
            self._showImage(args[0])
            return
        delay = 150
        wait = True
        loop = False
        clr = False
        for key in kwargs:
            if key == 'delay':
                delay = kwargs[key]
            if key == 'loop':
                loop = kwargs[key]
            if key == 'wait':
                wait = kwargs[key]
            if key == 'clear':
                clr = kwargs[key]
        if wait:
            self._showIterable(args[0], loop, delay, clr)
        else:
            t = _ShowThread(self, args[0], loop, delay, clr)
            t.setUncaughtExceptionHandler(_MyUncaughtExceptionHandler())
            t.start()
        
    def _showIterable(self, iterable, loop, delay, clr):
        if loop:
            while True:
                self._showOnce(iterable, delay, clr)
        else:       
            self._showOnce(iterable, delay, clr)
        
    def _showOnce(self, iterable, delay, clr):
        if type(iterable[0]) == str:
            for s in iterable:
                self.display(s, 9, 0)
                time.sleep(delay / 1000)
            if clr:
                self.clear()    
        else: # list or tuple
            for s in iterable:
                self._showImage(s)
                time.sleep(delay / 1000)
            if clr:
                self.clear()    
    
    def _showImage(self, image):
        matrix = image.getMatrix()
        self.image(matrix)

    def scroll(self, text, **kwargs):
        """Similar to show, but scrolls the string horizontally instead. The delay parameter controls how fast the text is scrolling."""
        _check()
        delay = 150
        wait = True
        loop = False
        monospace = False
        for key in kwargs:
            if key == 'delay':
                delay = kwargs[key]
            if key == 'loop':
                loop = kwargs[key]
            if key == 'wait':
                wait = kwargs[key]
            if key == 'monospace':
                monospace = kwargs[key]
        if wait:
            self._scroll(text, loop, delay, monospace)
        else:
            t = _ScrollThread(self, text, loop, delay, monospace)
            t.setUncaughtExceptionHandler(_MyUncaughtExceptionHandler())
            t.start()
        
    def _scroll(self, text, loop, delay, monospace):
       if loop:
           while True:
               self.textScroll(text, 9, 0, delay, monospace)
       else:                              
           self.textScroll(text, 9, 0, delay, monospace)

    def get_pixel(self, *args):
        """Return the brightness of the LED at column x and row y as an integer between 0 (off) and 9 (bright)."""
        _check()
        pt = self._toPoint(*args)
        if 0 <= pt[0] < self._w and 0 <= pt[1] < self._h:
            i = pt[0] + self._origin[0]
            k = pt[1] + self._origin[1]
            return self._buf[k][i]
        return 0        
    
    def line(self, x, y, dir, length, v):
        _check()
        if length <= 0:
            return
        enabled =  Display._isRepaintEnabled
        Display._isRepaintEnabled = False
        dir = dir % 8
        count = 0
        while True:
            self.dot(x, y, v)
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
        Display._isRepaintEnabled = enabled
        if enabled:        
            self.repaint()

    def arrow(self, x, y, dir, length, v):
        _check()
        if length <= 0 or dir < 0:
            return
        enabled =  Display._isRepaintEnabled
        Display._isRepaintEnabled = False
        dir = dir % 8
        self.line(x, y, dir, length, v)
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
        self.dot(p1[0], p1[1], v)
        self.dot(p2[0], p2[1], v)        
        Display._isRepaintEnabled = enabled
        if enabled:        
            self.repaint()
        
    def rectangle(self, ulx, uly, w, h, v):
        _check()
        for x in range(ulx, ulx + w):
            self._toBuf(x, uly, v)
            self._toBuf(x, uly + h - 1, v)
        for y in range(uly, uly + h):
            self._toBuf(ulx, y, v)
            self._toBuf(ulx + w - 1, y, v)
        if Display._isRepaintEnabled:
            self.repaint()

    def fillRectangle(self, ulx, uly, w, h, v):
        _check()
        for y in range(uly, uly + h):
            for x in range(ulx, ulx + w):
                self._toBuf(x, y, v)
        if Display._isRepaintEnabled:
            self.repaint()

    def circle(self, xcenter, ycenter, r, v):
        _check()
        d = -r
        x = r
        y = 0
        while True:
            for a in [-x, x]:
               for b in [-y, y]:
                    self._toBuf(a + xcenter, b + ycenter, v)
                    self._toBuf(b + xcenter, a + ycenter, v)
            d = d + 2 * y + 1
            y = y + 1
            if d > 0:
                d = d - 2 * x + 2
                x = x - 1
            if y > x:
                break
        if Display._isRepaintEnabled:
            self.repaint()
    
    def fillCircle(self, xcenter, ycenter, r, v):
        _check()
        b = Display._isRepaintEnabled 
        Display._isRepaintEnabled = False
        for z in range(0, r + 1):
            self.circle(xcenter, ycenter, z, v)
        Display._isRepaintEnabled = b
        if Display._isRepaintEnabled:
            self.repaint()

    def image(self, matrix):
        _check()
        self._clearBuf()
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                self._toBuf(x, y, matrix[y][x])
        if Display._isRepaintEnabled:
            self.repaint()

    def getArray(self):
        _check()
        buf = []
        for i in range(self._h):
           line = self._buf[i][:] 
           buf.append(line)
        return tuple(buf)

    def textScroll(self, text, textBrightness = 9, bgBrightness = 0, delay = 150,  monospace = False):
        # we use a scroll buffer of 4 characters to be sure that also chars with small width fills up at least 5 scroll positions 
        _check()
        if len(text) == 0:
            return
        tmp = text + "   "  # scrolls out everything
        isRepaint = Display._isRepaintEnabled
        Display._isRepaintEnabled = True
        m = [None] * 4
        for i in range(4):
            m[i] = self._charToMatrix(tmp[i], textBrightness, bgBrightness, monospace)
        n = 1
        first = True
        while True:
            self._scrollBuf = []    
            for i in range(5):
                self._scrollBuf.append(m[0][i] + [bgBrightness] + \
                                       m[1][i] + [bgBrightness] + \
                                       m[2][i] + [bgBrightness] + \
                                       m[3][i] + [bgBrightness])
            self._showScrollBuf()
            if first:
                time.sleep(0.5)
                first = False
            else:
                time.sleep(delay / 1000)
            for _ in range(len(m[0][0])): # shift left first char   
                self._shiftLeft()
                self._showScrollBuf()
                time.sleep(delay / 1000)
            m[0] = m[1]
            m[1] = m[2]
            m[2] = m[3]
            n += 1
            if n == len(tmp):
                break
            if n + 2 < len(tmp):
                m[3] = self._charToMatrix(tmp[n + 2], textBrightness, bgBrightness, monospace)
        Display._isRepaintEnabled = isRepaint

    def display(self, char, charBrightness = 9, bgBrightness = 0):
        _check()
        sign = False
        if type(char) == int and char < 0:
            sign = True
            char = -char
        isEnabled = Display._isRepaintEnabled
        Display._isRepaintEnabled = False
        self.image(self._charToMatrixMono(str(char), charBrightness, bgBrightness))
        if sign:
            self.set_pixel(0, 2, charBrightness)
            self.set_pixel(1, 2, charBrightness)
        Display._isRepaintEnabled = isEnabled
        if Display._isRepaintEnabled:
            self.repaint()
    
# ------------- public static methods -------------------------------                            
    @staticmethod
    def enableRepaint(enable):
        _check()
        Display._isRepaintEnabled = enable

    @staticmethod
    def getRandomPos():
        _check()
        if len(Display._pList) == 0:
            Display._pList = [n for n in range(25)]
        r = randint(0, len(Display._pList) - 1)    
        m = Display._pList[r]
        del Display._pList[r]
        return m % 5, m // 5

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
    
    def _charToMatrix(self, char, charColor, bgColor, monospace):                    
        matrix = []
        a = pixfont.font5x5[ord(char) - 32]
        start = a[5]
        width = a[6]
        for i in range(5):
            if monospace:
                matrix.append(self._rowToListMono(a[i], charColor, bgColor))
            else:
                matrix.append(self._rowToList(a[i], start, width, charColor, bgColor))
        return matrix

    def _rowToList(self, rowInt, start, width, charColor, bgColor):
        li = []
        mask = 1
        for k in range(5):
            if k >= start and len(li) < width:
                if (rowInt & mask) != 0:
                    li.append(charColor)
                else:
                    li.append(bgColor)
            mask = 2 * mask
        li.reverse()    
        return li

    def _charToMatrixMono(self, char, charColor, bgColor):                    
        if type(char) == int:
            char = str(char)
        matrix = []
        a = pixfont.font5x5[ord(char) - 32]
        for i in range(5):
            matrix.append(self._rowToListMono(a[i], charColor, bgColor))
        return matrix

    def _rowToListMono(self, rowInt, textColor, bgColor):
        li = [bgColor] * 5
        mask = 1
        for k in range(5):
            li[k] = textColor if ((rowInt & mask) != 0) else bgColor
            mask = 2 * mask
        li.reverse()
        return li

    def _shiftLeft(self):
        for i in range(5):  # rows
            a = self._scrollBuf[i][:]
            a =  a[1:] + [0]
            for k in range(len(self._scrollBuf[0])):
                self._scrollBuf[i][k] = a[k]

    def _showScrollBuf(self):
        matrix = [0] * 5
        for i in range(5):
            matrix[i] = self._scrollBuf[i][0:5]
        self.image(matrix)

    def _clearBuf(self):
        for i in range(self._h):
            for k in range(self._w):
                self._buf[i][k] = 0
