'''
This module contains the classes for the alien starships.

Author: Seth Hobbes
Company: Springboro Technologies, LLC DBA Monarch Technologies
Date: 1/20/2022
Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
Image assets credit to: https://github.com/exewin https://exewin.github.io/
'''
import numpy as np
import pygame
from .. import base_objects


class AlienStarship(base_objects.base_starship.BaseStarship):
    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, 'alien', **kwargs)
        self.fire_timer = pygame.time.get_ticks() + np.random.randint(0, 2000)


    def update(self, **kwargs):
        super().update()
        current_time = pygame.time.get_ticks()

        if current_time - self.fire_timer > 1000:
            self.fire()
            self.fire_timer = current_time + np.random.randint(500, 2000)
