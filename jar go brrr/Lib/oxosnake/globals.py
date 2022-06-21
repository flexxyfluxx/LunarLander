# globals.py

from random import randint

BUTTON_L1 = "BUTTON_L1"
BUTTON_L2 = "BUTTON_L2"
BUTTON_L3 = "BUTTON_L3"
BUTTON_R1 = "BUTTON_R1"
BUTTON_R2 = "BUTTON_R2"
BUTTON_R3 = "BUTTON_R3"
BUTTONS = (BUTTON_L1, BUTTON_L2, BUTTON_L3, BUTTON_R1, BUTTON_R2, BUTTON_R3) 

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BASE_COLORS = (RED, GREEN, BLUE, WHITE, YELLOW, CYAN, MAGENTA)

_cList = []
def getRandomColor():
    global _cList
    if len(_cList) == 0:
        _cList = list(BASE_COLORS[:])
    r = randint(0, len(_cList) - 1)
    c = _cList[r]
    del _cList[r]
    return c

def reduceBrightness(color, divider):
    if type(color) == int:
        color = intToRGB(color)
    col = [0] * 3    
    for i in range(3):
        if color[i] != 0:
            col[i] = max(1, int(color[i] / divider))     
    return col

def rgbToInt(c):
    if type(c) in [list, tuple] and len(c) == 3:
        return (c[0] << 16) + (c[1] << 8) + c[2]
    return c

def intToRGB(c):
    if type(c) in [list, tuple] and len(c) == 3:
        return c
    return (c >> 16) & 255, (c >> 8) & 255, c & 255
