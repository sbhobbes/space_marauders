# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import os

class Projectile(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, originPosX, originPosY, projectileOrigin, projectileType, projectileWidth, projectileHeight, projectileSpeed):
        super().__init__()
        self.screenWidth = screenWidth              # the width of the display screen
        self.screenHeight = screenHeight            # the height of the display screen
        self.positionX = originPosX                 # the x coordinate of the projectile
        self.positionY = originPosY                 # the y coordinate of the projectile
        self.width = projectileWidth                # the width of the projectile
        self.height = projectileHeight              # the height of the projectile
        self.type = projectileType                  # the type of projectile to create; this controls the image file
        self.LASER = 'laser'                        # one of the types of projectiles that could be referenced
        self.BOMB = 'bomb'                          # one of the types of projectiles that could be references
        self.ENEMY = 'enemy'                        # indicates if the projectile was launched by an enemy
        self.PLAYER = 'player'                      # indicates if the projectile was launched by the player
        self.UP = 'up'                              # indicates if the projectile travel direction should be up
        self.DOWN = 'down'                          # indicates if the projectile travel direction should be down
        self.speed = projectileSpeed
        
        # check the projectileOrigin value to see if it was launched by an enemy or the player.
        # if it was launched by an enemy then the travel direction should be down;
        # if it was launched by the player then the travel direction should be up.
        if projectileOrigin == self.ENEMY:
            self.direction = self.DOWN
        elif projectileOrigin == self.PLAYER:
            self.direction = self.UP

        # check the projectile type to see which graphic object to create.
        # if the type of projectile is laser, then create the object's image
        # using the laser file; if the projectile is a bomb, then create the
        # object's image using the bomb file. Also set the position according
        # to the x and y coordinates passed into the __init__ function.
        if self.type == self.LASER:
            # Create graphics for the starship laser projectile
            self.image = pygame.image.load(os.path.join('assets\Projectiles', 'Laser03.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.positionX, self.positionY)
        elif self.type == self.BOMB:
            # Create graphics for the bomb projectile
            self.image = pygame.image.load(os.path.join('assets\Projectiles', 'MachineGun03.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.positionX, self.positionY)

    # override the sprite.update method to control the movement of the projectile based
    # on the travel direction, the origin point, and the speed value passed into the
    # __init__ function.
    def update(self):
        if self.direction == self.UP:
            self.positionY -= self.speed
            self.rect.center = (self.positionX, self.positionY)
        elif self.direction == self.DOWN:
            self.positionY += self.speed
            self.rect.center = (self.positionX, self.positionY)

    # Method to return current x and y position of the object
    def GetCurrentPosition(self):
        return self.positionX, self.positionY