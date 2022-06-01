from __future__ import print_function
import ch.aplu.jgamegrid as gg
from java.awt import Font, Color
import random as r

class Terrain():
    def __init__(self, size, min, max, landing_zone_count=None, seed=r.randint(-2147483648, 2147483647), smoothing=0):
        self._upper = max
        self._lower = min

        self.size = int(size)
        self.seed = seed
        self.gen = r.Random(self.seed)
        self.smoothing = 0
        self._make_plot(size, int(smoothing))
        self.adjust(64)
        
    
    def _make_plot(self, size, smoothing):
        self.plot = [self.gen.randint(self._lower, self._upper) for c in range(size+1)]
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

    def get_interpolated(self, chunksize):
        out = []
        for c in range(len(self.plot)-1):
            out += [ (float(self.plot[c]) + (float(self.plot[c+1]) - float(self.plot[c])) / chunksize * current_step) for current_step in range(chunksize) ]
        
        # Deckel drauf!
        out += [self.plot[-1]]

        return out
    
    def push_to_grid(self, grid, show_seed=True):
        terrain_length = len(self.plot)-1
        ratio = grid.getNbHorzCells() / terrain_length
        grid_height = grid.getNbVertCells()
        background = grid.getBg()
        background.setLineWidth(1)

        for c in range(5):
            for z in range(1, terrain_length+1):
                background.drawLine(int(round((z-1) * ratio)), grid_height - self.plot[z-1] + c, int(round(z * ratio)), grid_height - self.plot[z] + c)
        
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
    
    def adjust(self, lower):
        adjustment = min(self.plot) - lower
        self.plot = [c - adjustment for c in self.plot]


    def next(self):
        tmp_smoothing = self.smoothing
        self._make_plot(self.size, self.smoothing)
        self.adjust(10)
        self.smoothing = tmp_smoothing
    

if __name__ == "__main__":
    terra = Terrain(100, 0, 1200, smoothing=13, seed=11)
    grid = gg.GameGrid(800, 800, 1)
    terra.push_to_grid(grid, True)
    grid.show()