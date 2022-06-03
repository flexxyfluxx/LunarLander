# -*- coding: utf-8 -*-

from __future__ import print_function
import ch.aplu.jgamegrid as gg
from constants_etc import *
from java.awt import Font
import random as r

class Terrain():
    def __init__(self, size, min, max, landing_zone_count=None, seed=r.randint(-2147483648, 2147483647), smoothing=0):
        self._upper = max
        self._lower = min

        self.size = int(size)
        self.seed = seed
        self.gen = r.Random(self.seed)

        if landing_zone_count is None:
            self._landing_zone_counts = range(4,6)
        else:
            try:
                self._landing_zone_counts = [int(c) for c in landing_zone_count]
            except TypeError:
                self._landing_zone_counts = int(landing_zone_count), # Trailing Comma, damit's technisch noch als Iterable zählt
            except ValueError:
                self._landing_zone_counts = range(4,6)
        
        self.smoothing = 0
        self._make_plot(size, int(round(smoothing)))
        self._add_landing_zones(self.gen.choice(self._landing_zone_counts))
        self.adjust(64)
        self._make_height_map()
        
    def _make_plot(self, size, smoothing):
        self._plot = [self.gen.randint(self._lower, self._upper) for c in range(size+1)]
        self.smooth_plot(smoothing)

    def print_plot(self):
        for c in self._plot:
            for z in range(c):
                print("#", end="")
            print("")
        
    def smooth_plot(self, count, iter=True):
        for c in range(count):
            self._plot = [(self._plot[c-1] + self._plot[c] + self._plot[c+1]) / 3 for c in range(len(self._plot) - 1)] \
                        + [(self._plot[-2] + self._plot[-1] + self._plot[0]) / 3]
            if iter: self.smoothing += 1

    def get_interpolated(self, chunksize):
        out = []
        for c in range(len(self.height_map)-1):
            out += [ (float(self.height_map[c]) + (float(self.height_map[c+1]) - float(self.height_map[c])) / chunksize * current_step) for current_step in range(chunksize) ]
        
        # Deckel drauf!
        out += [self._plot[-1]]

        return out
    
    def push_to_grid(self, grid, show_seed=True):
        terrain_length = len(self._plot)-1
        ratio = grid.getNbHorzCells() / float(terrain_length)
            # Aus irgendeinem Grund wird die (normale, fließkommazahlige) Division zweier Ints
            # als ganzzahlige Division interpretiert, d.h.
            # 5 / 2 == 5 // 2
            #
            # Ich muss also eine der Zahlen explitzit zum Float machen -_-
        grid_height = grid.getNbVertCells()
        background = grid.getBg()
        background.setLineWidth(1)

        zones_unpacked = []
        for a,b in self.zones:
            zones_unpacked += list(range(a,a+b))

        dont_draw = False
        for c in range(5):
            i=0
            for z in range(1, terrain_length+1): # +1, damit das Terrain wirklich von Rand zu Rand geht
                i += 1
                if z in zones_unpacked:
                    height_1 = int(round(grid_height - self._plot[i-1]))+c+1
                    height_2 = int(round(grid_height - self._plot[i-1]))+c+1
                    background.setPaintColor(WHITE)
                    i -= 1
                    if c == 4:
                        dont_draw = True
                else:
                    height_1 = int(round(grid_height - self._plot[i-1]))+c
                    height_2 = int(round(grid_height - self._plot[i]))+c

                if not dont_draw: background.drawLine(int(round((z-1) * ratio)), height_1, int(round(z * ratio)), height_2)
                background.setPaintColor(GRAY)
                dont_draw = False
        
        if show_seed:
            seed_display = gg.GGTextField(
                grid,
                "Seed: "+str(self.seed)+"; Smoothing: "+str(self.smoothing),
                gg.Location(10, grid_height - 20),
                True
            )
            seed_display.setFont(Font("Arial", Font.PLAIN, 24))
            seed_display.setTextColor(WHITE)
            seed_display.show()
    
    def _add_landing_zones(self, zone_count): # Füllt ein Array mit Landezonen im Format [[Position, Größe], ...]; sortiert nach Größe.
        terr_length = len(self._plot)
        zone_positions = []
        zone_lengths = []
        for c in range(zone_count):
            zone_pos = self.gen.randint(2, terr_length-1)
            while zone_pos in zone_positions:
                zone_pos = self.gen.randint(2, terr_length-1)
            zone_positions += [zone_pos]

            zone_len = self.gen.randint(3, 8)
            while zone_len in zone_lengths:
                zone_len = self.gen.randint(3, 8)
            zone_lengths += [zone_len]

        zipped_zones = zip(zone_positions, zone_lengths) # Listen zusammenfügen, um die Zonen nach Position zu sortieren
        zipped_zones.sort(key=lambda y: y[0])

        zone_positions, zone_lengths = zip(*zipped_zones) # Listen zur Verarbeitung wieder auseinandernehmen (kein Bock auf die ganzen weiteren Indices)
        zone_positions, zone_lengths = list(zone_positions), list(zone_lengths) # explizit zu Listen machen (zip gibt Tupel zurück)


            # Zonen-Positionen prüfen; korrigieren:
        for c in range(len(zone_positions)-1, 1, -1):
            if zone_positions[c] + zone_lengths[c] > terr_length-2: # Falls Zone über das rechte Terrain-Ende hinausgeht: korrigieren.
                zone_positions[c] = terr_length - zone_lengths[c] - 2
            if zone_positions[c] - zone_positions[c-1] - zone_lengths[c-1] < 1: # Falls Abstand zum nächsten linken Pad < 1: linkes Pad korrigieren.
                zone_positions[c-1] = zone_positions[c] - zone_lengths[c-1] - 1
        for c in range(1, len(zone_positions)-1):
            if zone_positions[c-1] < 2: # Falls Zone über das linke Ende hinausgeht: korrigieren.
                zone_positions[c-1] = 2
            if zone_positions[c] - zone_positions[c-1] - zone_lengths[c-1] < 1: # Falls Abstand zom nächsten rechten Pad < 1: rechtes Pad korrigieren.
                zone_positions[c] = zone_positions[c-1] + zone_lengths[c-1] + 1

        self.zones = zip(zone_positions, zone_lengths) # 

    
    def adjust(self, lower):
        adjustment = min(self._plot) - lower
        self._plot = [c - adjustment for c in self._plot]
        if hasattr(self, 'height_map'): self.height_map = [c - adjustment for c in self.height_map]
        # Da der kleinste Wert beim Plot und bei der Heightmap derselbe ist,
        # können wir den zuvor berechneten Wert wiedreverwenden.


    def next(self):
        self._make_plot(self.size, self.smoothing, iter=False)
        self._add_landing_zones(self.gen.randint(4,6))
        self._make_height_map()
        self.adjust(64)
    
    def _make_height_map(self):
        zones_unpacked = []
        for a,b in self.zones:
            zones_unpacked += list(range(a,a+b))

        self.height_map = [self._plot[0]]

        i=1
        for c in range(1, len(self._plot)):
            if c in zones_unpacked:
                self.height_map += [self._plot[i-1]]
            else:
                self.height_map += [self._plot[i]]
                i+=1

    

if __name__ == "__main__":
    terra = Terrain(200, 0, 1200, smoothing=13, seed=2096571153)
    
    grid = gg.GameGrid(1600, 900, 1)
    terra.push_to_grid(grid, True)
    grid.show()