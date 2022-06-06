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
from Player import *

class LunarGame(gg.GameGrid):
    def __init__(self, player_name, wndw_width=1280, wndw_height=960, terrain_chunksize=8):
        self.wndw_width = wndw_width
        self.wndw_height = wndw_height
        self.score = 0
        self.time = 0
        self._running = True
        gg.GameGrid.__init__(self, wndw_width, wndw_height, 1, None, True)

        self.terrain_chunksize = terrain_chunksize

        self.player = Player.load(player_name)
        self.score = 0
        
        self.lander = Lander(
            self,
            SPRITE['lander'],
            1.62,
            KEY['w'],
            KEY['s'],
            KEY['a'],
            KEY['d'],
            KEY['q'],
            KEY['e'],
            gg.Location(0,20)
        )
        self.lander.set_velocity(40, 0)

        self.terrain = Terrain(int(round(self.wndw_width / self.terrain_chunksize)), -100, 600, smoothing=13)
        self.terrain_interpol = self.terrain.get_interpolated(self.terrain_chunksize)

        self.hud = LunarGameHUD(self)

        self.setSimulationPeriod(10)
        self.setTitle("Loonar Lander!1 wOOOOO YeaH babY thAtswhativebeenwaitingfor; thatswhatitsallabout! yeaaah!")
        self.addActor(self.lander, gg.Location(0, 50))
        self.terrain.push_to_grid(self)

    """
    Die Kollision von Lander und Terrain muss mathematisch überprüft werden, da die GGActorCollisionListener-Klasse immer rechteckige Kollisionsformen
    erzeugt, was mit unregelmäßig geformtem Terrain natürlich nicht ideal ist.
    """
    def act(self):
        self.time += 1

        if hasattr(self, 'out_of_bounds_timer'):
            if not self._is_lander_out_of_bounds():
                del self.out_of_bounds_timer
            elif self.out_of_bounds_timer > 1000:
                self.lander.start_crash()
                del self.out_of_bounds_timer
            try:
                self.out_of_bounds_timer += 1
            except:
                pass
            finally:
                return

        self._check_lander_state()
        
        self.hud.update()
    
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
    
    def _has_lander_collided(self):
        lander_x = self.lander.true_position.get_int_x() # Int, da als Array-Index verwendet
        lander_y = self.lander.true_position.y # für erhöhte Präzision kein Int
        """
        Sucht nach einer Kollision links, rechts und mittig vom Lander, um Phasing bei steileren Hügeln zu minimieren.
        Falls der Lander Out of Bounds ist, wird False zurückgegeben, da dafür andere Methoden verwendet werden.
        Der Lander ist nur dann Out of Bounds, wenn er ganz vom Bildschirm verschwunden ist.
        Es sind also Try-Excepts nötig, damit kein Fehler entsteht, wenn der Lander nicht vollständig OOB ist.
        """
        out = False
        try:
            out = (self.wndw_height - lander_y < self.terrain_interpol[lander_x]+5) # Mitte
        except:
            pass
        try:
            out = out or (self.wndw_height - lander_y < self.terrain_interpol[lander_x+5]+5) # Rechts
        except:
            pass
        try:
            out = out or (self.wndw_height - lander_y < self.terrain_interpol[lander_x-5]+5) # Links
        except:
            pass

        return out
    
    def _is_lander_out_of_bounds(self):
        lander_x = self.lander.true_position.x
        lander_y = self.lander.true_position.y
        return (lander_x + 3 < 0)\
            or (lander_x - 3 > self.wndw_width)\
            or (lander_y + 3 < 0)\
            or (lander_y - 3 > self.wndw_height)
        
    def _check_lander_state(self):
        if self._is_lander_out_of_bounds():
            self.out_of_bounds_timer = 0
            return
        
        if self._has_lander_collided():
            self.lander.start_crash()



if __name__ == "__main__":
    game = LunarGame(1000)
    game.play()