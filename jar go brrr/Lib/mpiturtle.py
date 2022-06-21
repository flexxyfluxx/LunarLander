#
# (c) 2017, Tobias Kohn
#
# LAST UPDATE: MAY-01-2017
#
import tjparallels
import gturtle

print "PLEASE NOTE: 'mpiturtle' is an alpha-version in development."
print "             Please report any bugs or problems to the TigerJython-team."

parallel = tjparallels.parallel
getRank = tjparallels.getRank
makeTurtle = gturtle.makeTurtle
setPositionLabel = gturtle.setPositionLabel
enableRepaint = gturtle.enableRepaint
repaint = gturtle.repaint
savePlayground = gturtle.savePlayground
delay = gturtle.delay
clear = gturtle.clear
clean = gturtle.clean
getPlaygroundWidth = gturtle.getPlaygroundBufferWidth
getPlaygroundBufferHeight = gturtle.getPlaygroundBufferHeight
getKey = gturtle.getKey
getKeyWait = gturtle.getKeyWait
getKeyCode = gturtle.getKeyCode
getKeyCodeWait = gturtle.getKeyCodeWait

_turtles = []

def _init_parallel_turtles(threadCount):
    global _turtles
    frame = gturtle.getFrame()
    main_turtle = gturtle.getTurtle()
    sp = main_turtle.getSpeed()
    _turtles = [main_turtle]
    while threadCount > 1:
        t = main_turtle.clone()
        t.speed(sp)
        _turtles.append(t)
        threadCount -= 1
        
def _finish_parallel_turtles():
    global _turtles
    p = gturtle.getPlayground()
    for t in _turtles[1:]:
        t.hideTurtle()
        p.remove(t)
    _turtles = []
    
def _turtle():
    gturtle.isPlaygroundValid()
    if len(_turtles) > 0:
        return _turtles[getRank()]
    else:
        return gturtle.getTurtle()

tjparallels.registerStartParallel(_init_parallel_turtles)
tjparallels.registerStopParallel(_finish_parallel_turtles)

def forward(*args):
    _turtle().forward(*args)

def back(*args):
    _turtle().back(*args)

def left(*args):
    _turtle().left(*args)

def right(*args):
    _turtle().right(*args)

def setPos(*args):
    _turtle().setPos(*args)
    
def moveTo(*args):
    _turtle().moveTo(*args)

def hideTurtle(*args):
    _turtle().hideTurtle(*args)
    
def showTurtle(*args):
    _turtle().showTurtle(*args)

def speed(*args):
    _turtle().speed(*args)
    
def home(*args):
    _turtle().home(*args)
    
def direction(*args):
    return _turtle().direction(*args)

def heading(*args):
    return _turtle().heading(*args)

def towards(*args):
    return _turtle().towards(*args)

def setHeading(*args):
    _turtle().setHeading(*args)

def pushState(*args):
    _turtle().pushState(*args)

def popState(*args):
    return _turtle().popState(*args)

def clearStates(*args):
    _turtle().clearStates(*args)

def setFont(*args):
    _turtle().setFont(*args)

def setFontSize(*args):
    _turtle().setFontSize(*args)

def drawImage(*args):
    _turtle().drawImage(*args)

def getPos(*args):
    return _turtle().getPos(*args)

def getX(*args):
    return _turtle().getX(*args)

def getY(*args):
    return _turtle().getY(*args)

def setColor(*args):
    _turtle().setColor(*args)

def setPenColor(*args):
    _turtle().setPenColor(*args)

def setFillColor(*args):
    _turtle().setFillColor(*args)
    
def dot(*args):
    _turtle().dot(*args)

def setPenWidth(*args):
    _turtle().setPenWidth(*args)

def getColor(*args):
    return _turtle().getColor(*args)

def getPenColor(*args):
    return _turtle().getPenColor(*args)

def getFillColor(*args):
    return _turtle().getFillColor(*args)

def getPenWidth(*args):
    return _turtle().getPenWidth(*args)

def label(*args):
    _turtle().label(*args)

def getTurtleColorHue(*args):
    return _turtle().getTurtleColorHue(*args)

def getPixelColor(*args):
    return _turtle().getPixelColor(*args)

def getPixelColorStr(*args):
    return _turtle().getPixelColorStr(*args)

def getPixelColorHue(*args):
    return _turtle().getPixelColorHue(*args)

def penUp(*args):
    _turtle().penUp(*args)

def penDown(*args):
    _turtle().penDown(*args)

def fill(*args):
    _turtle().fill(*args)

def fillToPoint(*args):
    _turtle().fillToPoint(*args)

def fillOff(*args):
    _turtle().fillOff(*args)

if __name__ == "__main__":
    
    def square(s):
        repeat 4:
            forward(s)
            left(90)
    
    @parallel(4)
    def window(rank, s):
        if rank == 1:
            setPenColor("hot pink")
            fillToPoint()
            speed(-1)
        else:
            setPenColor("red")
        right(rank * 90)
        setPenWidth(rank + 2)
        square(s)
        fillOff()

    makeTurtle()
    forward(50)
    window(70, 90, 110, 130)
    left(45)
    forward(144)
    print "Done"
