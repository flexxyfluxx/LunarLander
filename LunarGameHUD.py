# -*- coding: utf-8 -*-

import ch.aplu.jgamegrid as gg

class LunarGameHUD(gg.Actor):
    def __init__(self, grid):
        left_align = 0
        quarter_left_align = grid.getNbHorzCells()//4
        quarter_right_align = grid.getNbHorzCells()//4*3
        right_align = grid.getNbHorzCells()
        row = (0, 20, 40)

        self.score_field = (
            gg.GGTextField(grid, gg.Location(left_align, 0), True),
            gg.GGTextField(grid, gg.Location(quarter_left_align, 0), True)
        )
        self.time_field = (
            gg.GGTextField(grid, gg.Location(left_align, 20), True),
            gg.GGTextField(grid, gg.Location(quarter_left_align, 20), True)
        )
        self.fuel_field = (
            gg.GGTextField(grid, gg.Location(left_align, 40), True),
            gg.GGTextField(grid, gg.Location(quarter_left_align, 40), True)
        )

        self.altitude_field = (
            gg.GGTextField(grid, gg.Location(quarter_right_align, 0), True),
            gg.GGTextField(grid, gg.Location(right_align, 0), True)
        )
        self.y_vel_field = (
            gg.GGTextField(grid, gg.Location(quarter_right_align, 20), True),
            gg.GGTextField(grid, gg.Location(right_align, 20), True)
        )
        self.x_vel_field = (
            gg.GGTextField(grid, gg.Location(quarter_right_align, 40), True),
            gg.GGTextField(grid, gg.Location(right_align, 40), True)
        )

        self.warn_out_of_bounds = gg.GGTextField(grid, gg.Location(quarter_right_align, grid.getNbVertCells() - 20))