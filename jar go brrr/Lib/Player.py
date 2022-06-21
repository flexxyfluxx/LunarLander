# -*- coding: utf-8 -*-

import pickle as p

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
        global _players
        _players.update({self.name: self})
        with open('players.pkl', 'wb') as f:
            p.dump(_players, f)

    @classmethod
    def load(self, name):
        name = str(name)
        return _players[name] if name in _players.keys() \
            else Player(name)
    
    @classmethod
    def players(self):
        return _players

_players = dict()
with open('players.pkl', 'rb') as f:
    try:
        _players.update(dict(p.load(f)))
    except:
        pass

if __name__ == "__main__":
    print(Player.players())