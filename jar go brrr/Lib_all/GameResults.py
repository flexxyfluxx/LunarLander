# -*- coding: utf-8 -*-

import pickle as p

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
        global _games
        _games += [self]
        with open("games.pkl", "wb") as f:
            p.dump(_games, f)
    
    @classmethod
    def games(self):
        return _games

_games = []
with open('games.pkl', 'rb') as f:
    try:
        _games += p.load(f)
    except:
        pass

if __name__ == "__main__":
    print(_games)