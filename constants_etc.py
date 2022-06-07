# -*- coding: utf-8 -*-

""" Universal Constants Module:
Enthält die ganzen Dicts und so.
Hier werden außerdem die Settings aus der INI geparsed
und Konstanten zugewiesen.
"""

""" Imports: """
from os.path import abspath # oh nyo the namespace OwO~ onwy impowt whats neccessawy~~ rawr :3
import ConfigParser as cp
from java.awt import Color

# ----- SETTINGS VON INI LADEN -----

class Cfg():
    """
    Diese Klasse verwaltet die Konfigurationswerte, die vom restlichen Programm verwendet werden.
    Sie kann die Werte in settings.ini lesen, verändern und wieder in die Datei schreiben.
    """
    def __init__(self):
        # initialisiere den Parser
        self._parser = cp.ConfigParser()
        self._parser.read("settings.ini")

        # hole geparste Werte aus dem Parser
        self.DRY_MASS = self._parser.getint('Lander','DryMass')
        self.FUEL_MASS = self._parser.getint('Lander', 'FuelMass')
        self.GRAVITY = self._parser.getfloat('Game', 'Gravity')
        self.FUEL_CONSUMPTION = self._parser.getfloat('Lander', 'MaxFuelConsumption')
        self.THRUST_SCALE = self._parser.getint('Lander', 'ThrustScale')
        self.FUEL_VELOCITY = self._parser.getint('Lander', 'FuelVelocity')
    
    def change(self, attr, val):
        try:
            self.attr = float(val)
        except AttributeError as err:
            print("[ERROR] "+repr(err)+" Attribute not found!")
        except ValueError as err:
            print("[ERROR] "+repr(err)+" Value must be a number!")
    
    def commit_to_ini(self):
        with open('settings.ini', 'w') as file:
            self._parser.write(file)


config = Cfg()

# ----- ENDE SETTINGS LADEN -----

# ----- KONSTANTEN -----
""" Dict mit den Paths zu den relevanten Bildern: """
SPRITE = {
    'lander': abspath("./sprites/lander.png")
}

""" Richtungskonstanten: """
EAST = 0
SOUTH = 90
WEST = 180
NORTH = 270

""" Farben: """
GRAY = Color(153, 153, 153)
WHITE = Color.WHITE

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
""" Blanke Objekte des Typs 'object' sind nur mit sich selbst identisch.
Hiermit kann ich arbiträre Konstanten definieren, die zB. hier nur zur
Spezifikation eines Funktionsverhaltens dienen:

obj1 = object()
obj2 = object()
print(obj1 is obj2) # prints False
print(obj1 == obj2) # prints False

obj3 = object()
ref = obj3
print(obj3 is ref) # prints True
print(obj3 == ref) # prints True

Ich kann hiermit arbiträre Keys erstellen, die nur der Identifikation/Kennzeichnung dienen und keine weitere Bedeutung haben:
"""
LAST_UP = object()
LAST_DN = object()
LAST_LEFT = object()
LAST_RIGHT = object()

# ----- ENDE KONSTANTEN -----

# ----- FUNKTIONEN -----
def unzip(zipped):
    """
    Umkehroperation von zip()
    """
    return zip(*zipped)

def getindex(val, arr):
    """
    Finde denjenigen Index in einem Array an einzigartigen Werten, dessen Wert gleich dem geg. ist.
    """
    for index in range(len(arr)):
        if arr[index] == val: return index