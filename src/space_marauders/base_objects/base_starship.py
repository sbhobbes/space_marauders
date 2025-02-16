'''
This module holds the base class for all starships.  This class is not
intended to be used directly, but rather as a super class for the 
indivdual player and alien starships.
'''

import pygame
from space_marauders.utils.helpers import load_asset
from space_marauders.objects.projectile import ProjectileNew


class BaseStarship(pygame.sprite.Sprite):
    '''
    This is the base starship class.
    '''
    def __init__(self, x, y, image_path, speed, faction):
        super().__init__()
        self.image = load_asset(image_path, base_path='ships')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.faction = faction
        self.projectiles = pygame.sprite.Group()


    def update(self):
        self.projectiles.update()


    def fire(self, projectile_image_path, projectile_speed):
        if len(self.projectiles) == 0:
            projectile = ProjectileNew(
                self.rect.centerx,
                self.rect.top,
                projectile_image_path,
                projectile_speed,
                self.faction
            )
            self.projectiles.add(projectile)


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.projectiles.draw(screen)
