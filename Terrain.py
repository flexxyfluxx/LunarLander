from __future__ import print_function
import ch.aplu.jgamegrid as gg
#from time import time_ns
import random as r

class Terrain():
    def __init__(self, resolution, min, max):
        self.plot = [r.randint(min, max) for c in range(resolution)]
        
    
    def print_plot(self):
        for c in self.plot:
            for z in range(c):
                print("#", end="")
            print("")
        
    def smooth_plot(self, count):
        for c in range(count):
            self.plot = [(self.plot[c-1] + self.plot[c] + self.plot[c+1]) / 3 for c in range(len(self.plot) - 1)] \
                        + [(self.plot[-2] + self.plot[-1] + self.plot[0]) / 3]


if __name__ == "__main__":
    """
    terra = Terrain(200, 5, 150)
    terra.smooth_plot(4)
    terra.print_plot()
    """
    terra = Terrain(100)
    grid = gg.GameGrid(800, 800, 1)
    #"""