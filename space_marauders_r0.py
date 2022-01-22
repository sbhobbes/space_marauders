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
    def __init__(self, width, height, color, startingHealth, currentHealth, fireRate, weaponType, shipType, startPosX, 
    StartPosY, currentPosX, currentPosY, moveRate, baseDamage = 1, lastAttackTime = None):
        super().__init__()
        self.width = width                              # the width of the enemy spaceship 
        self.height = height                            # the height of the enemy spaceship
        self.startingHealth = startingHealth            # starting health value of the enemy spaceship
        self.currentHealth = currentHealth              # current health value of the enemy spaceship
        self.fireRate = fireRate                        # the rate at which the enemy ship can attack
        self.weaponType = weaponType                    # the type of weapon equipped by enemy spaceship
        self.shipType = shipType                        # the type of spaceship
        self.currentPosX = currentPosX                  # current x coordinate position of the enemy spaceship
        self.currentPosY = currentPosY                  # current y coordinate position of the enemy spaceship
        self.moveRate = moveRate                        # the speed at which the enemy spaceship moves along the x axis
        self.baseDamage = baseDamage                    # the base damage of the enemy spaceship; could be impacted by multipliers
        self.lastAttackTime = lastAttackTime            # the time of the last attack, used to see if another attack can be made
        
        # Create the graphics for the enemy spaceship
        self.image = pygame.Surface((self.width, self.height))
        self.image = pygame.image.load(os.path.join('assets', 'moroders.png'))
        self.rect = self.image.get_rect()
        self.rect.center = (startPosX, StartPosY)

class Starship(pygame.sprite.Sprite):
    def __init__(self, width, height, color, startingHealth, currentHealth, fireRate, weaponType, shipType, startPosX, 
    startPosY, currentPosX, baseDamage, shieldType, lastAttackTime = None):
        super().__init__()
        self.startingHealth = startingHealth
        self.currentHealth = currentHealth
        self.fireRate = fireRate
        self.weaponType = weaponType
        self.shipType = shipType
        self.currentPosX = currentPosX
        self.baseDamage = baseDamage
        self.shieldType = shieldType
        self.lastAttackTime = lastAttackTime

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (startPosX, startPosY)

# Main function
def main():

    # Define variables
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    FPSCLOCK = pygame.time.Clock()
    
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    BG_COLOR = BLACK

    FPSCLOCK.tick(FPS)

    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    SCREEN.fill(BG_COLOR)

    # enemies
    enemy = Enemy(50, 50, RED, 10, 10, 5, 'phaser', 'alpha', 100, 100, 100, 100, 1)
    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy)

    # starship
    starship = Starship(50, 50, BLUE, 100, 100, 10, 'phaser', 'alpha', (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 4 * 3), 10, 10, 'ion')
    starship_group = pygame.sprite.Group()
    starship_group.add(starship)

    # Game loop
    while True:
        
        # Check user input for quit events and escape key
        CheckForQuit()

        pygame.display.flip()
        enemy_group.draw(SCREEN)
        starship_group.draw(SCREEN)
        FPSCLOCK.tick(FPS)

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