'''
This module holds the base class for all starships.  This class is not
intended to be used directly, but rather as a super class for the 
indivdual player and alien starships.

Author: Seth Hobbes
Company: Springboro Technologies, LLC DBA Monarch Technologies
Date: 1/20/2022
Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
Image assets credit to: https://github.com/exewin https://exewin.github.io/
'''

import pygame
from space_marauders.utils.helpers import load_asset, get_metadata
from space_marauders.objects.projectile import Projectile


class BaseStarship(pygame.sprite.Sprite):
    '''
    This is the base starship class.
    '''
    def __init__(self, x, y, faction, **kwargs):
        super().__init__()
        setup = get_metadata('setup.yaml')[faction]
        self.image = load_asset(setup['ship_image_path'], base_path='ships')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image = self.brighten_image(self.image, 50)
        self.image = self.add_outline(self.image, (80, 80, 80), 1)
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = setup['ship_speed']
        self.faction = faction
        self.global_projectiles = kwargs.get('projectile_group', None)
        self.projectiles = pygame.sprite.Group()


    # def update(self):
    #     self.projectiles.update()


    def fire(self):
        if len(self.projectiles) == 0:
            projectile = Projectile(
                self.rect.centerx,
                self.rect.centery,
                self.faction
            )
            self.projectiles.add(projectile)
            self.global_projectiles.add(projectile)


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.projectiles.draw(screen)


    def brighten_image(self, image, amount):
        brightened = image.copy()
        brightened.fill((amount, amount, amount), special_flags=pygame.BLEND_RGB_ADD)

        return brightened


    def add_outline(self, image, color=(255, 255, 255), thickness=2):
        """Create an outline effect around the sprite."""
        mask = pygame.mask.from_surface(image)
        outline = mask.outline()
        outlined_image = image.copy()
        
        for point in outline:
            pygame.draw.circle(outlined_image, color, point, thickness)

        return outlined_image
