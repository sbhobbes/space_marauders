# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import os

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
        self.image = pygame.image.load(os.path.join('assets\ships', 'skyBlanc.png'))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.currentPosX, self.startPosY)

    # Override the sprit.update method to allow the player to control the position of the starship
    def update(self, direction):
        """This method takes direction as an argument and updates the x coordinate
        position of the player starship based on that input.  It also checks to ensure
        that the spaceship isn't too far to the left or the right on the screen."""

        # If the parameter direction is to the left and not out of bounds,
        # then update the position of the player starship to be a little
        # further to the left.
        if direction == self.LEFT and (self.currentPosX - (self.image.get_width() / 2)) > 10:
            self.currentPosX -= 5
            self.rect.center = (self.currentPosX, self.startPosY)

        # If the parameter direction is to the right and not out of bounds,
        # then update the position of the player starship to be a little
        # further to the right.
        elif direction == self.RIGHT and (self.currentPosX + (self.image.get_width() / 2)) < self.screenWidth - 10:
            self.currentPosX += 5
            self.rect.center = (self.currentPosX, self.startPosY)

    def GetStarshipPosition(self):
        return self.currentPosX, self.startPosY