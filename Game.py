# -*- coding: utf-8 -*-

"""
class LunarGame:
Hier wird das gesamte Spiel an sich verwaltet.
"""

from EndScreen import EndScreen
import ch.aplu.jgamegrid as gg
from time import localtime, strftime
from Terrain import *
from Lander import *
from constants_etc import *
from LunarGameHUD import *
from Player import *
from EndScreen import *

class LunarGame(gg.GameGrid):
    def __init__(self, player, wndw_width=1280, wndw_height=960, terrain_chunksize=8, seed=None):
        self.start_time = localtime()
        self.wndw_width = wndw_width
        self.wndw_height = wndw_height
        self.score = 0
        self.time = 0
        gg.GameGrid.__init__(self, wndw_width, wndw_height, 1, None, True)

        self.terrain_chunksize = terrain_chunksize

        self.player = Player.load(player)
        
        self.lander = Lander(
            self, # übergebe Selbst als grid_or_game
            [ # Liste an Sprites
                SPRITE['lander'], # Zero Thrust;
                SPRITE['lander_exp01'], # Explosion Sprites
                SPRITE['lander_exp02'],
                SPRITE['lander_exp03'],
                SPRITE['lander_exp04'],
                SPRITE['lander_exp05'],
                SPRITE['lander_exp06'],
                SPRITE['lander_exp07'],
                SPRITE['lander_exp08'],
                SPRITE['lander_exp09'],
                SPRITE['lander_exp10'],
                SPRITE['lander_lthr1'], # Low Thrust Animation
                SPRITE['lander_lthr2'],
                SPRITE['lander_hthr1'], # High Thrust Animation
                SPRITE['lander_hthr2']
            ],
            1.62, # Gravitationskonstante
            KEY['w'], # Thrust ↑
            KEY['s'], # Thrust ↓
            KEY['a'], # Rotate ↺
            KEY['d'], # Rotate ↻
            KEY['q'], # Thrust → 0
            KEY['e'], # Thrust → max
            gg.Location(0,20) # Startpos.
        )
        self.lander.set_velocity(40, 0)

        if seed is None:
            self.terrain = Terrain(int(round(self.wndw_width / self.terrain_chunksize)), -100, 600, smoothing=config.SMOOTHING) # CHANGE
        else:
            self.terrain = Terrain(int(round(self.wndw_width / self.terrain_chunksize)), -100, 600, smoothing=config.SMOOTHING, seed=seed) # CHANGE
        self.terrain_interpol = self.terrain.get_interpolated(self.terrain_chunksize)
        self.landing_zones = self.terrain.get_unpacked_zones(self.terrain_chunksize)
        

        self.hud = LunarGameHUD(self)

        self.setSimulationPeriod(10)
        self.setTitle("Loonar Lander!1 wOOOOO YeaH babY thAtswhativebeenwaitingfor; thatswhatitsallabout! yeaaah!")
        self.addActor(self.lander, gg.Location(0, 50))
        self.terrain.push_to_grid(self)
        self.hud.show()

    """
    Die Kollision von Lander und Terrain muss mathematisch überprüft werden, da es (afaik) keinen (einfacheren) Weg gibt,
    dies mit gg.GGActorCollisionListener zu erreichen.
    """
    def act(self):
        self.time += 1
        try:
            if hasattr(self, 'out_of_bounds_timer'):
                if not self._is_lander_out_of_bounds():
                    del self.out_of_bounds_timer
                    return
                if self.out_of_bounds_timer > 1000:
                    self.do_crash()
                    del self.out_of_bounds_timer
                    return
                self.out_of_bounds_timer += 1
                return
            
            self._check_lander_state()
        finally:
            self.hud.update()
    
    def play(self):
        self.show()
        self.hud.show()
        self.doRun()
    
    def do_reset(self):
        self.terrain.next()
        self.lander.setLocation(gg.Location(10, 64))
    
    def get_secs(self):
        return self.time // 100
    
    def refresh_terrain(self):
        self.terrain.next()
        self.terrain_interpol = self.terrain.get_interpolated(self.terrain_chunksize)
        self.landing_zones = self.terrain.get_unpacked_zones(self.terrain_chunksize)
    
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
            out = (self.wndw_height - lander_y < self.terrain_interpol[lander_x]+8) # Mitte
        except:
            pass
        try:
            out = out or (self.wndw_height - lander_y < self.terrain_interpol[lander_x+8]+8) # Rechts
        except:
            pass
        try:
            out = out or (self.wndw_height - lander_y < self.terrain_interpol[lander_x-8]+8) # Links
        except:
            pass

        return out
    
    def _is_lander_out_of_bounds(self):
        lander_x = self.lander.true_position.x
        lander_y = self.lander.true_position.y
        return (lander_x + 8 < 0) \
            or (lander_y + 8 < 0) \
            or (lander_x - 8 > self.wndw_width) \
            or (lander_y - 8 > self.wndw_height)
    
    def _could_lander_land(self):
        # Ist der Lander theoretisch in der Lage zu landen, wenn er in dem Tick auf den Boden trifft?
        return (self.lander.true_position.get_int_x()+8) in self.landing_zones \
            and (self.lander.true_position.get_int_x()) in self.landing_zones \
            and abs(self.lander.x_velocity) <= 3 \
            and abs(self.lander.y_velocity) <= 10 \
            and self.lander.getDirection() in range(260, 281)
    
    def _check_lander_state(self):
        if hasattr(self.lander, 'crash_timer'): return
        if hasattr(self.lander, 'land_timer'): return
        if self._is_lander_out_of_bounds():
            self.out_of_bounds_timer = 0
            return
        
        if self._has_lander_collided():
            if self._could_lander_land():
                self.do_land()
                return
            self.do_crash()

    def do_crash(self):
        if self.lander.isVisible(): # CHANGE
            self.lander.start_crash()
            self.score += 15
    
    def do_land(self):
        self.lander.start_land()
        multiplier = self._get_zone_multiplier(self.lander.true_position.get_int_x())
        self.score += 50 * multiplier
        self.lander.fuel += 500 * multiplier
        self.hud.update()

    def _get_zone_multiplier(self, x):
        """
        Finde den Multiplier der Landezone, in der der Lander sich befindet.
        Geschieht in Abhängigkeit zur Landezonenlänge:
            bei len=3 (minimal): 5x
            bei len=4: 4x
            ...
            bei len=7: 1x
            bei len=8: 1x
        
        Falls der Lander(-ursprung) nicht auf einer Landezone liegt, gebe 0 zurück.
        """
        if x not in self.landing_zones: return 0

        terr_positions, terr_lengths = unzip(self.terrain.zones)

        # Finde das linke Ende der Zone, da in terrain.zones die linken Ränder der Landezonen gespeichert sind
        x //= self.terrain_chunksize
        while x not in terr_positions:
            x -= 1
        # Finde den entsprechenden Index (geht, da die selbe Position nicht mehrmals vorkommen kann)
        index = getindex(x, terr_positions)
        local_length = terr_lengths[index]

        return (8 - local_length) if local_length < 8 else 1
    
    def next_map(self):
        if self.lander.fuel == 0:
            self.do_end()
            return
        self.terrain.next()
        self.terrain_interpol = self.terrain.get_interpolated(self.terrain_chunksize)
        self.landing_zones = self.terrain.get_unpacked_zones(self.terrain_chunksize)
        self.getBg().clear()
        self.terrain.push_to_grid(self)
        self.lander.show()
        self.lander.setDirection(0)
        self.lander.setLocation(gg.Location(10, 64))
        self.lander.set_velocity(40, 0)
    
    def do_end(self):
        self.hud.hide()
        self.save()
        self.player.add_score(self.score)
        self.player.save()
        EndScreen(self, self.score, self.player.name, True if self.score == self.player.high_score else False).show()
        self.doPause()
    
    def save(self):
        time = strftime("%Y-%m-%d %H:%M:%S", self.start_time)
        with open('history.txt', 'a+') as f:
            f.write(
                time+": ["+self.player.name+"] Achieved score of "+str(self.score)+" on seed "+str(self.terrain.seed)+" with smoothing "+str(self.terrain.smoothing)+"."
                    + (" (New high score! :DDD)\n" if self.score > self.player.high_score else "\n")
            )