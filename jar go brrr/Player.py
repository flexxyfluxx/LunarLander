# -*- coding: utf-8 -*-

import pickle as p
from constants_etc import *

class Player():

    def __init__(self, name, games=[]):
        self.name = str(name)
        self.games = []
        for game in games:
            try:
                self.add_score(game)
            except:
                pass
        self.high_score = sorted(self.games, key=lambda y: y.score)[-1] if len(self.games) > 0 \
                        else None
    
    def add_game(self, game):
        self.games += [game]
        if self.high_score is None:
            self.high_score = game
        if game.score > self.high_score.score: self.high_score = game
    
    def save(self):
        players = get_players()
        players.update({self.name: self})
        with open(config.SAVEDIR+'\\players.pkl', 'wb') as f:
            p.dump(players, f)

    @classmethod
    def load(self, name):
        players = get_players()
        name = str(name)
        return players[name] if name in players.keys() \
            else Player(name)

def get_players():
    players = dict()
    with open(config.SAVEDIR+'\\players.pkl', 'rb') as f:
        try:
            players.update(dict(p.load(f)))
        except:
            pass
    return players

if __name__ == "__main__":
    print(Player.players())