'''
This module contains the classes for the alien starships.
'''
# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/
import numpy as np
import pygame
import space_marauders


# Enemy spaceship class, inherits pygame.sprite.Sprite
class Alien(pygame.sprite.Sprite):
    '''
    This is the main alien starship class.
    '''
    def __init__(
        self,
        width: int,
        height: int,
        fire_rate: int,
        starting_x_position: int,
        starting_y_position: int,
        move_rate: int #
    ):
        super().__init__()
        self.LEFT = 'left'                              # constant to check the direction the enemy ship is moving
        self.RIGHT = 'right'                            # constant to check the direction the enemy ship is moving
        self.width = width                              # the width of the enemy spaceship 
        self.height = height                            # the height of the enemy spaceship
        self.fire_rate = fire_rate                        # the rate at which the enemy ship can attack
        self.starting_x_position = starting_x_position                      # starting x coordinate of the enemy spaceship
        self.starting_y_position = starting_y_position                      # starting y coordinate of the enemy spaceship
        self.current_x_position = self.starting_x_position               # current x coordinate of the enemy spaceship
        self.current_y_position = self.starting_y_position               # current y coordinate  of the enemy spaceship
        self.move_rate = move_rate                        # the speed at which the enemy spaceship moves along the x axis
        self.move_direction = self.LEFT                  # indicates the direction the enemy spaceship is moving, left or right

        # Create the graphics for the enemy spaceship; define the path, resize the image, assign the image to a rect
        # object of the same size, and finally set the position of the image on the screen.
        self.image = space_marauders.utils.helpers.load_asset('moroder_2.png', base_path='ships')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (self.current_x_position, self.current_y_position)


    # Override the sprit.update method to automate the movement of the enemy spaceship
    def update(self, direction, drop):
        '''
        This method automates the left-to-right movement of the enemy spaceship
        In some version it will also be used to drop the spaceship down a level so
        with each back and forth motion the spaceship moves a little closer to the player
        '''
        # Assign parameter variables
        self.move_direction = direction

        # if the direction argument is left, then update the position to the left; or if the direction
        # argument is right, then update the position to the right
        if self.move_direction == self.LEFT:
            self.current_x_position -= self.move_rate
            self.rect.center = (self.current_x_position, self.current_y_position)

        elif self.move_direction == self.RIGHT:
            self.current_x_position += self.move_rate
            self.rect.center = (self.current_x_position, self.current_y_position)

        if drop:
            self.current_y_position += 20
            self.rect.center = (self.current_x_position, self.current_y_position)


    # method to get the current x and y position of the enemy object
    def get_current_position(self):
        '''
        Get the current x and y coordinates of the alien starship.
        '''
        return self.current_x_position, self.current_y_position


    # method to get the fire rate of the enemy object
    def get_enemy_fire_rate(self):
        '''
        Get the fire rate of the alien starship.
        '''
        return self.fire_rate


    # Method to get the width of the enemy object
    def get_enemy_width(self):
        '''
        Get the width of the alien starship.
        '''
        return self.image.get_width()


class AlienStarshipGroup(pygame.sprite.Group):
    def __init__(self, *sprites, **kwargs):
        self.alien_count = kwargs.get('alient_count', 10)
        self.setup = space_marauders.utils.helpers.get_metadata('setup.yaml')
        self.direction_to_set = 'left'

        super().__init__(*sprites)


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
        for alien in range(self.alien_count):
            new_starship = Alien(
                width=self.setup['alien_ship_size'],
                height=self.setup['alien_ship_size'],
                fire_rate=self.setup['alien_fire_rate'],
                starting_x_position=((self.setup['screen_width'] / (self.alien_count + 1)) * (alien + 1)),
                starting_y_position=(self.setup['screen_height'] / 8 * 0.5),
                move_rate=self.setup['alien_speed']
            )
            self.add(new_starship)


    def check_boundary_collision(self):
        '''
        Checks if any alien in the group has hit the screen boundaries.
        Returns:
            tuple: (direction_change, drop_row_needed)
                direction_change: "LEFT", "RIGHT", or None if no change needed.
                drop_row_needed: True if the group should drop down a row, False otherwise.
        '''
        min_left_edge = np.inf
        max_right_edge = -np.inf
        drop_row_needed = False

        for alien in self.sprites():
            x_position = alien.get_current_position()[0]
            width = alien.get_enemy_width()
            alien_left_edge = x_position - (width / 2)
            alien_right_edge = x_position + (width / 2)

            min_left_edge = min(min_left_edge, alien_left_edge)
            max_right_edge = max(max_right_edge, alien_right_edge)

        if min_left_edge < 10:
            print('Left side collision')
            self.direction_to_set = 'right'
            drop_row_needed = True

        if max_right_edge > self.setup['screen_width'] - 10:
            print('Right side collision')
            self.direction_to_set = 'left'
            drop_row_needed = True

        return self.direction_to_set, drop_row_needed
