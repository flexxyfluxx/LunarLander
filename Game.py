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
    def __init__(self, start_fuel, wndw_width=960, wndw_height=960, terrain_chunksize=8):
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
            KEY['space'],
            gg.Location(400, 100)
        )

        self.terrain = Terrain(self._wndw_width // self._terrain_chunksize, -100, 600)\
            .smooth_plot(12)\
            .adjust(64)
        self.terrain_interpol = self.terrain.get_interpolated(self._terrain_chunksize)

    """
    Die Kollision von Lander und Terrain muss manuell überprüft werden, da die GGActorCollisionListener-Klasse immer rechteckige Kollisionsformen
    erzeugt, was mit unregelmäßig geformtem Terrain natürlich nicht ideal ist.
    """
    def act(self):
        
        if self._has_lander_collided():
            self.lander.start_crash()

    def _setup_grid(self):
        self.setSimulationPeriod(10)
        self.setTitle("Loonar Lander!1 wOOOOO YeaH babY thAtswhativebeenwaitingfor; thatswhatitsallabout! yeaaah!")
        self.addActor(self.lander, gg.Location(0, 50))
        self.terrain.push_to_grid(self)
    
    def _has_lander_collided(self):
        lander_x = self.lander.true_position.get_int_x()
        return (self._wndw_height - self.lander.true_position.y < self.terrain_interpol[lander_x]+5)\
            or (self._wndw_height - self.lander.true_position.y < self.terrain_interpol[lander_x+3]+5)\
            or (self._wndw_height - self.lander.true_position.y < self.terrain_interpol[lander_x-3]+5)
    
    def play(self):
        self._setup_grid()
        self.show()
        self.doRun()
    
    def do_reset(self):
        self.terrain.next()
        self.lander.setLocation(gg.Location(0, 20))


if __name__ == "__main__":
    game = LunarGame(1000)
    game.play()