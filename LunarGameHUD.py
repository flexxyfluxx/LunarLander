# -*- coding: utf-8 -*-

import ch.aplu.jgamegrid as gg
from java.awt import Font, Color

class LunarGameHUD(gg.Actor):
    def __init__(self, grid_or_game):
        self.grid_or_game = grid_or_game
        self._left_align = 0
        self._third_left_align = grid_or_game.getNbHorzCells()//3
        self._third_right_align = grid_or_game.getNbHorzCells()//3*2
        self._right_align = grid_or_game.getNbHorzCells()
        hud_font = Font("Arial", Font.PLAIN, 20)

        self.score_field = (
            gg.GGTextField(grid_or_game, gg.Location(self._left_align, 10), True),
            gg.GGTextField(grid_or_game, gg.Location(self._third_left_align, 10), True)
        )
        self.time_field = (
            gg.GGTextField(grid_or_game, gg.Location(self._left_align, 30), True),
            gg.GGTextField(grid_or_game, gg.Location(self._third_left_align, 30), True)
        )
        self.fuel_field = (
            gg.GGTextField(grid_or_game, gg.Location(self._left_align, 50), True),
            gg.GGTextField(grid_or_game, gg.Location(self._third_left_align, 50), True)
        )

        self.altitude_field = (
            gg.GGTextField(grid_or_game, gg.Location(self._third_right_align, 10), True),
            gg.GGTextField(grid_or_game, gg.Location(self._right_align, 10), True)
        )
        self.y_vel_field = (
            gg.GGTextField(grid_or_game, gg.Location(self._third_right_align, 30), True),
            gg.GGTextField(grid_or_game, gg.Location(self._right_align, 30), True)
        )
        self.x_vel_field = (
            gg.GGTextField(grid_or_game, gg.Location(self._third_right_align, 50), True),
            gg.GGTextField(grid_or_game, gg.Location(self._right_align, 50), True)
        )

        self.warn_out_of_bounds = gg.GGTextField(grid_or_game, gg.Location(self._third_right_align, grid_or_game.getNbVertCells() - 20), True)

        # viele repetitive Aufrufe ._.
        for element in self.score_field:
            element.setFont(hud_font)
        for element in self.time_field:
            element.setFont(hud_font)
        for element in self.fuel_field:
            element.setFont(hud_font)
        for element in self.altitude_field:
            element.setFont(hud_font)
        for element in self.y_vel_field:
            element.setFont(hud_font)
        for element in self.x_vel_field:
            element.setFont(hud_font)
        
        for element in self.score_field:
            element.setTextColor(Color.WHITE)
        for element in self.time_field:
            element.setTextColor(Color.WHITE)
        for element in self.fuel_field:
            element.setTextColor(Color.WHITE)
        for element in self.altitude_field:
            element.setTextColor(Color.WHITE)
        for element in self.y_vel_field:
            element.setTextColor(Color.WHITE)
        for element in self.x_vel_field:
            element.setTextColor(Color.WHITE)
        
        self.warn_out_of_bounds.setTextColor(Color.RED)

        self.score_field[0].setText("Score:")
        self.time_field[0].setText("Time:")
        self.fuel_field[0].setText("Fuel:")
        self.altitude_field[0].setText("Altitude:")
        self.y_vel_field[0].setText("Vert. Velocity:")
        self.x_vel_field[0].setText("Horz. Velocity:")
    
    def update(self):
        try:
            score = self.grid_or_game.score
            secs = self.grid_or_game.get_secs()
            mins = secs//60
            secs %= 60
            lander = self.grid_or_game.lander
            terrain = self.grid_or_game.terrain
        except:
            print("[WARNING] self.grid_or_game missing critical attributes! Handling as pure GameGrid.")
        else:
            self.score_field[1].setText(str(score))
            self.score_field[1].setLocation(gg.Location(self._third_left_align - self.score_field[1].getTextWidth(), 10))
            
            self.time_field[1].setText(str(mins) + ":" + (str(secs) if len(str(secs))==2 else ("0" + str(secs))))
            self.time_field[1].setLocation(gg.Location(self._third_left_align - self.time_field[1].getTextWidth(), 30))

            self.fuel_field[1].setText(str(int(round(lander.fuel))))
            self.fuel_field[1].setLocation(gg.Location(self._third_left_align - self.fuel_field[1].getTextWidth(), 50))

            """
            Falls aufgrund eines Fehlers (zB. Index out of range, wenn der Lander OOB ist) keine Höhe des Landers gefunden werden kann,
            wird diese unter Miteinbezug der Lander-Geschwindigkeit errechnet.
            """
            try:
                self._last_altitude = self.grid_or_game.wndw_height - lander.true_position.y - terrain.get_interpolated(self.grid_or_game.terrain_chunksize)[lander.true_position.get_int_x()]
                self.altitude_field[1].setText(str(round(self._last_altitude)))
            except:
                self._last_altitude -= lander.y_velocity / 100
                self.altitude_field[1].setText(str(round(self._last_altitude)))
            finally:
                self.altitude_field[1].setLocation(gg.Location(self._right_align - self.altitude_field[1].getTextWidth(), 10))

            self.y_vel_field[1].setText(str(round(lander.y_velocity, 2)) + (u"↑" if lander.y_velocity > 0 else u"↓"))
            self.y_vel_field[1].setLocation(gg.Location(self._right_align - self.y_vel_field[1].getTextWidth(), 30))

            self.x_vel_field[1].setText(str(round(abs(lander.x_velocity), 2)) + (u"→" if lander.x_velocity > 0 else u"←"))
            self.x_vel_field[1].setLocation(gg.Location(self._right_align - self.x_vel_field[1].getTextWidth(), 50))
    
            if hasattr(self.grid_or_game, 'out_of_bounds_timer'):
                print("Out of bounds!")
                """
                if self.grid_or_game.out_of_bounds_timer // 50 > 24:
                    if self.warn_out_of_bounds.isVisible(): self.warn_out_of_bounds.hide()
                elif self.grid_or_game.out_of_bounds_timer // 50 < 25:
                    if not self.warn_out_of_bounds.isVisible(): self.warn_out_of_bounds.show()
            else:
                if self.warn_out_of_bounds.isVisible(): self.warn_out_of_bounds.hide()
                """
    
    def show(self):
        for element in self.score_field:
            element.show()
        for element in self.time_field:
            element.show()
        for element in self.fuel_field:
            element.show()
        for element in self.altitude_field:
            element.show()
        for element in self.y_vel_field:
            element.show()
        for element in self.x_vel_field:
            element.show()
        

    def act(self):
        self.update_everything_but_score()
    

if __name__ == "__main__":
    grid = gg.GameGrid(800, 800, 1, None)

    hud = LunarGameHUD(grid)

    grid.show()
    hud.show()
    grid.setSimulationPeriod(1000)
    grid.doRun()