

import gamegrid as gg
from math import *
from Floacation import *

class Lander(gg.Actor):
    def __init__(self, sprite, gravity):
        gg.Actor.__init__(self, sprite)
        self._gravity = gravity
        
        self.x_velocity = 0
        self.y_velocity = 0
        
        self.true_location = Floacation(20, 20)
        
        self.angle = 0
    
    
    def act(self):
        self._apply_gravity()
        self.true_position.x += self.x_velocity / 100
        self.true_position.y -= self.y_velocity / 100
        self.move()
    
    
    def move(self):
        self.setX(self.true_position.get_int_x())
        self.setY(self.true_position.get_int_y())


    def get_abs_velocity(self):
        return sqrt(self.x_velocity ** 2 + self.y_velocity ** 2)
    
    
    def _apply_gravity(self):
        self.y_velocity -= self._gravity / 100

if __name__ == "__main__":
    grid = gg.GameGrid(800, 800, 1, None)
    
    lander = Lander('sprites/jellyfish.gif', 1.62)
    
    grid.addActor(lander, lander.true_position)
    
    grid.setSimulationPeriod(10)
    grid.show()
    grid.doRun()