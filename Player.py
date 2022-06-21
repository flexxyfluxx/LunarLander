# -*- coding: utf-8 -*-

import pickle as p
from constants_etc import *


class Player():
    try: # CHANGE
        players = dict(p.load(open('players.pkl', 'rb+'))) # CHANGE
    except:
        players = dict()
    def __init__(self, name, scores=[]):
        self.name = str(name)
        self.scores = []
        for score in scores:
            try:
                self.add_score(score)
            except:
                pass
        self.high_score = max(self.scores) if len(self.scores) > 0 \
                        else 0
    
    def add_score(self, score):
        self.scores += [int(score)]
        if score > self.high_score: self.high_score = score
    
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
    print(Player.players)