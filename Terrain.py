from __future__ import print_function
import ch.aplu.jgamegrid as gg
import java.awt.Font as j_Font
from time import time
import random as r

class Terrain():
    def __init__(self, resolution, min, max, seed=time()):
        self.seed = seed
        gen = r.Random(self.seed)
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

    def get_interpolated(self, spacing):
        out = []
        for c in range(len(self.plot)-1):
            out += [ (float(self.plot[c]) + (float(self.plot[c+1]) - float(self.plot[c])) / spacing * current_step) for current_step in range(spacing) ]
        
        # Deckel drauf!
        out += [self.plot[-1]]

        return out
    
    def draw_to_grid(self, grid, show_seed):
        terrain_length = len(self.plot)
        ratio = grid.getNbHorzCells() / terrain_length
        grid_height = grid.getNbVertCells()
        #interpolated = self.get_interpolated(ratio)
        current_true = 0
        background = grid.getBg()
        background.setLineWidth(5)

        for c in range(1, terrain_length):
            background.drawLine(int(round((c-1) * ratio)), grid_height - self.plot[c-1], int(round(c * ratio)), grid_height - self.plot[c])
        
        if show_seed:
            seed_display = gg.GGTextField(grid, str(self.seed), gg.Location(grid_height - 20, 0))
            seed_display.setFont()
    

if __name__ == "__main__":
    terra = Terrain(50, -100, 600)
    terra.smooth_plot(12)
    grid = gg.GameGrid(800, 800, 1)
    terra.draw_to_grid(grid)
    grid.show()