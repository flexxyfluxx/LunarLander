import gamegrid as gg

"""
Floacation: Float Location

Wie gg.Location, aber mit FLOATS!!1!
"""

class Floacation(gg.Location):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    
    def get_int_location(self):
        return Location(int(self.x), int(self.y))
    
    def get_int_x(self):
        return int(x)
    
    def get_int_y(self):
        return int(y)