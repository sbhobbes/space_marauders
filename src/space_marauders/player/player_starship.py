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
        self.current_score = 0
        self.shots_fired = 0
        self.aliens_hit = 0
        self.bombs_hit = 0
        self.shooting = False
        self.level_score = 0


    def get_current_score(self):
        return self.current_score


    def get_level_score(self):
        return self.level_score


    def reset_level_score(self):
        self.level_score = 0


    def update_score(self, amount_to_add):
        self.current_score += amount_to_add
        self.level_score += amount_to_add


    def update_aliens_hit(self):
        self.aliens_hit += 1


    def update_bombs_hit(self):
        self.bombs_hit += 1


    def get_accuracy(self):
        return round(((self.aliens_hit + self.bombs_hit) / self.shots_fired) * 100) if self.shots_fired > 0 else 0


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.shooting:
                self.shooting = True
                self.fire()
                self.shots_fired += 1

        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.shooting = False


    def update(self, delta_time):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed * delta_time

        if keys[pygame.K_RIGHT] and self.rect.right < self.setup['screen_width']:
            self.rect.x += self.speed * delta_time
