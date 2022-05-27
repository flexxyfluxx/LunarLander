from __future__ import print_function
import ch.aplu.jgamegrid as gg
from java.awt import Font, Color
import random as r

class Terrain():
    def __init__(self, resolution, min, max, seed=r.randint(-2147483648, 2147483647), smoothing=0):
        self.seed = seed
        gen = r.Random(self.seed)
        self.plot = [gen.randint(min, max) for c in range(resolution)]
        self.smoothing = 0
        self.smooth_plot(smoothing)
        
    
    def print_plot(self):
        for c in self.plot:
            for z in range(c):
                print("#", end="")
            print("")
        
    def smooth_plot(self, count):
        for c in range(count):
            self.plot = [(self.plot[c-1] + self.plot[c] + self.plot[c+1]) / 3 for c in range(len(self.plot) - 1)] \
                        + [(self.plot[-2] + self.plot[-1] + self.plot[0]) / 3]
            self.smoothing += 1

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
            seed_display = gg.GGTextField(
                grid,
                "Seed: "+str(self.seed)+"; Smoothing: "+str(self.smoothing),
                gg.Location(10, grid_height - 20),
                True
            )
            seed_display.setFont(Font("Arial", Font.PLAIN, 24))
            seed_display.setTextColor(Color.WHITE)
            seed_display.show()
    

if __name__ == "__main__":
    terra = Terrain(50, 0, 600, smoothing=12)
    grid = gg.GameGrid(800, 800, 1)
    terra.draw_to_grid(grid, True)
    grid.show()