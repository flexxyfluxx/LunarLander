# -*- coding: utf-8 -*-

"""
class LunarGame:
Hier wird das gesamte Spiel an sich verwaltet.
"""

import ch.aplu.jgamegrid as gg
from java.awt import Color
from Terrain import *
from Lander import *
from constants_etc import *


class LunarGame(gg.GameGrid):
    def __init__(self, start_fuel, wndw_width=800, wndw_height=800, terrain_chunksize=8):
        self._wndw_width = wndw_width
        self._wndw_height = wndw_height
        gg.GameGrid.__init__(self, wndw_width, wndw_height, 1, None, True)

        self._terrain_chunksize = terrain_chunksize
        
        self.lander = Lander(
            self,
            SPRITE['lander'],
            1.62,
            start_fuel,
            KEY['w'],
            KEY['s'],
            KEY['a'],
            KEY['d'],
            KEY['space']
        )

        self.terrain = Terrain(self._wndw_width // self._terrain_chunksize, -100, 600)
        self.terrain.smooth_plot(12)
    
    # Pertick Checks
    def act(self):
        if self._wndw_height - self.lander.true_position.y < self.terrain.get_interpolated(self._terrain_chunksize)[self.lander.true_position.get_int_x()] + 8:
            self.lander.do_crash()

    def _setup_grid(self):
        self.setSimulationPeriod(10)
        self.setTitle("Loonar Lander!1 wOOOOO YeaH babY thAtswhativebeenwaitingfor; thatswhatitsallabout! yeaaah!")
        self.addActor(self.lander, gg.Location(0, 50))
        self.terrain.draw_to_grid(self, True)
    
    def play(self):
        self._setup_grid()
        self.show()
        self.doRun()


if __name__ == "__main__":
    game = LunarGame(1000)
    game.play()