'''
This module contains the classes for the alien and player projectiles.

Author: Seth Hobbes
Company: Springboro Technologies, LLC DBA Monarch Technologies
Date: 1/20/2022
Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
Image assets credit to: https://github.com/exewin https://exewin.github.io/
'''
import pygame
from space_marauders.utils.helpers import get_metadata, load_asset


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, faction):
        super().__init__()
        setup = get_metadata('setup.yaml')
        self.screen_height = setup['screen_height']
        self.image = load_asset(setup[faction]['projectile_image_path'], base_path='projectiles')
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = setup[faction]['projectile_speed']
        self.faction = faction


    def update(self):
        if self.faction == 'player':
            self.rect.y -= self.speed

        else:
            self.rect.y += self.speed

        if self.rect.y < 0 or self.rect.y > self.screen_height:
            self.kill()
