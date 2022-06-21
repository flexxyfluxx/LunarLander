# Part of TigerJython (www.tigerjython.ch)
# (c) 2013-2015, T. Kohn
#
# Last update: 30. August 2015
#
# This module contains various calculations for 
# didactic/educational use.
from java.awt import Color as __AwtColor
from tigerjython.utils import ImageUtils

def easterday(year):
    """Das Osterdatum fuer ein bestimmtes Jahr nach 
       der Formel von Gauss berechnen."""
    k = year // 100
    p = (8 * k + 13) // 25
    q = k * 3 // 4
    M = (15 + q - p) % 30
    N = (4 + q) % 7
    b = year % 4
    c = year % 7
    d = (19*(year % 19) + M) % 30
    e = (2*b + 4*c + 6*d + N) % 7
    return (22 + d + e)

# These are the colors from the sun's spectrum.
__RAINBOW_COLORS = [0x170027, 0x25003D, 0x36005F, 0x450081,
                    0x5000A4, 0x5300C1, 0x4900D4, 0x3800E0,
                    0x2803EB, 0x1917F2, 0x0D3FF8, 0x0669F5,
                    0x0191E5, 0x00B4C6, 0x00D09D, 0x00D972,
                    0x00D148, 0x00C624, 0x00BC0C, 0x00B802,
                    0x01B700, 0x07B900, 0x18BE00, 0x3DC900,
                    0x68D300, 0x92D800, 0xBCD600, 0xE0CA00,
                    0xFAB500, 0xFF9900, 0xFF7800, 0xFF5B00,
                    0xFF4300, 0xFF3000, 0xFF2100, 0xF01500,
                    0xCC0D00, 0xA10600, 0x770200, 0x4B0000]
    
def makeRainbowColor(index, maxIndex = None):
    """Gibt eine 'Regenbogenfarbe' oder 'Schwarz' zurueck."""
    if maxIndex != None and maxIndex != len(__RAINBOW_COLORS):
        newIndex = int(index * len(__RAINBOW_COLORS) // maxIndex)
        return makeRainbowColor(newIndex)
    elif 0 <= index < len(__RAINBOW_COLORS):
        return __AwtColor(__RAINBOW_COLORS[int(index)])
    else:
        return __AwtColor.BLACK
        
def loadImageData(filename):
    """Gibt die Daten des angegeben Bilds zurueck."""
    return ImageUtils.loadImageData(filename)

def loadImageDataGray(filename):
    """Gibt die Daten des angegeben Bilds in Graustufen zurueck."""
    return ImageUtils.loadImageDataGray(filename)

def loadImageDataBW(filename):
    """Gibt die Daten des angegeben Bilds in Schwarz/Weiss zurueck."""
    return ImageUtils.loadImageDataBW(filename)