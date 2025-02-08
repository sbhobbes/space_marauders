# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import os
from pygame.locals import *
import space_marauders


# Player starship class, inherits pygame.sprite.Sprite
class Starship(pygame.sprite.Sprite):
    def __init__(
        self,
        screen_width,
        screen_height,
        width,
        height,
        starting_health,
        current_health,
        fire_rate,
        weapon_type,
        ship_type,
        starting_x_position,
        starting_y_position,
        base_damage,
        shield_type,
        last_attack_time=None
    ):
        super().__init__()
        self.LEFT = 'left'                              # used to check the direction of the player starship
        self.RIGHT = 'right'                            # used to check the direction of the player starship
        self.screen_width = screen_width                  # the width of the display screen
        self.screen_height = screen_height                # the height of the display screen
        self.width = width                              # the width of the player starship
        self.height = height                            # the height of the player starship
        self.starting_health = starting_health            # starting health value of the player starship
        self.current_health = current_health              # current health value of the player starship
        self.fire_rate = fire_rate                        # the rate at which the player ship can attack
        self.weapon_type = weapon_type                    # the type of weapon equipped by the player starship
        self.ship_type = ship_type                        # the type of starship
        self.starting_x_position = starting_x_position                      # starting x coordinate of the player starship
        self.starting_y_position = starting_y_position                      # starting y coordinate of the player starship
        self.currentPosX = self.starting_x_position               # current x coordinate position of the player starship
        self.base_damage = base_damage                    # the base damage of the player starship; impacted by damage multipliers
        self.shield_type = shield_type                    # the type of shield equipped by the player starship
        self.last_attack_time = last_attack_time            # the time of the last attack, used to see if another attack can be made

        # Create the graphics for the player starship; define the path, resize the image, assign the image to a rect
        # object of the same size, and finally set the position of the image on the screen.
        # self.image = pygame.image.load(os.path.join('assets/ships', 'skyBlanc2.png')).convert_alpha()
        self.image = space_marauders.utils.helpers.load_asset('skyBlanc2.png', base_path='ships')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.currentPosX, self.starting_y_position)

    def Input(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            if (self.currentPosX - (self.image.get_width() / 2)) > 10:
                self.currentPosX -= 5
                self.rect.center = (self.currentPosX, self.starting_y_position)
        if keys[K_RIGHT] or keys[K_d]:
            if (self.currentPosX + (self.image.get_width() / 2)) < pygame.display.get_window_size()[0]:
                self.currentPosX += 5
                self.rect.center = (self.currentPosX, self.starting_y_position)

    # Override the sprit.update method to allow the player to control the position of the starship
    def update(self):
        self.Input()

    # Method to return the current x and y coordinates of the player starship
    def get_current_position(self):
        return self.currentPosX, self.starting_y_position