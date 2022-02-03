# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import os
from pygame.locals import *

# Player starship class, inherits pygame.sprite.Sprite
class Starship(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, width, height, startingHealth, currentHealth, fireRate, weaponType, shipType, startPosX, 
    startPosY, baseDamage, shieldType, lastAttackTime = None):
        super().__init__()
        self.LEFT = 'left'                              # used to check the direction of the player starship
        self.RIGHT = 'right'                            # used to check the direction of the player starship
        self.screenWidth = screenWidth                  # the width of the display screen
        self.screenHeight = screenHeight                # the height of the display screen
        self.width = width                              # the width of the player starship
        self.height = height                            # the height of the player starship
        self.startingHealth = startingHealth            # starting health value of the player starship
        self.currentHealth = currentHealth              # current health value of the player starship
        self.fireRate = fireRate                        # the rate at which the player ship can attack
        self.weaponType = weaponType                    # the type of weapon equipped by the player starship
        self.shipType = shipType                        # the type of starship
        self.startPosX = startPosX                      # starting x coordinate of the player starship
        self.startPosY = startPosY                      # starting y coordinate of the player starship
        self.currentPosX = self.startPosX               # current x coordinate position of the player starship
        self.baseDamage = baseDamage                    # the base damage of the player starship; impacted by damage multipliers
        self.shieldType = shieldType                    # the type of shield equipped by the player starship
        self.lastAttackTime = lastAttackTime            # the time of the last attack, used to see if another attack can be made

        # Create the graphics for the player starship; define the path, resize the image, assign the image to a rect
        # object of the same size, and finally set the position of the image on the screen.
        self.image = pygame.image.load(os.path.join('assets\ships', 'skyBlanc2.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.currentPosX, self.startPosY)

    def Input(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            if (self.currentPosX - (self.image.get_width() / 2)) > 10:
                self.currentPosX -= 5
                self.rect.center = (self.currentPosX, self.startPosY)
        if keys[K_RIGHT] or keys[K_d]:
            if (self.currentPosX + (self.image.get_width() / 2)) < pygame.display.get_window_size()[0]:
                self.currentPosX += 5
                self.rect.center = (self.currentPosX, self.startPosY)

    # Override the sprit.update method to allow the player to control the position of the starship
    def update(self):
        self.Input()

    # Method to return the current x and y coordinates of the player starship
    def GetCurrentPosition(self):
        return self.currentPosX, self.startPosY