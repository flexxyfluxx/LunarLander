""" Universal Constants Module:
Enthält die ganzen Dicts und so.
Hier werden außerdem die Settings aus der INI geparsed
und Konstanten zugewiesen.
"""

""" Imports: """
from os.path import abspath # oh nyo the namespace OwO~ onwy impowt whats neccessawy~~ rawr :3
import ConfigParser as cp

# ----- SETTINGS VON INI LADEN -----

class Cfg(): # Dataclass mit den Settings aus der INI.
    def __init__(self):
        self._parser = cp.ConfigParser()
        self._parser.read("settings.ini")
        
        self.WINDOW_HEIGHT = self._parser.getint('WindowDimensions', 'WINDOW_HEIGHT')
        self.WINDOW_HEIGHT = 200 if self.WINDOW_HEIGHT < 200 else self.WINDOW_HEIGHT
        
        self.WINDOW_WIDTH = self._parser.getint('WindowDimensions', 'WINDOW_WIDTH')
        self.WINDOW_WIDTH = 200 if self.WINDOW_WIDTH < 200 else self.WINDOW_WIDTH
        
        self.PADDLE_SPEED = self._parser.getint('GameSettings', 'PADDLE_SPEED')
        self.PADDLE_ACCEL_LIMIT = self._parser.getfloat('GameSettings', 'PADDLE_ACCEL_LIMIT')
        self.BALL_SPEED = self._parser.getint('GameSettings', 'BALL_SPEED')
        self.OBSTACLES = self._parser.getboolean('GameSettings', 'OBSTACLES')
    
    
    def commit_to_ini(self):
        fileobj = open('settings.ini', 'w')
        self._parser.write(fileobj)
        fileobj.close()


config = Cfg()

# ----- ENDE SETTINGS LADEN -----

# ----- KONSTANTEN -----
""" Dict mit den Paths zu den relevanten Bildern: """
SPRITE = {
    # insert sprites
}

""" Richtungskonstanten: """
EAST = 0
SOUTH = 90
WEST = 180
NORTH = 270

""" Keypress-Dict """
KEY = {
    'arr_up': 38,
    'arr_dn': 40,
    'arr_lt': 37,
    'arr_rt': 39,
    'esc': 27,
    'ctrl': 17,
    'shift': 16,
    'space': 32,
    'a': 65,
    'b': 66,
    'c': 67,
    'd': 68,
    'e': 69, # nice
    'f': 70,
    'g': 71,
    'h': 72,
    'i': 73,
    'j': 74,
    'k': 75,
    'l': 76,
    'm': 77,
    'n': 78,
    'o': 79,
    'p': 80,
    'q': 81,
    'r': 82,
    's': 83,
    't': 84,
    'u': 85,
    'v': 86,
    'w': 87,
    'x': 88,
    'y': 89,
    'z': 90,
    '0': 48,
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57
}

# ----- ENDE KONSTANTEN -----