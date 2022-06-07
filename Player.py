# -*- coding: utf-8 -*-

import pickle as p


class Player():
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
        global _players
        _players.update({self.name: self})
        p.dump(_players, open('players.pkl', 'wb'))

    @classmethod
    def load(self, name):
        name = str(name)
        return _players[name] if name in _players.keys() \
            else Player(name)

try:
    _players = dict(p.load(open('players.pkl', 'rb')))
except:
    _players = dict()