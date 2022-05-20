# -*- coding: utf-8 -*-

"""
class LunarGame:
Hier wird das gesamte Spiel an sich verwaltet.
"""

import ch.aplu.jgamegrid as gg
import java.awt.Color as jColors



class LunarGame(gg.GameGrid):
    def __init__(self):
        self.master = gg.GameGrid(800, 800, 1, None, True)
        
#        self.lander = Lander()
#        
#        self.terrain = Terrain()

    def _setup_grid(self):
        self.master.setSimulationSpeed(10)



obj = LunarGame()