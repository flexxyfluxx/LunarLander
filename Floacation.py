# -*- coding: utf-8 -*-
# author: flyxx

import ch.aplu.jgamegrid as gg

"""
Floacation: Float Location

Wie gg.Location, aber mit FLOATS!!1!
"""

class Floacation():
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    
    def get_int_location(self):
        return gg.Location(int(round(self.x)), int(round(self.y)))
    
    def get_int_x(self):
        return int(round(self.x))
    
    def get_int_y(self):
        return int(round(self.y))