# -*- coding: utf-8 -*-
import ch.aplu.jgamegrid as gg
from math import *
from Floacation import *
from constants_etc import *

class Lander(gg.Actor):
    def __init__(self, grid_or_game, sprites, gravity, key_thrust_up, key_thrust_dn, key_rotate_left, key_rotate_right, key_kill_thrust, key_max_thrust, start_location):
        self.grid_or_game = grid_or_game

        # geg. Sprite runterskalieren
        
        scaled_sprites = gg.GGBitmap.getScaledImage(sprites, 1, 90) if isinstance(sprites, str)\
                    else [gg.GGBitmap.getScaledImage(sprite, 1, 90) for sprite in sprites]
        
        gg.Actor.__init__(self, True, scaled_sprites)
        self._gravity = gravity
        
        # Geschwindigkeitsvektoren initialisieren
        self.x_velocity = 0
        self.y_velocity = 0
        
        # "wahre" Location als Floacation speichern, um Nachkommastellen nicht zu verlieren
        self.true_position = Floacation(start_location.x, start_location.y)
        
        self.fuel = config.FUEL_MASS # Start-Treibstoff aus der Config holen

        # Thrust-Attribute initialisieren
        self.thrust = 0
        self._thrust_momentum = None
        self._rotate_momentum = None

        # Keybinds speichern
        self._key_thrust_up = key_thrust_up
        self._key_thrust_dn = key_thrust_dn
        self._key_rotate_left = key_rotate_left
        self._key_rotate_right = key_rotate_right
        self._key_kill_thrust = key_kill_thrust
        self._key_max_thrust = key_max_thrust

        self._thrust_flickerer = 0


    def set_velocity(self, x_vel=0, y_vel=0):
        self.x_velocity = x_vel
        self.y_velocity = y_vel
    
    def act(self):
        """
        Erst wird je nach Tastendruck der Schub erhöht/gesenkt
        und die Drehung des Landers gesteuert.
        Dann werden mit momentanem Schub und Drehung die x-/y-Geschwindigkeiten verändert.
        Schließlich bewegt sich der Lander entsprechend der Vektorgeschwindigkeiten.
        """

        if not self.isVisible(): return

        if hasattr(self, 'crash_timer'):
            if self.crash_timer >= 100:
                self.hide()
                if self.crash_timer >= 110:
                    delattr(self, 'crash_timer')
                    self.delay(1000)
                    self.grid_or_game.next_map()
                    return
            self.show(self.crash_timer // 10)
            self.crash_timer += 1
            return
        
        if hasattr(self, 'land_timer'):
            if self.land_timer > 50:
                if self.land_timer > 100:
                    delattr(self, 'land_timer')
                    self.delay(1000)
                    self.grid_or_game.next_map()
                    return
                self.show(0)
                self.land_timer += 1
                return
            self.show(15)
            self.land_timer += 1
            return

        if self.fuel <= 0:
            self.show(0)
            if self._last_rotation == LAST_RIGHT: self.turn(2)
            elif self._last_rotation == LAST_LEFT: self.turn(-2)
            self._apply_gravity()
            self.move()
            return

        # thrust
        if self.grid_or_game.isKeyPressed(self._key_kill_thrust):
            self.thrust = 0

        elif self.grid_or_game.isKeyPressed(self._key_max_thrust):
            self.thrust = config.THRUST_SCALE

        elif self.grid_or_game.isKeyPressed(self._key_thrust_up) \
                and self.grid_or_game.isKeyPressed(self._key_thrust_dn):
            
            if self._thrust_momentum == LAST_UP:
                self.thrust -= 5 if self.thrust > 0 else 0
                
            elif self._thrust_momentum == LAST_DN:
                self.thrust += 5 if self.thrust < config.THRUST_SCALE else 0
        
        elif self.grid_or_game.isKeyPressed(self._key_thrust_up) \
                and not self.grid_or_game.isKeyPressed(self._key_thrust_dn):
            self.thrust += 5 if self.thrust < config.THRUST_SCALE else 0
            self._thrust_momentum = LAST_UP
        
        elif self.grid_or_game.isKeyPressed(self._key_thrust_dn) \
                and not self.grid_or_game.isKeyPressed(self._key_thrust_up):
            self.thrust -= 5 if self.thrust > 0 else 0
            self._thrust_momentum = LAST_DN
        
        else:
            self._thrust_momentum = None
            self._last_rotation = None
        # end of thrust

        # rotation
        if self.grid_or_game.isKeyPressed(self._key_rotate_left) \
                and self.grid_or_game.isKeyPressed(self._key_rotate_right):
            
            if self._rotate_momentum == LAST_LEFT:
                self.turn(2)
                self.fuel -= 1
                self._last_rotation = LAST_RIGHT
                
            elif self._rotate_momentum == LAST_RIGHT:
                self.turn(-2)
                self.fuel -= 1
                self._last_rotation = LAST_LEFT
        
        elif self.grid_or_game.isKeyPressed(self._key_rotate_left) \
                and not self.grid_or_game.isKeyPressed(self._key_rotate_right):
            self.turn(-2)
            self.fuel -= 1
            self._rotate_momentum = LAST_LEFT
            self._last_rotation = LAST_LEFT
        
        elif self.grid_or_game.isKeyPressed(self._key_rotate_right) \
                and not self.grid_or_game.isKeyPressed(self._key_rotate_left):
            self.turn(2)
            self.fuel -= 1
            self._rotate_momentum = LAST_RIGHT
            self._last_rotation = LAST_RIGHT
        
        else:
            rounded_direction = self.getDirection()
            rounded_direction /= 15
            rounded_direction = round(rounded_direction)
            rounded_direction *= 15
            self.setDirection(rounded_direction)
            self._rotate_momentum = None
        # end of rotation
        
        if self.thrust > 0:
            if self.thrust < config.THRUST_SCALE/2:
                self.show(11 if self._thrust_flickerer < 5 else 12)
            else:
                self.show(13 if self._thrust_flickerer < 5 else 14)
        
        if self.thrust == 0 or self.fuel <= 0:
            self.show(0)
        
        self._thrust_flickerer += 1
        if self._thrust_flickerer > 10:
            self._thrust_flickerer = 0

        self.print_stats()
        

        self._apply_gravity()
        self._apply_thrust()
        self.move()

    
    def move(self):
        self.true_position.x += self.x_velocity / 100
        self.true_position.y -= self.y_velocity / 100
        self.setX(self.true_position.get_int_x())
        self.setY(self.true_position.get_int_y())

    def get_abs_velocity(self):
        return sqrt(self.x_velocity ** 2 + self.y_velocity ** 2)
    
    def _apply_gravity(self):
        self.y_velocity -= self._gravity / 100
    
    def get_mass(self):
        return config.DRY_MASS + self.fuel

    def _apply_thrust(self):
        spent_fuel = config.FUEL_CONSUMPTION / config.THRUST_SCALE * self.thrust / 100
        mass = self.get_mass()


        accel = -config.FUEL_VELOCITY * log(1-(spent_fuel / mass))
        print(accel)

        angle = self.getDirection()
        
        self.x_velocity += (accel * cos(radians(angle)))
        self.y_velocity -= (accel * sin(radians(angle)))
        """
        Da die Gamegrid-Richtungen nicht, wie bei einem normalen
        Koordinatensystem, im Gegenuhrzeigersinn, sondern im Uhrzeigersinn
        verlaufen, muss man für die y-Achse '-=' statt '+=' verwenden.
        Für den x-Wert ist dies nicht nötig.
        """

        self.fuel -= spent_fuel
        if self.fuel < 0: self.fuel = 0
    
    def start_crash(self):
        self.set_velocity(0,0)
        self.thrust = 0
        self.crash_timer = 0
    
    def start_land(self):
        self.set_velocity(0,0)
        self.thrust = 0
        self.land_timer = 0
    
    def setLocation(self, location):
        self.true_position.x, self.true_position.y = location.x, location.y
        gg.Actor.setLocation(self, location)
    
    def print_stats(self):
        print(str(self.thrust) +  " | " + str(self.getDirection()) \
            + " || " + str(self.y_velocity) + " | " + str(self.x_velocity) \
            + " || " + str(self.fuel))
    

if __name__ == "__main__":
    grid = gg.GameGrid(800, 800, 1, None)
    
    lander = Lander(
        grid,
        SPRITE['lander'],
        1.62,
        KEY['w'],
        KEY['s'],
        KEY['a'],
        KEY['d'],
        KEY['q'],
        KEY['e'],
        gg.Location(0,20)
    )
    
    grid.addActor(lander, lander.true_position.get_int_location(), 270)
    
    grid.setSimulationPeriod(10)
    grid.setTitle("Lander Thruster Physics Test")
    grid.show()
    grid.doRun()