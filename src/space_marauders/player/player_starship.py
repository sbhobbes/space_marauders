'''
This module contains the classes for the player starships.
'''
# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
from ..utils.helpers import load_asset, get_metadata
from ..base_objects.base_starship import BaseStarship
from ..objects.projectile import Projectile


# Player starship class, inherits pygame.sprite.Sprite
class Starship(pygame.sprite.Sprite):
    '''
    This is the main player starship class.
    '''
    def __init__(
        self,
        width: int,
        height: int,
        fire_rate: int,
        starting_x_position: int,
        starting_y_position: int,
        move_rate: int
    ):
        super().__init__()
        self.setup = get_metadata('setup.yaml')['player']
        self.LEFT = 'left'                              # used to check the direction of the player starship
        self.RIGHT = 'right'                            # used to check the direction of the player starship
        self.width = width                              # the width of the player starship
        self.height = height                            # the height of the player starship
        self.fire_rate = fire_rate                        # the rate at which the player ship can attack
        self.speed = move_rate
        self.starting_x_position = starting_x_position                      # starting x coordinate of the player starship
        self.starting_y_position = starting_y_position                      # starting y coordinate of the player starship
        self.current_x_position = self.starting_x_position               # current x coordinate position of the player starship
        self.projectiles = pygame.sprite.Group()

        # Create the graphics for the player starship; define the path, resize the image, assign the image to a rect
        # object of the same size, and finally set the position of the image on the screen.
        self.image = load_asset('sky_blanc_2.png', base_path='ships')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.current_x_position, self.starting_y_position)


    def input(self):
        '''
        Checks for user input and updates object coordinates according to which keys are pressed.
        '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if (self.current_x_position - (self.image.get_width() / 2)) > 10:
                self.current_x_position -= 5
                self.rect.center = (self.current_x_position, self.starting_y_position)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if (self.current_x_position + (self.image.get_width() / 2)) < pygame.display.get_window_size()[0]:
                self.current_x_position += 5
                self.rect.center = (self.current_x_position, self.starting_y_position)


    def update(self):
        '''
        Overrides the sprit.update parent class method to allow the player to control the 
        position of the starship using either the arrow keys or asdw.
        '''
        self.input()
        self.projectiles.update()


    def get_current_position(self):
        '''
        Method to return the current x and y coordinates of the player starship.
        '''
        return self.current_x_position, self.starting_y_position


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.projectiles.draw(screen)


    def fire_laser(self):
        projectile = Projectile(
            original_x_position=self.rect.centerx,
            original_y_position=self.rect.centery,
            projectile_origin='player',
            projectile_type=self.setup['projectile_type'],
            projectile_width=self.setup['projectile_width'],
            projectile_length=self.setup['projectile_length'],
            projectile_speed=self.setup['projectile_speed']
        )
        self.projectiles.add(projectile)
    # def fire_laser(self):
    #     ship_x_position, ship_y_position = ship.get_current_position()
    #     projectile = Projectile(
    #         original_x_position=ship_x_position,
    #         original_y_position=ship_y_position,
    #         projectile_origin=self.projectile_origin,
    #         projectile_type=self.setup['projectile_type'],
    #         projectile_width=self.setup['projectile_width'],
    #         projectile_length=self.setup['projectile_length'],
    #         projectile_speed=self.setup['projectile_speed']
    #     )
    #     self.add(projectile)


class PlayerStarshipGroup(pygame.sprite.Group):
    def __init__(self, *sprites, **kwargs):
        setup = get_metadata('setup.yaml')

        super().__init__(*sprites)
        self.starship = Starship(
            width=setup['player_ship_size'],
            height=setup['player_ship_size'],
            fire_rate=setup['player_fire_rate'],
            starting_x_position=(setup['screen_width'] / 2),
            starting_y_position=(setup['screen_height'] / 8 * 7.5),
            move_rate=10
        )


    def update(self, *args, **kwargs):
        '''
        Overrides the update method to include custom logic.
        Calls super().update() within this function to keep default behavior.
        '''
        for sprite in self.sprites():
            if hasattr(sprite, 'my_sprite_attribute'):
                one = 1

        super().update(*args, **kwargs)


    def add(self, *sprites):
        '''
        Overrides the add method to include custom logic.
        Calls super().add() within this function to keep default behavior.
        '''
        super().add(*sprites)


    def draw(self, surface):
        '''
        Overrides the draw method to include custom logic.
        Calls super().draw() within this function to keep default behavior.
        '''
        super().draw(surface)


    def deploy(self):
        self.add(self.starship)


class PlayerStarship(BaseStarship):
    def __init__(self, x, y, image_path, speed, faction):
        super().__init__(x, y, image_path, speed, faction)


    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE]:
            self.fire('laser_03.png', 10)
