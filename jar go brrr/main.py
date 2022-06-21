# -*- coding: utf-8 -*-

import ch.aplu.jgamegrid as gg
from Game import *
from Terrain import *
from Lander import *
from Player import *
from GameResults import *
from constants_etc import *
import MainMenu
import Leaderboard
from math import log10


def setup_menu(menu):
    menu.jtf_wndw_height.setText(str(config.WNDW_HEIGHT))
    menu.jtf_wndw_width.setText(str(config.WNDW_WIDTH))

def update_hof(hof):
    playerlist = get_players().values()
    top_players = sorted(
        playerlist, key=lambda player: player.high_score.score, reverse=True
    )[:(100 if len(playerlist) > 100 else len(playerlist))]

    scoretxt = ["", ""]
    c=0
    for player in top_players:
        if c > 99:
            break
        """
        scoretxt[0] += "%d: %s%s%d\nSeed/Smooth: %d / %d\n\n" % (
                    c+1,
                    player.name,
                    "." * (33 - len(player.name) - int(log10(player.high_score.score))),
                    player.high_score.score,
                    player.high_score.seed,
                    player.high_score.smoothing
                )
        """
        scoretxt[0] += str(c+1) + ": " + player.name \
                    + "."*(33 - len(player.name) - int(log10(player.high_score.score))) \
                    + str(player.high_score.score) \
                    + "\nSeed/Smooth: " + str(player.high_score.seed) + " / " \
                    + str(player.high_score.smoothing) + "\n\n"
        #"""
        c+=1

    gamelist = get_games()
    top_games = sorted(gamelist, key=lambda game: game.score, reverse=True)[:(100 if len(gamelist) > 100 else len(gamelist))]

    c=0
    for game in top_games:
        if c > 99:
            break
        """
        scoretxt[1] += "%d: %s%s%d\nSeed/Smooth: %d / %d\n\n" % (
                    c+1,
                    game.playername,
                    "." * (33 - len(game.playername) - int(log10(game.score))),
                    game.score,
                    game.seed,
                    game.smoothing
                )
        """
        scoretxt[1] += str(c+1) + ": " + game.playername \
                    + "."*(33 - len(game.playername) - int(log10(game.score))) \
                    + str(game.score) \
                    + "\nSeed/Smooth: " + str(game.seed) + " / " \
                    + str(game.smoothing) + "\n\n"
        #"""
        c+=1
    
    hof.updateBoards(*scoretxt)
        

def onclick_play(event, menu):
    playername = str(menu.jtf_name.getText())
    if len(playername) > 24:
        return

    seed = menu.jtf_seed.getText()
    if seed == "":
        seed = None
    else:
        seed = int(seed)
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
        menu.jtf_wndw_width.setText(str(config.WNDW_WIDTH))
    
    config.commit_to_ini()
    
def onclick_hof(event, hof):
    if hof.isVisible(): hof.setVisible(False) 
    else:
        hof.setVisible(True)
        update_hof(hof)


def bind_onclicks(menu, hof):
    menu.jbtn_save_settings.actionPerformed = lambda event: onclick_save_settings(event, menu)
    menu.jbtn_play.actionPerformed = lambda event: onclick_play(event, menu)
    menu.jbtn_hof.actionPerformed = lambda event: onclick_hof(event, hof)

def play_game(playername, seed=None): # CHANGE
    game = LunarGame(playername, config.WNDW_WIDTH, config.WNDW_HEIGHT, seed=seed)
    game.play()

def main():
    menu = MainMenu()
    hof = Leaderboard()
    setup_menu(menu)
    bind_onclicks(menu, hof)


main()