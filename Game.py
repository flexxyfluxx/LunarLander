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
from LunarGameHUD import *


class LunarGame(gg.GameGrid):
    def __init__(self, start_fuel, wndw_width=1280, wndw_height=960, terrain_chunksize=8):
        self._wndw_width = wndw_width
        self.wndw_height = wndw_height
        self.score = 0
        self.time = 0
        self._running = True
        gg.GameGrid.__init__(self, wndw_width, wndw_height, 1, None, True)

        self.terrain_chunksize = terrain_chunksize
        
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
        self.lander.set_velocity(80, 0)

        self.terrain = Terrain(self._wndw_width // self.terrain_chunksize, -100, 600)
        self.terrain.smooth_plot(12)
        self.terrain.adjust(64)
        self.terrain_interpol = self.terrain.get_interpolated(self.terrain_chunksize)

        self.hud = LunarGameHUD(self)

        self.setSimulationPeriod(10)
        self.setTitle("Loonar Lander!1 wOOOOO YeaH babY thAtswhativebeenwaitingfor; thatswhatitsallabout! yeaaah!")
        self.addActor(self.lander, gg.Location(0, 50))
        self.terrain.push_to_grid(self)

    """
    Die Kollision von Lander und Terrain muss manuell überprüft werden, da die GGActorCollisionListener-Klasse immer rechteckige Kollisionsformen
    erzeugt, was mit unregelmäßig geformtem Terrain natürlich nicht ideal ist.
    """
    def act(self):
        self.time += 1
        
        if self._has_lander_collided():
            self.lander.start_crash()
        
        self.hud.update()
    
    def _has_lander_collided(self):
        lander_x = self.lander.true_position.get_int_x()
        """
        Sucht nach einer Kollision links, rechts und mittig vom Lander, um Phasing bei steileren Hügeln zu minimieren.
        """
        return (self.wndw_height - self.lander.true_position.y < self.terrain_interpol[lander_x]+5)\
            or (self.wndw_height - self.lander.true_position.y < self.terrain_interpol[lander_x+3]+5)\
            or (self.wndw_height - self.lander.true_position.y < self.terrain_interpol[lander_x-3]+5)
            # Mitte;
            # Rechts;
            # Links
    
    def play(self):
        self.show()
        self.hud.show()
        self.doRun()
    
    def do_reset(self):
        self.terrain.next()
        self.lander.setLocation(gg.Location(0, 20))
    
    def get_secs(self):
        return self.time // 100
    
    def refresh_terrain(self):
        self.terrain.next()
        self.terrain_interpol = self.terrain.get_interpolated(self.terrain_chunksize)


if __name__ == "__main__":
    game = LunarGame(1000)
    game.play()