# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import space_marauders


# Enemy spaceship class, inherits pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        screen_width,
        screen_height,
        width,
        height,
        starting_health,
        current_health,
        fire_rate,
        weapon_type,
        ship_type,
        starting_x_position,
        starting_y_position,
        move_rate,
        base_damage=1,
        last_attack_time=None
    ):
        super().__init__()
        self.LEFT = 'left'                              # constant to check the direction the enemy ship is moving
        self.RIGHT = 'right'                            # constant to check the direction the enemy ship is moving
        self.screen_width = screen_width                  # width of the game screen
        self.screen_height = screen_height                # height of the game screen
        self.width = width                              # the width of the enemy spaceship 
        self.height = height                            # the height of the enemy spaceship
        self.starting_health = starting_health            # starting health value of the enemy spaceship
        self.current_health = current_health              # current health value of the enemy spaceship
        self.fire_rate = fire_rate                        # the rate at which the enemy ship can attack
        self.weapon_type = weapon_type                    # the type of weapon equipped by enemy spaceship
        self.ship_type = ship_type                        # the type of spaceship
        self.starting_x_position = starting_x_position                      # starting x coordinate of the enemy spaceship
        self.starting_y_position = starting_y_position                      # starting y coordinate of the enemy spaceship
        self.currentPosX = self.starting_x_position               # current x coordinate of the enemy spaceship
        self.currentPosY = self.starting_y_position               # current y coordinate  of the enemy spaceship
        self.move_rate = move_rate                        # the speed at which the enemy spaceship moves along the x axis
        self.base_damage = base_damage                    # the base damage of the enemy spaceship; impacted by damage multipliers
        self.last_attack_time = last_attack_time            # the time of the last attack, used to see if another attack can be made
        self.moveDirection = self.LEFT                  # indicates the direction the enemy spaceship is moving, left or right
        
        # Create the graphics for the enemy spaceship; define the path, resize the image, assign the image to a rect
        # object of the same size, and finally set the position of the image on the screen.
        # self.image = pygame.image.load(os.path.join('assets/ships', 'moroder2.png')).convert_alpha()
        self.image = space_marauders.utils.helpers.load_asset('moroder2.png', base_path='ships')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (self.currentPosX, self.currentPosY)

    # Override the sprit.update method to automate the movement of the enemy spaceship
    def update(self, direction, drop):
        """This method automates the left-to-right movement of the enemy spaceship
        In some version it will also be used to drop the spaceship down a level so
        with each back and forth motion the spaceship moves a little closer to the player"""
        
        # Assign parameter variables
        self.moveDirection = direction

        # if the direction argument is left, then update the position to the left; or if the direction
        # argument is right, then update the position to the right
        if self.moveDirection == self.LEFT:
            self.currentPosX -= self.move_rate
            self.rect.center = (self.currentPosX, self.currentPosY)
        elif self.moveDirection == self.RIGHT:
            self.currentPosX += self.move_rate
            self.rect.center = (self.currentPosX, self.currentPosY)

        if drop:
            self.currentPosY += 20
            self.rect.center = (self.currentPosX, self.currentPosY)

    # method to get the current x and y position of the enemy object
    def get_current_position(self):
        return self.currentPosX, self.currentPosY

    # method to get the fire rate of the enemy object
    def get_enemy_fire_rate(self):
        return self.fire_rate

    # Method to get the width of the enemy object
    def get_enemy_width(self):
        return self.image.get_width()