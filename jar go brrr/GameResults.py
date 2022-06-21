# -*- coding: utf-8 -*-

import pickle as p
from constants_etc import *

class GameResult():
    def __init__(self, playername, score, seed, smoothing, time):
        self._playername = playername
        self._score = score
        self._seed = seed
        self._smoothing = smoothing
        self._time = time
    
    @property
    def playername(self):
        return self._playername
    
    @property
    def score(self):
        return self._score
    
    @property
    def seed(self):
        return self._seed

    @property
    def smoothing(self):
        return self._smoothing
    
    @property
    def time(self):
        return self._time

    def save(self):
        games = get_games()
        games += [self]
        with open(config.SAVEDIR+"\\games.pkl", "wb") as f:
            p.dump(games, f)

def get_games():
    games = []
    with open(config.SAVEDIR+'\\games.pkl', 'rb') as f:
        try:
            games += p.load(f)
        except:
            pass
    return games

if __name__ == "__main__":
    print(get_games())