'''
This module contains the classes for the player starships.
'''
# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import space_marauders


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
        self.LEFT = 'left'                              # used to check the direction of the player starship
        self.RIGHT = 'right'                            # used to check the direction of the player starship
        self.width = width                              # the width of the player starship
        self.height = height                            # the height of the player starship
        self.fire_rate = fire_rate                        # the rate at which the player ship can attack
        self.speed = move_rate
        self.starting_x_position = starting_x_position                      # starting x coordinate of the player starship
        self.starting_y_position = starting_y_position                      # starting y coordinate of the player starship
        self.current_x_position = self.starting_x_position               # current x coordinate position of the player starship

        # Create the graphics for the player starship; define the path, resize the image, assign the image to a rect
        # object of the same size, and finally set the position of the image on the screen.
        self.image = space_marauders.utils.helpers.load_asset('sky_blanc_2.png', base_path='ships')
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


    def get_current_position(self):
        '''
        Method to return the current x and y coordinates of the player starship.
        '''
        return self.current_x_position, self.starting_y_position
