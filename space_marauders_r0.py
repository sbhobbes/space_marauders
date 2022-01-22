# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import os
from sys import exit
from pygame.locals import *

# Enemy spaceship class, inherits pygame.sprite.Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screenWidth, screenHeight, width, height, startingHealth, currentHealth, fireRate, weaponType, shipType, startPosX, 
    startPosY, moveRate, baseDamage = 1, lastAttackTime = None):
        super().__init__()
        self.LEFT = 'left'                              # constant to check the direction the enemy ship is moving
        self.RIGHT = 'right'                            # constant to check the direction the enemy ship is moving
        self.screenWidth = screenWidth                  # width of the game screen
        self.screenHeight = screenHeight                # height of the game screen
        self.width = width                              # the width of the enemy spaceship 
        self.height = height                            # the height of the enemy spaceship
        self.startingHealth = startingHealth            # starting health value of the enemy spaceship
        self.currentHealth = currentHealth              # current health value of the enemy spaceship
        self.fireRate = fireRate                        # the rate at which the enemy ship can attack
        self.weaponType = weaponType                    # the type of weapon equipped by enemy spaceship
        self.shipType = shipType                        # the type of spaceship
        self.startPosX = startPosX                      # starting x coordinate of the enemy spaceship
        self.startPosY = startPosY                      # starting y coordinate of the enemy spaceship
        self.currentPosX = self.startPosX               # current x coordinate of the enemy spaceship
        self.currentPosY = self.startPosY               # current y coordinate  of the enemy spaceship
        self.moveRate = moveRate                        # the speed at which the enemy spaceship moves along the x axis
        self.baseDamage = baseDamage                    # the base damage of the enemy spaceship; impacted by damage multipliers
        self.lastAttackTime = lastAttackTime            # the time of the last attack, used to see if another attack can be made
        self.moveDirection = self.LEFT                  # indicates the direction the enemy spaceship is moving, left or right
        
        # Create the graphics for the enemy spaceship
        self.image = pygame.image.load(os.path.join('assets\ships', 'moroder.png'))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.currentPosX, self.currentPosY)

    # Override the sprit.update method to control automate the movement of the enemy spaceship
    def update(self):
        if self.moveDirection == self.LEFT and self.currentPosX - self.image.get_width() / 2 > 10:
            self.currentPosX -= self.moveRate
            self.rect.center = (self.currentPosX, self.currentPosY)
        elif self.moveDirection == self.LEFT and self.currentPosX - self.image.get_width() / 2 <= 10:
            self.moveDirection = self.RIGHT
        elif self.moveDirection == self.RIGHT and self.currentPosX + self.image.get_width() / 2 < self.screenWidth - 10:
            self.currentPosX += self.moveRate
            self.rect.center = (self.currentPosX, self.currentPosY)
        elif self.moveDirection == self.RIGHT and self.currentPosX + self.image.get_width() / 2 >= self.screenWidth - 10:
            self.moveDirection = self.LEFT


# Player starship class, inherits pygame.sprite.Sprite
class Starship(pygame.sprite.Sprite):
    def __init__(self, width, height, startingHealth, currentHealth, fireRate, weaponType, shipType, startPosX, 
    startPosY, currentPosX, baseDamage, shieldType, lastAttackTime = None):
        super().__init__()
        self.LEFT = 'left'
        self.RIGHT = 'right'
        self.width = width                              # the width of the player starship
        self.height = height                            # the height of the player starship
        self.startingHealth = startingHealth            # starting health value of the player starship
        self.currentHealth = currentHealth              # current health value of the player starship
        self.fireRate = fireRate                        # the rate at which the player ship can attack
        self.weaponType = weaponType                    # the type of weapon equipped by the player starship
        self.shipType = shipType                        # the type of starship
        self.startPosX = currentPosX                    # starting x coordinate of the player starship
        self.startPosY = startPosY                      # starting y coordinate of the player starship
        self.currentPosX = self.startPosX               # current x coordinate position of the player starship
        self.baseDamage = baseDamage                    # the base damage of the player starship; impacted by damage multipliers
        self.shieldType = shieldType                    # the type of shield equipped by the player starship
        self.lastAttackTime = lastAttackTime            # the time of the last attack, used to see if another attack can be made

        # Create the graphics for the player starship
        self.image = pygame.image.load(os.path.join('assets\ships', 'skyBlanc.png'))
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (self.currentPosX, self.startPosY)

    def update(self, direction):
        if direction == self.LEFT:
            self.currentPosX -= 5
            self.rect.center = (self.currentPosX, self.startPosY)
        elif direction == self.RIGHT:
            self.currentPosX += 5
            self.rect.center = (self.currentPosX, self.startPosY)

# Main game function
def main():

    # Start the pygame engine
    pygame.init()

    # Declare constants
    SCREEN_WIDTH = 1200                 # width of the screen area
    SCREEN_HEIGHT = 900                 # height of the screen area
    FPS = 60                            # maximum frames per second (FPS)
    FPSCLOCK = pygame.time.Clock()      # clock object to control the maximum FPS
    LEFT = 'left'
    RIGHT = 'right'

    # Declare variables
    enemySpeed = 2                      # enemy ship starting speed, impacted by multipliers
    
    # Create the game display area, assign it to the SCREEN constant, and apply the background image
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BG_IMAGE = pygame.image.load(os.path.join('assets', 'backgroundSpace.png'))
    BG_IMAGE.set_alpha(150)
    BG_IMAGE = pygame.transform.scale(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # create enemy spaceship object
    enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, 100, 100, 10, 10, 5, 'phaser', 'alpha', (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 8 * 0.5), enemySpeed, True)
    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy)

    # create player starship object
    starship = Starship(100, 100, 100, 100, 10, 'phaser', 'alpha', (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 8 * 7.5), 10, 10, 'ion')
    starship_group = pygame.sprite.Group()
    starship_group.add(starship)

    # Game loop
    while True:
        
        # Set maximum framerate
        FPSCLOCK.tick(FPS)
        
        # Check user input for quit events and escape key
        CheckForQuit()

        # Draw background image
        SCREEN.blit(BG_IMAGE, (0, 0))

        # Draw spaceship groups
        enemy_group.draw(SCREEN)
        starship_group.draw(SCREEN)

        # Check user input for starship movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            starship_group.update(LEFT)
        if keys[K_RIGHT] or keys[K_d]:
            starship_group.update(RIGHT)

        # Update enemy position every frame
        enemy_group.update()

        # Update game display
        pygame.display.update()

# Check for quit event
def CheckForQuit():
    """check user inputs to see if the game should continue or terminate"""
    
    # Loop through all events of type QUIT
    for event in pygame.event.get(QUIT):

        # If QUIT event found, call terminate function
        Terminate()

    # Loop through keyup events to check for Esc key input
    for event in pygame.event.get(KEYUP):

        # if key up is the Esc key then call terminate function to exit game
        if event.key == K_ESCAPE:
            Terminate()

        # if key up is not the Esc key then put it back into the event queue
        else:
            pygame.event.post(event)

# Quit function
def Terminate():
    """This function quits the game and terminates code execution"""
    pygame.quit()
    exit()

# Call main function
if __name__ == '__main__':
    main()