from __future__ import print_function
import ch.aplu.jgamegrid as gg
from time import time
import random as r

class Terrain():
    def __init__(self, resolution, min, max, seed=time()):
        gen = r.Random(seed)
        self.plot = [gen.randint(min, max) for c in range(resolution)]
        
    
    def print_plot(self):
        for c in self.plot:
            for z in range(c):
                print("#", end="")
            print("")
        
    def smooth_plot(self, count):
        for c in range(count):
            self.plot = [(self.plot[c-1] + self.plot[c] + self.plot[c+1]) / 3 for c in range(len(self.plot) - 1)] \
                        + [(self.plot[-2] + self.plot[-1] + self.plot[0]) / 3]

    def get_interpolated(self, steps):
        out = []
        for c in range(len(self.plot)-1):
            out += [ (float(self.plot[c]) + (float(self.plot[c+1]) - float(self.plot[c])) / steps * current_step) for current_step in range(steps) ]
        
        # Deckel drauf!
        out += [self.plot[-1]]

        return out


if __name__ == "__main__":
    #"""
    terra = Terrain(10, 5, 150)
    terra.smooth_plot(4)
    interpol = terra.get_interpolated(16)
    terra.print_plot()
    print("\n----------\n")
    for c in interpol:
        print("".join(["#" for z in range(int(round(c)))]), sep="")
    """
    terra = Terrain(100)
    grid = gg.GameGrid(800, 800, 1)

    #"""