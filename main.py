# -*- coding: utf-8 -*-

import ch.aplu.jgamegrid as gg
from Game import *
from Terrain import *
from Lander import *
from Player import *
from constants_etc import *

def main():
    playername = str(raw_input("Enter player name!"))
    game = LunarGame(playername)
    game.play()

if __name__ == "__main__":
    main()