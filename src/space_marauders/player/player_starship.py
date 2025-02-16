'''
This module contains the classes for the player starships.

Author: Seth Hobbes
Company: Springboro Technologies, LLC DBA Monarch Technologies
Date: 1/20/2022
Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
Image assets credit to: https://github.com/exewin https://exewin.github.io/
'''
import pygame
from ..base_objects.base_starship import BaseStarship


class PlayerStarship(BaseStarship):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, 'player', **kwargs)


    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE]:
            self.fire()
