# -*- coding: utf-8 -*-

import ch.aplu.jgamegrid as gg
from java.awt import Font
from constants_etc import *

class EndScreen():
    def __init__(self, grid, score, player_name, is_high_score):
        self.grid = grid
        self._center_align = self.grid.getNbHorzCells()/2
        self._is_high_score = is_high_score

        self.gameover_field = gg.GGTextField(self.grid, gg.Location(self._center_align, 80), True)
        self.pname_field = gg.GGTextField(self.grid, gg.Location(self._center_align, 128), True)
        self.with_score_of_field = gg.GGTextField(self.grid, gg.Location(self._center_align, 156), True)
        self.score_field = gg.GGTextField(self.grid, gg.Location(self._center_align, 192), True)
        self.highscore_field = gg.GGTextField(self.grid, gg.Location(self._center_align, 240), True)

        self.gameover_field.setText("GAME OVER")
        self.pname_field.setText(player_name)
        self.with_score_of_field.setText("achieved a final score of")
        self.score_field.setText(str(score))
        self.highscore_field.setText("New high score!")

        self.gameover_field.setFont(Font("Arial", Font.BOLD, 64))
        self.pname_field.setFont(Font("Arial", Font.PLAIN, 48))
        self.with_score_of_field.setFont(Font("Arial", Font.PLAIN, 32))
        self.score_field.setFont(Font("Arial", Font.PLAIN, 72))
        self.highscore_field.setFont(Font("Arial", Font.PLAIN, 32))

        self.gameover_field.setTextColor(WHITE)
        self.pname_field.setTextColor(WHITE)
        self.with_score_of_field.setTextColor(WHITE)
        self.score_field.setTextColor(WHITE)
        self.highscore_field.setTextColor(WHITE)
        
    
    def show(self):
        self.gameover_field.show()
        self.pname_field.show()
        self.with_score_of_field.show()
        self.score_field.show()
        if self._is_high_score: self.highscore_field.show()

        self.gameover_field.setLocation(gg.Location(self._center_align - self.gameover_field.getTextWidth()/2, 80))
        self.pname_field.setLocation(gg.Location(self._center_align - self.pname_field.getTextWidth()/2, 128))
        self.with_score_of_field.setLocation(gg.Location(self._center_align - self.with_score_of_field.getTextWidth()/2, 192))
        self.score_field.setLocation(gg.Location(self._center_align - self.score_field.getTextWidth()/2, 240))
        self.highscore_field.setLocation(gg.Location(self._center_align - self.highscore_field.getTextWidth()/2, 280))

    
    def hide(self):
        self.gameover_field.hide()
        self.pname_field.hide()
        self.with_score_of_field.hide()
        self.score_field.hide()
        if self._is_high_score: self.highscore_field.hide()

if __name__ == "__main__":
    grid = gg.GameGrid(800, 800, 1, None)
    endscreen = EndScreen(grid, 456, "std::player", True)

    grid.show()
    endscreen.show()
    grid.doRun()
