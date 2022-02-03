# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import os

# Enemy spaceship class, inherits pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, width, height, startingHealth, currentHealth, fireRate, weaponType, shipType, startPosX, 
    startPosY, moveRate, baseDamage = 1, lastAttackTime = None):
        super().__init__()
        self.LEFT = 'left'                              # constant to check the direction the enemy ship is moving
        self.RIGHT = 'right'                            # constant to check the direction the enemy ship is moving
        self.screenWidth = screenWidth                  # width of the game screen
        self.screenHeight = screenHeight                # height of the game screen
        self.width = width                              # the width of the enemy spaceship 
        self.height = height                            # the height of the enemy spaceship
        self.startingHealth = startingHealth            # starting health value of the enemy spaceship
        self.currentHealth = currentHealth              # current health value of the enemy spaceship
        self.fireRate = fireRate                        # the rate at which the enemy ship can attack
        self.weaponType = weaponType                    # the type of weapon equipped by enemy spaceship
        self.shipType = shipType                        # the type of spaceship
        self.startPosX = startPosX                      # starting x coordinate of the enemy spaceship
        self.startPosY = startPosY                      # starting y coordinate of the enemy spaceship
        self.currentPosX = self.startPosX               # current x coordinate of the enemy spaceship
        self.currentPosY = self.startPosY               # current y coordinate  of the enemy spaceship
        self.moveRate = moveRate                        # the speed at which the enemy spaceship moves along the x axis
        self.baseDamage = baseDamage                    # the base damage of the enemy spaceship; impacted by damage multipliers
        self.lastAttackTime = lastAttackTime            # the time of the last attack, used to see if another attack can be made
        self.moveDirection = self.LEFT                  # indicates the direction the enemy spaceship is moving, left or right
        
        # Create the graphics for the enemy spaceship; define the path, resize the image, assign the image to a rect
        # object of the same size, and finally set the position of the image on the screen.
        self.image = pygame.image.load(os.path.join('assets\ships', 'moroder2.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (self.currentPosX, self.currentPosY)

    # Override the sprit.update method to automate the movement of the enemy spaceship
    def update(self, direction, drop):
        """This method automates the left-to-right movement of the enemy spaceship
        In some version it will also be used to drop the spaceship down a level so
        with each back and forth motion the spaceship moves a little closer to the player"""
        
        # Assign parameter variables
        self.moveDirection = direction

        # if the direction argument is left, then update the position to the left; or if the direction
        # argument is right, then update the position to the right
        if self.moveDirection == self.LEFT:
            self.currentPosX -= self.moveRate
            self.rect.center = (self.currentPosX, self.currentPosY)
        elif self.moveDirection == self.RIGHT:
            self.currentPosX += self.moveRate
            self.rect.center = (self.currentPosX, self.currentPosY)

        if drop:
            self.currentPosY += 20
            self.rect.center = (self.currentPosX, self.currentPosY)

    # method to get the current x and y position of the enemy object
    def GetCurrentPosition(self):
        return self.currentPosX, self.currentPosY

    # method to get the fire rate of the enemy object
    def GetEnemyFireRate(self):
        return self.fireRate

    # Method to get the width of the enemy object
    def GetEnemyWidth(self):
        return self.image.get_width()