# -*- coding: utf-8 -*-
#
# turtle.py: a swing/gturtle-based turtle graphics module for Jython
# Version 1.0 - 3. 2. 2015
#
# Copyright (C) 2015, Tobias Kohn (http://jython.tobiaskohn.ch)
#
# Based upon: 'turtle.py' by G. Lingl (Version 1.1b - 4. 5. 2009):
# 		Copyright (C) 2006 - 2010  Gregor Lingl
# 		email: glingl@aon.at
#
# This is a reimplementation that tries to be as compatible as possible
# with Python's standard turtle module.
#
# See also: http://python4kids.net/turtle.html
#      and: http://www.tigerjython.com/
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
"""
Turtle graphics is a popular way for introducing programming to
kids. It was part of the original Logo programming language developed
by Wally Feurzig and Seymour Papert in 1966.

Imagine a robotic turtle starting at (0, 0) in the x-y plane. Give it
the command turtle.forward(15), and it moves (on-screen!) 15 pixels in
the direction it is facing, drawing a line as it moves. Give it the
command turtle.left(25), and it rotates in-place 25 degrees clockwise.

By combining together these and similar commands, intricate shapes and
pictures can easily be drawn.

----- turtle.py

This module is a reimplementation of turtle.py from the Python standard 
distribution intended to be used with (Tiger) Jython 2.7. It tries to be 
as compatible with Python's original 'turtle.py' as possible. There are
some differences as this module is based upon A. Pluess' Java Turtle
Library 'gturtle' instead of Tkinter (which does not work in Jython).

Currently, the following features do not work properly:

- You cannot change the shape of your turtle or tilt the current shape.

- Mouse handling is restricted to the screen. You cannot react to a mouse
  click or dragging directly on the turtle.
  
- Since there is no underlying Tkinter, any access to it will not work.

- There is no undo-mechanism.

- You cannot remove the drawings of any one turtle without clearing the entire
  screen.
"""
import math, time, types

def _loadMethods(cls, instance):
    """
    Finds all methods of the given class and adds them as functions to the global
    namespace, using the given instance name.
    
    The first parameter 'cls' must be a class and the second is the name of an
    instance of the above class.
    """
    d = cls.__dict__
    d = { key: d[key] for key in d.keys() if key[0] != "_" }
    for k in d:
        value = d[k]
        if isinstance(value, types.FunctionType):
            globals()[k] = eval(instance + "()." + value.__name__)
            
def _lazy(**args):
    """Defines a lazy variable as lambda/function."""
    for key in args:
        value = args[key]
        if callable(value):
            def _def():
                v = value()
                globals()[key] = lambda: v
                return v
            globals()[key] = _def
        else:
            globals()[key] = lambda: value
    
#############################################################################################
##                   Vec2D is taken directly from the official turtle.py                   ##
#############################################################################################

    
class Vec2D(tuple):
    """A 2 dimensional vector class, used as a helper class
    for implementing turtle graphics.
    May be useful for turtle graphics programs also.
    Derived from tuple, so a vector is a tuple!

    Provides (for a, b vectors, k number):
       a+b vector addition
       a-b vector subtraction
       a*b inner product
       k*a and a*k multiplication with scalar
       |a| absolute value of a
       a.rotate(angle) rotation
    """
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))
    def __add__(self, other):
        return Vec2D(self[0]+other[0], self[1]+other[1])
    def __mul__(self, other):
        if isinstance(other, Vec2D):
            return self[0]*other[0]+self[1]*other[1]
        return Vec2D(self[0]*other, self[1]*other)
    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec2D(self[0]*other, self[1]*other)
    def __sub__(self, other):
        return Vec2D(self[0]-other[0], self[1]-other[1])
    def __neg__(self):
        return Vec2D(-self[0], -self[1])
    def __abs__(self):
        return (self[0]**2 + self[1]**2)**0.5
    def rotate(self, angle):
        """rotate self counterclockwise by angle
        """
        perp = Vec2D(-self[1], self[0])
        angle = angle * math.pi / 180.0
        c, s = math.cos(angle), math.sin(angle)
        return Vec2D(self[0]*c+perp[0]*s, self[1]*c+perp[1]*s)
    def __getnewargs__(self):
        return (self[0], self[1])
    def __repr__(self):
        return "(%.2f,%.2f)" % self    
    
#############################################################################################
#############################################################################################

from ch.aplu.turtle import Turtle as _Turtle, TurtleFrame as _TurtleFrame
from java.awt import Font as _Font
from java.awt.geom.Point2D import Double as _AwtPoint2D
from javax.swing import Timer as _SwingTimer
from java.awt.event import ActionListener as _ActionListener

class _TimerActionListener(_ActionListener):
    function = None
    def actionPerformed(self, event):
        if self.function is not None:
            self.function()

_gl_frame = None

def _getGlobalFrame():
    global _gl_frame
    if _gl_frame is None:
        lastFrame = _TurtleFrame.getLastFrame()
        if lastFrame != None:
            lastFrame.dispose()
        _gl_frame = _TurtleFrame()
    return _gl_frame

#############################################################################################

@hideFromDebugView
class TurtleScreen():
    _colormode = 255
    _turtleFrame = None
    _keyPressedDict = {}
    _keyReleasedDict = {}
    
    def __init__(self, frame = None):
        if isinstance(frame, _TurtleFrame):
            self._turtleFrame = frame
        else:
            self._turtleFrame = _getGlobalFrame()
        self._turtleFrame.keyPressed = self._onkeyPressed
        self._turtleFrame.keyReleased = self._onkeyReleased

            
    ###
    
    def bgcolor(self, *args):
        """Set or return background color of the TurtleScreen."""
        pg = self._turtleFrame.getPlayground()
        if len(args) == 0:
            pg.getBkColor()
        else:
            pg.setBkColor(makeColor(args))
    
    def clear(self):
        """Delete all drawings and all turtles from the TurtleScreen. Reset the now empty 
        TurtleScreen to its initial state: white background, no background image, no event 
        bindings and tracing on."""
        pg = self._turtleFrame.getPlayground()
        pg.clear()
    clearscreen = clear
    
    def colormode(self, cmode=None):
        """Return the colormode or set it to 1.0 or 255."""
        if cmode is None:
            return self._colormode
        if cmode == 1.0:
            self._colormode = float(cmode)
        elif cmode == 255:
            self._colormode = int(cmode)
            
    def _colorToTuple(self, clr):
        """Return the tuple (r, g, b) for a given awt-color."""
        r = clr.getRed()
        g = clr.getGreen()
        b = clr.getBlue()
        if self._colormode == 1.0:
            return (r / 255.0, g / 255.0, b / 255.0)
        else:
            return (r, g, b)
        
    def reset(self):
        """Reset all Turtles on the Screen to their initial state."""
        pg = self._turtleFrame.getPlayground()
        pg.clear()
        for i in range(pg.countTurtles()):
            t = pg.getTurtle(i)
            t.home()
    resetscreen = reset
    
    def screensize(self, *args):
        """Return current (canvaswidth, canvasheight)."""
        sz = self._turtleFrame.getPlayground().getSize()
        return (sz.width, sz.height)
    
    def update(self):
        """Perform a TurtleScreen update."""
        self._turtleFrame.repaint()
        
    def listen(self, xdummy=None, ydummy=None):
        """Obsolete! Set focus on TurtleScreen (in order to collect key-events). Dummy arguments are 
        provided in order to be able to pass listen() to the onclick method."""
        pass
    
    def onclick(self, fun, btn=1, add=None):
        """Bind fun to mouse-click event on canvas."""
        self._turtleFrame.mouseHit = fun
    
    def _onkeyPressed(self, event):
        ch = event.getKeyChar()
        if ch in self._keyPressedDict:
            fun = self._keyPressedDict[ch]
            if fun is not None:
                fun()
        
    def _onkeyReleased(self, event):
        ch = event.getKeyChar()
        if ch in self._keyReleasedDict:
            fun = self._keyReleasedDict[ch]
            if fun is not None:
                fun()
            
    def onkey(self, fun, key):
        """Bind fun to key-release event of key."""
        self._keyReleasedDict[key] = fun
        
    def onkeypress(self, fun, key=None):
        """Bind fun to key-press event of key if key is given,
        or to any key-press-event if no key is given."""
        self._keyPressedDict[key] = fun
        
    def ontimer(self, fun, t=0):
        """Install a timer, which calls fun after t milliseconds."""
        if fun is not None and callable(fun):
            listener = _TimerActionListener()
            listener.function = fun
            timer = _SwingTimer(t, listener)
            timer.setRepeats(False)
            timer.start()
        
    def mainloop(self):
        """This function is obsolete in Jython's version of the turtle."""
        pass
    
    def textinput(self, title, prompt, default=None):
        """Pop up a dialog window for input of a string."""
        return inputString(prompt, init=default, quit=False)
    
    def numinput(self, title, prompt, default=None, minval=None, maxval=None):
        """Pop up a dialog window for input of a number."""
        while True:
            value = inputFloat(prompt, init=default, quit=False)
            if value is None:
                return None
            if (minval is None or value >= minval) and \
               (maxval is None or value <= maxval):
                return value
    
#############################################################################################
        
class _Screen(TurtleScreen):
    
    def bye(self):
        """Shut the turtlegraphics window."""
        self._turtleFrame.dispose()
    
    def title(self, titlestring):
        """Set title of turtle window to titlestring."""
        self._turtleFrame.setTitle(titlestring)
        
    def exitonclick(self):
        """Go into mainloop until the mouse is clicked."""
        self.onclick(lambda x, y: self.bye())

#############################################################################################

@hideFromDebugView
class RawTurtle():
    _angleMultiplier = 1.0
    _anglePhase = 0.0
    _isFilling = False
    _polygon = None
    _lastPolygon = None
    _turtle = None
    undobuffer = None
    
    def __init__(self, canvas=None, turtle=None):
        if canvas is None:
            canvas = _gl_screen()
        self.screen = canvas
        if turtle is None:
            self._turtle = _Turtle(canvas._turtleFrame)
        else:
            self._turtle = turtle.clone()
        
    def clone(self):
        """Create and return a clone of the turtle with same position, heading and turtle properties."""
        return RawTurtle(canvas=self.screen, turtle=self._turtle)
        
    def getturtle(self):
        """Return the Turtle object itself."""
        return self
    getpen = getturtle
    
    def reset(self):
        """Re-center the turtle and set variables to the default values."""
        self.home()
        self.undobuffer = None
        self._polygone = None
        self._lastPolygon = None
        self._angleMultiplier = 1.0
        self._anglePhase = 0.0
        self.screen.reset()
        self._turtle.showTurtle()
    
    def getscreen(self):
        """Return the TurtleScreen object the turtle is drawing on. TurtleScreen methods can then be 
        called for that object."""
        return self.screen
    getcanvas = getscreen
    
    def _colorToTuple(self, clr):
        return self.screen._colorToTuple(clr)
        
    ###
    
    def _add_poly(self, p=None):
        if self._polygon is not None:
            if p is None:
                p = self._turtle.getPos()
                (x, y) = (p.x, p.y)
            else:
                x, y = p
            x = round(x, 3)
            y = round(y, 3)
            if len(self._polygon) > 0:
                lx, ly = self._polygon[-1]
                if lx != x or ly != y:
                    self._polygon.append((x, y))
            else:
                self._polygon.append((x, y))
        
    
    def begin_poly(self):
        """Start recording the vertices of a polygon. Current turtle position is first 
        vertex of polygon."""
        self._polygon = []
        self._add_poly()
    
    def end_poly(self):
        """Stop recording the vertices of a polygon. Current turtle position is last vertex 
        of polygon. This will be connected with the first vertex."""
        if self._polygon is not None and len(self._polygon) > 0:
            self._add_poly()
            self._add_poly(self._polygon[0])
            self._lastPolygon = self._polygon
        self._polygon = None
    
    def get_poly(self):
        """Return the last recorded polygon."""
        return self._lastPolygon
    
    ###
    
    def degrees(self, fullcircle = 360.0):
        """Set angle measurement units, i.e. set number of “degrees” for a 
        full circle. Default value is 360 degrees."""
        if fullcircle > 0:
            self._angleMultiplier = 360.0 / fullcircle
        else:
            raise Exception()
    
    def radians(self):
        """Set the angle measurement units to radians. Equivalent to degrees(2*math.pi)."""
        self._angleMultiplier = 360 / math.pi
        
    def _toAngle(self, angle):
        return (angle * self._angleMultiplier) + self._anglePhase
    
    def _fromAngle(self, angle):
        return (angle - self._anglePhase) / self._angleMultiplier
    
    def _toPoint(self, x, y):
        if isinstance(x, RawTurtle):
            x, y = x.position()
        elif isinstance(x, tuple):
            x, y = x
        elif isinstance(x, _AwtPoint2D):
            y = x.y
            x = x.x
        return (x, y)
        
    ###
        
    def position(self):
        """Return the turtle’s current location (x,y) (as a Vec2D vector)."""
        pnt = self._turtle.getPos()
        return (pnt.x, pnt.y)
    pos = position
    
    def xcor(self):
        """Return the turtle’s x coordinate."""
        return self._turtle.getPos().x
    
    def ycor(self):
        """Return the turtle’s y coordinate."""
        return self._turtle.getPos().y
    
    def towards(self, x, y=None):
        """Return the angle between the line from turtle position to position specified by (x,y), 
        the vector or the other turtle."""
        x, y = self._toPoint(x, y)
        return self._fromAngle(self._turtle.towards(x, y))
        
    def heading(self):
        """Return the turtle’s current heading."""
        return self._fromAngle(self._turtle.heading())
    
    def distance(self, x, y=None):
        """Return the distance from the turtle to (x,y), the given vector, or 
        the given other turtle, in turtle step units."""
        x, y = self._toPoint(x, y)
        return self._turtle.distance(x, y)
    
    ###
        
    def forward(self, distance):
        """Move the turtle forward by the specified distance, in the direction the turtle is headed."""
        self._turtle.forward(distance)
    fd = forward
    
    def backward(self, distance):
        """Move the turtle backward by distance, opposite to the direction the turtle is headed. Do 
        not change the turtle’s heading."""
        self._add_poly()
        self._turtle.back(distance)
    bk = backward
    back = backward
    
    def left(self, angle):
        """Turn turtle left by angle units. (Units are by default degrees, but can be set via the 
        degrees() and radians() functions.)"""
        angle *= self._angleMultiplier
        self._turtle.left(angle)
        self._add_poly()
    lt = left
    
    def right(self, angle):
        """Turn turtle right by angle units. (Units are by default degrees, but can be set via the 
        degrees() and radians() functions.)"""
        angle *= self._angleMultiplier
        self._turtle.right(angle)
        self._add_poly()
    rt = right
    
    def setposition(self, x, y=None):
        """If y is None, x must be a pair of coordinates or a Vec2D (e.g. as returned by pos()).

        Move turtle to an absolute position. If the pen is down, draw line. Do not change 
        the turtle’s orientation."""
        x, y = self._toPoint(x, y)
        self._turtle.setPos(x, y)
        self._add_poly()
    setpos = setposition
    goto = setposition
    
    def setx(self, x):
        """Set the turtle’s first coordinate to x, leave second coordinate unchanged."""
        if isinstance(x, RawTurtle):
            x = x.xcor()
        self._turtle.setX(x)
        self._add_poly()
    
    def sety(self, y):
        """Set the turtle’s second coordinate to y, leave first coordinate unchanged."""
        if isinstance(y, RawTurtle):
            y = y.xcor()
        self._turtle.setY(y)
        self._add_poly()
        
    def setheading(self, to_angle):
        """Set the orientation of the turtle to to_angle."""
        self._turtle.heading(self._toAngle(to_angle))
        self._add_poly()
    seth = setheading
    
    def home(self):
        """Move turtle to the origin – coordinates (0,0) – and set its heading to its start-orientation."""
        self._turtle.home()
        self._add_poly()
        
    def _drawpolygon(self, radius, extent, steps):
        """Auxiliary method for 'circle'. Draws a polygon or a fraction thereof."""
        # Distinguish between going left and right
        if radius < 0:
            turn = self._turtle.right
            radius *= -1
        else:
            turn = self._turtle.left
        # Compute the turning angle and the edge length of the polygon
        phi = 180 / steps
        s = 2 * radius * math.cos(math.radians(90 - phi))
        # Is there a remaining angle?
        if extent != 360:
            stepCount = extent * steps // 360
            remAngle = extent - (stepCount * 2 * phi)
        else:
            stepCount = steps
            remAngle = 0
        # Draw the main part of the polygon
        self._add_poly()
        for i in range(stepCount):
            turn(phi)
            self._turtle.forward(s)
            self._add_poly()
            turn(phi)
        # Draw the remaining/fractional part of the polygon
        if remAngle > 0:
            turn(phi)
            h = radius * math.sin(math.radians(90 - phi))
            s = s/2 + h * math.tan(math.radians(remAngle - phi))
            self._turtle.forward(s)
            self._add_poly()
        
    def circle(self, radius, extent=None, steps=None):
        """Draw a circle with given radius. The center is radius units left of the turtle; 
        extent – an angle – determines which part of the circle is drawn. If extent is not given, 
        draw the entire circle. If extent is not a full circle, one endpoint of the arc is the 
        current pen position. Draw the arc in counterclockwise direction if radius is positive, 
        otherwise in clockwise direction. Finally the direction of the turtle is changed by the 
        amount of extent.

        As the circle is approximated by an inscribed regular polygon, steps determines the number of 
        steps to use. If not given, it will be calculated automatically. May be used to draw regular 
        polygons."""
        if extent is None:
            extent = 360.0
        else:
            extent *= self._angleMultiplier
            extent %= 360.0
            if extent <= 0: extent = 360.0
        if self._polygon is not None:
            self._drawpolygon(radius, extent, abs(radius))
        elif steps is None or steps > 30:
            if radius >= 0:
                self._turtle.leftArc(radius, extent)
            else:
                self._turtle.rightArc(-radius, extent)
        elif steps > 2:
            self._drawpolygon(radius, extent, steps)
        
    def dot(self, size=None, *color):
        """Draw a circular dot with diameter size, using color. If size is not given, the maximum 
        of pensize+4 and 2*pensize is used."""
        if size is None:
            size = 2
        if size >= 1:
            if len(color) > 0:
                clr = self._turtle.getPenColor()
                self._turtle.setPenColor(makeColor(color))
                self._turtle.dot(size)
                self._turtle.setPenColor(clr)
            else:
                self._turtle.dot(size)
    
    def stamp(self):
        """Stamp a copy of the turtle shape onto the canvas at the current turtle position."""
        self._turtle.stampTurtle()
    
    def speed(self, speed=None):
        """Set the turtle’s speed to an integer value in the range 0..10. If no argument is given, 
        return current speed.

        If input is a number greater than 10 or smaller than 0.5, speed is set to 0. Speedstrings 
        are mapped to speedvalues as follows:

        “fastest”: 0
        “fast”: 10
        “normal”: 6
        “slow”: 3
        “slowest”: 1

        Speeds from 1 to 10 enforce increasingly faster animation of line drawing and turtle turning.

        Attention: speed = 0 means that no animation takes place. forward/back makes turtle jump and 
        likewise left/right make the turtle turn instantly."""
        if speed is None:
            s = self._turtle.getSpeed()
            if s <= 0:
                return 0
            else:
                return min(s // 200, 10)
        elif 0 < speed <= 10:
            self._turtle.speed(speed * 200)
            self._turtle.setAngleResolution(int(72 // speed))
        else:
            self._turtle.speed(-1)
            
    def pendown(self):
        """Pull the pen down – drawing when moving."""
        self._turtle.penDown()
    pd = pendown
    down = pendown
    
    def penup(self):
        """Pull the pen up – no drawing when moving."""
        self._turtle.penUp()
    pu = penup
    up = penup
    
    def pensize(self, size, width=None):
        """Set the line thickness to width or return it. If resizemode is set to “auto” and turtleshape 
        is a polygon, that polygon is drawn with the same line thickness. If no argument is given, the 
        current pensize is returned."""
        if width is None:
            return self._turtle.penWidth()
        elif width >= 1:
            self._turtle.penWidth(width)
    width = pensize
    
    def pen(self, pen=None, **pendict):
        """Return or set the pen’s attributes in a “pen-dictionary”."""
        currentDict = {
            'pendown': self.isdown(),
            'pencolor': self.pencolor(),
            'fillcolor': self.fillcolor(),
            'pensize': self.pensize(),
            'speed': self.speed(),
            'shown': self.isvisible()
        }
        
        def _setValue(key, value):
            if key == 'pendown':
                if value != self.isdown():
                    if value:
                        self.pendown()
                    else:
                        self.penup()
            elif key == 'pencolor':
                self.pencolor(value)
            elif key == 'fillcolor':
                self.pencolor(value)
            elif key == 'pensize':
                self.pensize(value)
            elif key == 'speed':
                self.speed(speed)
            elif key == 'shownn':
                if value:
                    self.showturtle()
                else:
                    self.hideturtle()
                
        if pen != None:
            for key in pen:
                _setValue(key, pen[key])
        if len(pendict) > 0:
            for key in pendict:
                _setValue(key, pen[key])
        
        return currentDict
    
    def isdown(self):
        """Return True if pen is down, False if it’s up."""
        return not self._turtle.isPenUp()
    
    def pencolor(self, *args):
        """Return or set the pencolor."""
        if len(args) > 0:
            clr = makeColor(*args)
            self._turtle.setPenColor(clr)
            self._turtle.setColor(clr)
        else:
            clr = self._turtle.getPenColor()
            return self._colorToTuple(clr)

    def fillcolor(self, *args):
        """Return or set the fillcolor."""
        if len(args) > 0:
            clr = makeColor(*args)
            self._turtle.setFillColor(clr)
        else:
            clr = self._turtle.getFillColor()
            return self._colorToTuple(clr)
    
    def color(self, *args):
        """Return or set pencolor and fillcolor."""
        if len(args) > 0:
            if len(args) % 2 == 1:
                clr = makeColor(*args)
                self._turtle.setPenColor(clr)
                self._turtle.setFillColor(clr)
                self._turtle.setColor(clr)
            else:
                L = len(args) // 2
                clr = makeColor(args[:L])
                self._turtle.setPenColor(clr)
                self._turtle.setColor(clr)
                clr = makeColor(args[L:])
                self._turtle.setFillColor(clr)
        else:
            pc = self.pencolor()
            fc = self.fillcolor()
            return (self._colorToTuple(pc), _colorToTuple(fc))
    
    def fill(self, flag=None):
        """Call fill(True) before drawing the shape you want to fill, and fill(False) when done. 
        When used without argument: return fillstate (True if filling, False else)."""
        if flag is None:
            return self._isFilling
        elif flag:
            self.begin_fill()
        else:
            self.end_fill()
        
    def begin_fill(self):
        """Call just before drawing a shape to be filled. Equivalent to fill(True)."""
        if not self._isFilling:
            self._isFilling = True
            self._turtle.startPath()
        
    def end_fill(self):
        """Fill the shape drawn after the last call to begin_fill(). Equivalent to fill(False)."""
        if self._isFilling:
            self._turtle.fillPath()
            self._isFilling = False

    def hideturtle(self):
        """Make the turtle invisible. It’s a good idea to do this while you’re in the middle of 
        doing some complex drawing, because hiding the turtle speeds up the drawing observably."""
        self._turtle.hideTurtle()
    ht = hideturtle
        
    def showturtle(self):
        """Make the turtle visible."""
        self._turtle.showTurtle()
    st = showturtle
        
    def isvisible(self):
        """Return True if the Turtle is shown, False if it’s hidden."""
        return not self._turtle.isHidden()
    
    def window_height(self):
        """Return the height of the turtle window."""
        return self.screen.screensize()[1]
    
    def window_width(self):
        """Return the width of the turtle window."""
        return self.screen.screensize()[0]
    
    def _setRelativePos(self, deltaX=None, deltaY=None):
        if deltaX is not None and deltaX != 0:
            self._turtle.setX(self._turtle.getX() + deltaX)
        if deltaY is not None and deltaY != 0:
            self._turtle.setY(self._turtle.getY() + deltaY)
    
    def write(self, arg, move=False, align="left", font=None):
        """Write text - the string representation of arg - at the current turtle position according 
        to align (“left”, “center” or right”) and with the given font. If move is true, the pen is 
        moved to the bottom-right corner of the text. By default, move is False."""
        # First, set the new font
        if font is not None:
            if type(font) == int:
                f_size = font
                self._turtle.setFontSize(f_size)
            else:
                f_name, f_size, f_type = font
                if f_type == "bolditalic":
                    f_type = _Font.BOLD | _Font.ITALIC
                elif f_type == "bold":
                    f_type = _Font.BOLD
                elif f_type == "italic":
                    f_type = _Font.ITALIC
                else:
                    f_type = _Font.PLAIN
                self._turtle.setFont(f_name, f_type, f_size)
        # Get the width of text to draw. 
        width = self._turtle.getTextWidth(arg)
        # Draw the text and move the turtle if approriate
        if align == "left":
            self._turtle.label(arg)
            if move:
                self._setRelativePos(deltaX=width)
        elif align == "center":
            if move:
                self._setRelativePos(deltaX=-width/2)
                self._turtle.label(arg)
                self._setRelativePos(deltaX=width)
            else:
                p = self._turle.getPos()
                self._setRelativePos(deltaX=-width/2)
                self._turtle.label(arg)
                self._turtle.setPos(p)
        elif align == "right":
            p = self._turtle.getPos()
            self._setRelativePos(deltaX=-width)
            self._turtle.label(arg)
            self._turtle.setPos(p)
        else:
            self._turtle.label(arg)
            
    ###
    
    def colormode(self, cmode=None):
        """Return the colormode or set it to 1.0 or 255. Subsequently r, g, b 
        values of color triples have to be in the range 0..cmode."""
        return self.screen.colormode(cmode)
    
    def onclick(self, fun, btn=1, add=None):
        """Bind fun to mouse-click events on this turtle."""
        self.screen.onclick(fun)
        
    def onrelease(self, fun, btn=1, add=None):
        """Bind fun to mouse-button-release events on this turtle."""
        pass
    
    def ondrag(self, fun, btn=1, add=None):
        """Bind fun to mouse-move events on this turtle."""
        pass
    
    def mainloop():
        """Obsolete."""
        pass
    done = mainloop
    
    ### Here are compatiblity methods which are not implemented: ###
    
    def getshapes(self):
        """Not implemented."""
        return ['turtle']
    
    def register_shape(self, name, shape=None):
        """Not implemented."""
        pass
    add_shape = register_shape
    
    def shape(self, name=None):
        """Not implemented."""
        pass
    
    def resizemode(self, rmode=None):
        """Not impleneted."""
        if rmode is None:
            return "noresize"
        
    def shapesize(self, stretch_wid=None, stretch_len=None, outline=None):
        """Not implenented."""
        if stretch_wid is None and stretch_len is None and outline is None:
            return (1, 1, 1)
    turtlesize=shapesize
    
    def tilt(self, angle):
        """Not implemented."""
        pass
    settitleangle = tilt
    
    def tiltangle(self):
        """Not implemented."""
        return 0
    
    def undo(self):
        """Not implemented."""
        pass
    
    def setundobuffer(self, size):
        """Not implemented."""
        pass
    
    def undobufferentries(self):
        """Not implemented."""
        return 0
    
    def tracer(self, flag):
        """Deprecated! Set tracing on if flag is True, and off if it is False.
        Tracing means line are drawn more slowly, with an
        animation of an arrow along the line."""
        if flag:
            self.showturtle()
        else:
            self.hideturtle()

class Turtle(RawTurtle):
    pass

#############################################################################################

# Create a global turtle-instance when needed!
_lazy(_gl_screen = _Screen())
_lazy(_gl_turtle = Turtle)

def Screen():
    """Return the singleton screen object.
    If none exists at the moment, create a new one and return it,
    else return the existing one."""
    return _gl_screen()

# Load all methods from the turtle to be accessible as functions as well
_loadMethods(_Screen, "_gl_screen")
_loadMethods(RawTurtle, "_gl_turtle")

#############################################################################################

#############################################################################################

if __name__ == "__main__":

    def switchpen():
        if isdown():
            pu()
        else:
            pd()

    def demo1():
        """Demo of old turtle.py - module"""
        reset()
        tracer(True)
        up()
        backward(100)
        down()
        # draw 3 squares; the last filled
        width(3)
        for i in range(3):
            if i == 2:
                begin_fill()
            for _ in range(4):
                forward(20)
                left(90)
            if i == 2:
                color("maroon")
                end_fill()
            up()
            forward(30)
            down()
        width(1)
        color("black")
        # move out of the way
        tracer(False)
        up()
        right(90)
        forward(100)
        right(90)
        forward(100)
        right(180)
        down()
        # some text
        write("startstart", 1)
        write("start", 1)
        color("red")
        # staircase
        for i in range(5):
            forward(20)
            left(90)
            forward(20)
            right(90)
        # filled staircase
        tracer(True)
        begin_fill()
        for i in range(5):
            forward(20)
            left(90)
            forward(20)
            right(90)
        end_fill()
        # more text

    def demo2():
        """Demo of some new features."""
        speed(1)
        st()
        pensize(3)
        setheading(towards(0, 0))
        radius = distance(0, 0)/2.0
        rt(90)
        for _ in range(18):
            switchpen()
            circle(radius, 10)
        write("wait a moment...")
        while undobufferentries():
            undo()
        reset()
        lt(90)
        colormode(255)
        laenge = 10
        pencolor("green")
        pensize(3)
        lt(180)
        for i in range(-2, 16):
            if i > 0:
                begin_fill()
                fillcolor(255-15*i, 0, 15*i)
            for _ in range(3):
                fd(laenge)
                lt(120)
            end_fill()
            laenge += 10
            lt(15)
            speed((speed()+1)%12)
        #end_fill()

        lt(120)
        pu()
        fd(70)
        rt(30)
        pd()
        color("red","yellow")
        speed(0)
        begin_fill()
        for _ in range(4):
            circle(50, 90)
            rt(90)
            fd(30)
            rt(90)
        end_fill()
        lt(90)
        pu()
        fd(30)
        pd()
        shape("turtle")

        tri = getturtle()
        tri.resizemode("auto")
        turtle = Turtle()
        turtle.resizemode("auto")
        turtle.shape("turtle")
        turtle.reset()
        turtle.left(90)
        turtle.speed(0)
        turtle.up()
        turtle.goto(280, 40)
        turtle.lt(30)
        turtle.down()
        turtle.speed(6)
        turtle.color("blue","orange")
        turtle.pensize(2)
        tri.speed(6)
        setheading(towards(turtle))
        count = 1
        while tri.distance(turtle) > 4:
            turtle.fd(3.5)
            turtle.lt(0.6)
            tri.setheading(tri.towards(turtle))
            tri.fd(4)
            if count % 20 == 0:
                turtle.stamp()
                tri.stamp()
                switchpen()
            count += 1
        tri.write("CAUGHT! ", font=("Arial", 16, "bold"), align="right")
        tri.pencolor("black")
        tri.pencolor("red")

        def baba(xdummy, ydummy):
            clearscreen()
            bye()

        time.sleep(2)

        while undobufferentries():
            tri.undo()
            turtle.undo()
        tri.fd(50)
        tri.write("  Click me!", font = ("Courier", 12, "bold") )
        tri.onclick(baba, 1)

    demo1()
    demo2()
    exitonclick()