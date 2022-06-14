# -*- coding: utf-8 -*-

import ch.aplu.jgamegrid as gg
from Game import *
from Terrain import *
from Lander import *
from Player import *
from constants_etc import *
import MainMenu


def setup_menu(menu):
    menu.jtf_wndw_height.setText(str(config.WNDW_HEIGHT))
    menu.jtf_wndw_width.setText(str(config.WNDW_WIDTH))


def onclick_play(event, menu):
    playername = str(menu.jtf_name.getText())
    seed = menu.jtf_seed.getText()
    if seed == "":
        seed = None
    else:
        seed = int(seed)
    menu.dispose()
    play_game(playername, seed)

def onclick_save_settings(event, menu):
    try:
        config.write_wndw_height(menu.jtf_wndw_height.getText())
    except:
        pass
    finally:
        menu.jtf_wndw_height.setText(str(config.WNDW_HEIGHT))
    
    try:
        config.write_wndw_width(menu.jtf_wndw_width.getText())
    except:
        pass
    finally:
        menu.jtf_wndw_height.setText(str(config.WNDW_WIDTH))


def bind_onclicks(menu):
    menu.jbtn_save_settings.actionPerformed = lambda event: onclick_save_settings(event, menu)
    menu.jbtn_play.actionPerformed = lambda event: onclick_play(event, menu)

def play_game(playername, seed=None): # CHANGE
    game = LunarGame(playername, config.WNDW_WIDTH, config.WNDW_HEIGHT, seed=seed)
    game.play()


if __name__ == "__main__":
    menu = MainMenu()
    setup_menu(menu)
    bind_onclicks(menu)