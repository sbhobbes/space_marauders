# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import os

class Projectile(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, originPosX, originPosY, projectileOrigin, projectileType = 'laser', projectileWidth = 50, projectileHeight = 100):
        super().__init__()
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.positionX = originPosX
        self.positionY = originPosY
        self.width = projectileWidth
        self.height = projectileHeight
        self.type = projectileType
        self.LASER = 'laser'
        self.BOMB = 'bomb'
        self.ENEMY = 'enemy'
        self.PLAYER = 'player'
        self.UP = 'up'
        self.DOWN = 'down'
        
        if projectileOrigin == self.ENEMY:
            self.direction = self.DOWN
        elif projectileOrigin == self.PLAYER:
            self.direction = self.UP

        if self.type == self.LASER:
            # Create graphics for the starship laser projectile
            self.image = pygame.image.load(os.path.join('assets\Projectiles', 'Laser03.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.positionX, self.positionY)
        elif self.type == self.BOMB:
            # Create graphics for the bomb projectile
            self.image = pygame.image.load(os.path.join('assets\Projectiles', 'MachineGun01.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
            self.rect.center = (self.positionX, self.positionY)

    def update(self):
        if self.direction == self.UP:
            self.positionY -= 10
            self.rect.center = (self.positionX, self.positionY)
        elif self.direction == self.DOWN:
            self.positionY += 8
            self.rect.center = (self.positionX, self.positionY)
        