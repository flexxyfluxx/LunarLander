# -*- coding: utf-8 -*-

import ch.aplu.jgamegrid as gg
from constants_etc import *
from java.awt import Font
import random as r

class Terrain():
    """
    TERRAIN:
    Das Terrain besteht hier aus Chunks, also kleinen Abschnitten, bei denen jeweils rechts und links eine Höhe gegeben ist.
    Zwischen diesen geg. Werten verläuft das Terrain linear, da dies am einfachsten zu berechnen ist.
    """
    def __init__(self, size, min, max, landing_zone_count=range(4,6), seed=r.randint(-2147483648, 2147483647), smoothing=0):
        self._upper = max
        self._lower = min

        self.size = int(size)
        self.seed = seed
        self.gen = r.Random(self.seed)

        try:
            self._landing_zone_counts = tuple([int(c) for c in landing_zone_count])
        except TypeError:
            self._landing_zone_counts = int(landing_zone_count), # Trailing Comma: lustige Syntax zur Formatierung eines Singleton-Tuples
        except ValueError:
            self._landing_zone_counts = range(4,6)
        
        self.smoothing = 0
        self._make_plot(size, int(round(smoothing)))
        self._add_landing_zones(self.gen.choice(self._landing_zone_counts))
        self.adjust(64)
        self._make_height_map()
        
    def _make_plot(self, size, smoothing, iter=True):
        """
        Es werden die o.g. Randhöhen der Chunks generiert.
        Beim Generator wird nicht nur für 'size', sondern 'size+1' iteriert, da n Chunks insgesamt n+1 Ränder besitzen.
        """
        self._plot = [self.gen.randint(self._lower, self._upper) for c in range(size+1)]
        # Glätte das generierte Terrain so oft wie gegeben
        self.smooth_plot(smoothing, iter) # glätte Plot wie verlangt

    def smooth_plot(self, count, iter=True):
        """
        Jeder Punkt wird gleich dem Durchschnitt der Zelle selbst, der vorherigen und der nachherigen Zelle gesetzt.
        Dadurch wird die Varianz verringert und das Terrain sieht immer flacher aus, je häufiger man das macht.
        """
        for c in range(count):
            self._plot = [ (self._plot[z-1] + self._plot[z] + self._plot[z+1]) / 3 for z in range(len(self._plot) - 1) ] \
                        + [(self._plot[-2] + self._plot[-1] + self._plot[0]) / 3]
        if iter: self.smoothing += count

    def get_interpolated(self, chunksize):
        """
        Erstellt eine vollständige Liste der Terrainhöhe an jeder Stelle.
        Ich verwende hierfür lineare Interpolation, d.h.
        für jeden Chunk addiere ich bei jeder Stelle innerhalb des Chunks
        zur Stelle x=0 *innerhalb* des Chunks die Differenz der Enden des Chunks
        mal die jwlg. Stelle im Chunk.
        """
        out = []
        for c in range(len(self.height_map)-1): # -1, da die Ränder enthalten sind und für n Chunks n+1 Ränder existieren
            out += [ (float(self.height_map[c]) + (float(self.height_map[c+1]) - float(self.height_map[c])) / chunksize * current_step) for current_step in range(chunksize) ]
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
        background.setPaintColor(GRAY)


        # male Fläche
        background.setPaintColor(GRAY)
        interpol = self.get_interpolated(int(ratio))
        for c in range(len(interpol)):
            background.drawLine(c, int(round(grid_height-interpol[c])+1), c, int(round(grid_height)))


        # male Strich oben drauf
        zones_unpacked = self.get_unpacked_zones(1)
        dont_draw = False
        for c in range(5):
            i=0
            for z in range(1, terrain_length+1): # +1, damit das Terrain wirklich von Rand zu Rand geht
                i += 1
                if z in zones_unpacked:
                    height_1 = int(round(grid_height - self._plot[i-1]))+c+1
                    height_2 = int(round(grid_height - self._plot[i-1]))+c+1
                    background.setPaintColor(LANDPAD_COLOR)
                    i -= 1
                    if c == 4:
                        dont_draw = True
                else:
                    height_1 = int(round(grid_height - self._plot[i-1]))+c
                    height_2 = int(round(grid_height - self._plot[i]))+c

                if not dont_draw: background.drawLine(int(round((z-1) * ratio)), height_1, int(round(z * ratio)), height_2)
                background.setPaintColor(WHITE)
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

        zone_positions, zone_lengths = unzip(zipped_zones) # Listen zur Verarbeitung wieder auseinandernehmen (kein Bock auf die ganzen weiteren Indices)
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

        self.zones = zip(zone_positions, zone_lengths) # wieder zippen und speichern

    
    def adjust(self, lower):
        adjustment = min(self._plot) - lower
        self._plot = [c - adjustment for c in self._plot]
        if hasattr(self, 'height_map'): self.height_map = [c - adjustment for c in self.height_map]
        # Da der kleinste Wert beim Plot und bei der Heightmap derselbe ist,
        # können wir den zuvor berechneten Wert wiedreverwenden.


    def next(self):
        self._make_plot(self.size, self.smoothing, iter=False)
        self._add_landing_zones(self.gen.randint(4,6))
        self.adjust(64)
        self._make_height_map()
    
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
    
    def get_unpacked_zones(self, chunksize):
        zones_unpacked = []
        for a,b in self.zones:
            zones_unpacked += list(range(a*chunksize, (a+b)*chunksize))
        return zones_unpacked

    def __len__(self):
        return len(self._plot)-1
    

if __name__ == "__main__":
    terra = Terrain(200, 0, 1200, smoothing=16, seed=1)
    
    grid = gg.GameGrid(1600, 900, 1)
    terra.push_to_grid(grid, True)
    grid.show()