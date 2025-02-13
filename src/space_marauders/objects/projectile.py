'''
This module contains the classes for the alien and player projectiles.
'''
# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import space_marauders


class Projectile(pygame.sprite.Sprite):
    '''
    This is the main projectile class.
    '''
    def __init__(
        self,
        original_x_position: int,
        original_y_position: int,
        projectile_origin: int,
        projectile_type: str,
        projectile_width: int,
        projectile_length: int,
        projectile_speed
    ):
        super().__init__()
        self.position_x = original_x_position                 # the x coordinate of the projectile
        self.position_y = original_y_position                 # the y coordinate of the projectile
        self.width = projectile_width                # the width of the projectile
        self.length = projectile_length             # the length of the projectile
        self.speed = projectile_speed
        self.type = projectile_type                  # the type of projectile to create; this controls the image file
        self.LASER = 'laser'                        # one of the types of projectiles that could be referenced
        self.BOMB = 'bomb'                          # one of the types of projectiles that could be references
        self.ENEMY = 'enemy'                        # indicates if the projectile was launched by an enemy
        self.PLAYER = 'player'                      # indicates if the projectile was launched by the player
        self.UP = 'up'                              # indicates if the projectile travel direction should be up
        self.DOWN = 'down'                          # indicates if the projectile travel direction should be down
        
        # check the projectile_origin value to see if it was launched by an enemy or the player.
        # if it was launched by an enemy then the travel direction should be down;
        # if it was launched by the player then the travel direction should be up.
        if projectile_origin == self.ENEMY:
            self.direction = self.DOWN

        elif projectile_origin == self.PLAYER:
            self.direction = self.UP

        # check the projectile type to see which graphic object to create.
        # if the type of projectile is laser, then create the object's image
        # using the laser file; if the projectile is a bomb, then create the
        # object's image using the bomb file. Also set the position according
        # to the x and y coordinates passed into the __init__ function.
        if self.type == self.LASER:
            # Create graphics for the starship laser projectile
            # self.image = pygame.image.load(os.path.join('assets/Projectiles', 'Laser03.png')).convert_alpha()
            self.image = space_marauders.utils.helpers.load_asset('laser_03.png', base_path='projectiles')
            self.image = pygame.transform.scale(self.image, (self.width, self.length))
            self.rect = self.image.get_rect()
            self.rect.center = (self.position_x, self.position_y)

        elif self.type == self.BOMB:
            # Create graphics for the bomb projectile
            # self.image = pygame.image.load(os.path.join('assets/Projectiles', 'MachineGun03.png')).convert_alpha()
            self.image = space_marauders.utils.helpers.load_asset('machine_gun_03.png', base_path='projectiles')
            self.image = pygame.transform.scale(self.image, (self.width, self.length))
            self.rect = self.image.get_rect()
            self.rect.center = (self.position_x, self.position_y)


    def update(self):
        '''
        This method overrides the sprite.update parent object method to control the movement
        of the projectile based on the travel direction, the origin point, and the speed
        value.
        '''
        if self.direction == self.UP:
            self.position_y -= self.speed
            self.rect.center = (self.position_x, self.position_y)

        elif self.direction == self.DOWN:
            self.position_y += self.speed
            self.rect.center = (self.position_x, self.position_y)


    # Method to return current x and y position of the object
    def get_current_position(self):
        '''
        Get the current x and y coordinates of the projectile.
        '''
        return self.position_x, self.position_y


class ProjectileGroup(pygame.sprite.Group):
    def __init__(self, *sprites, **kwargs):
        super().__init__(*sprites)
        self.starship_group = kwargs.get('starship_group', None)
        self.projectile_origin = kwargs.get('projectile_origin', None)
        self.setup = space_marauders.utils.helpers.get_metadata('setup.yaml')[self.projectile_origin]


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


    def fire(self):
        for ship in self.starship_group:
            ship_x_position, ship_y_position = ship.get_current_position()
            projectile = Projectile(
                original_x_position=ship_x_position,
                original_y_position=ship_y_position,
                projectile_origin=self.projectile_origin,
                projectile_type=self.setup['projectile_type'],
                projectile_width=self.setup['projectile_width'],
                projectile_length=self.setup['projectile_length'],
                projectile_speed=self.setup['projectile_speed']
            )
            self.add(projectile)
