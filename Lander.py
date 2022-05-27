# -*- coding: utf-8 -*-
import ch.aplu.jgamegrid as gg
from math import *
from Floacation import *
from constants_etc import *

class Lander(gg.Actor):
    def __init__(self, grid, sprite, gravity, start_fuel, key_thrust_up, key_thrust_dn,
            key_rotate_left, key_rotate_right, key_kill_thrust):
        self.grid = grid
        scaled_sprite = gg.GGBitmap.getScaledImage(sprite, 0.1, 90)
        
        gg.Actor.__init__(self, True, scaled_sprite)
        self._gravity = gravity
        
        self.x_velocity = 0
        self.y_velocity = 0
        
        self.true_position = Floacation(64, 64)
        
        self.angle = EAST
        
        self.fuel = start_fuel
        self._start_fuel = start_fuel

        self.thrust = 0
        self._thrust_momentum = None
        self._rotate_momentum = None

        self._key_thrust_up = key_thrust_up
        self._key_thrust_dn = key_thrust_dn
        self._key_rotate_left = key_rotate_left
        self._key_rotate_right = key_rotate_right
        self._key_kill_thrust = key_kill_thrust
    
    
    def act(self):
        """
        Erst wird je nach Tastendruck der Schub erhöht/gesenkt
        und die Drehung des Landers gesteuert.
        Dann werden mit momentanem Schub und Drehung die x-/y-Geschwindigkeiten verändert.
        Schließlich bewegt sich der Lander entsprechend der Vektorgeschwindigkeiten.
        """
        # thrust
        if self.grid.isKeyPressed(self._key_kill_thrust):
            self.thrust = 0
        elif self.grid.isKeyPressed(self._key_thrust_up) \
                and self.grid.isKeyPressed(self._key_thrust_dn):
            
            if self._thrust_momentum == LAST_UP:
                self.thrust -= 5 if self.thrust > 0 else 0
                
            elif self._thrust_momentum == LAST_DN:
                self.thrust += 5 if self.thrust < 1000 else 0
        
        elif self.grid.isKeyPressed(self._key_thrust_up) \
                and not self.grid.isKeyPressed(self._key_thrust_dn):
            self.thrust += 5 if self.thrust < 1000 else 0
            self._thrust_momentum = LAST_UP
        
        elif self.grid.isKeyPressed(self._key_thrust_dn) \
                and not self.grid.isKeyPressed(self._key_thrust_up):
            self.thrust -= 5 if self.thrust > 0 else 0
            self._thrust_momentum = LAST_DN
        
        else:
            self._thrust_momentum = None
        # end of thrust

        # rotation
        if self.grid.isKeyPressed(self._key_rotate_left) \
                and self.grid.isKeyPressed(self._key_rotate_right):
            
            if self._rotate_momentum == LAST_LEFT:
                self.turn(5)
                
            elif self._rotate_momentum == LAST_RIGHT:
                self.turn(-5)
        
        elif self.grid.isKeyPressed(self._key_rotate_left) \
                and not self.grid.isKeyPressed(self._key_rotate_right):
            self.turn(-5)
            self._rotate_momentum = LAST_LEFT
        
        elif self.grid.isKeyPressed(self._key_rotate_right) \
                and not self.grid.isKeyPressed(self._key_rotate_left):
            self.turn(5)
            self._rotate_momentum = LAST_RIGHT
        
        else:
            self._rotate_momentum = None
        # end of rotation
        
        
        print(str(self.thrust) +  " | " + str(self.getDirection()) \
            + " || " + str(self.y_velocity) + " | " + str(self.x_velocity))

        self._apply_gravity()
        self._apply_thrust()
        self.true_position.x += self.x_velocity / 100
        self.true_position.y -= self.y_velocity / 100
        self.move()

    
    def move(self):
        self.setX(self.true_position.get_int_x())
        self.setY(self.true_position.get_int_y())

    def get_abs_velocity(self):
        return sqrt(self.x_velocity ** 2 + self.y_velocity ** 2)
    
    def _apply_gravity(self):
        self.y_velocity -= self._gravity / 100
    
    def get_mass(self):
        return config.DRY_MASS + config.FUEL_MASS / self._start_fuel * self.fuel

    def _apply_thrust(self):
        accel = 160 * self.thrust / self.get_mass()
        angle = self.getDirection()
        
        self.x_velocity += (accel * cos(radians(angle))) / 100
        self.y_velocity -= (accel * sin(radians(angle))) / 100

        # TODO subtract fuel
        """
        Da die Gamegrid-Richtungen nicht, wie bei einem normalen
        Koordinatensystem, im Gegenuhrzeigersinn, sondern im Uhrzeigersinn
        verlaufen, muss man für die y-Achse '-=' statt '+=' verwenden.
        Für den x-Wert ist dies nicht nötig.
        """
    
    

if __name__ == "__main__":
    grid = gg.GameGrid(800, 800, 1, None)
    
    lander = Lander(
        grid,
        SPRITE['lander'],
        1.62,
        1000,
        KEY['w'],
        KEY['s'],
        KEY['a'],
        KEY['d'],
        KEY['space']
    )
    
    grid.addActor(lander, lander.true_position.get_int_location(), 270)
    
    grid.setSimulationPeriod(10)
    grid.setTitle("Lander Thruster Physics Test")
    grid.show()
    grid.doRun()