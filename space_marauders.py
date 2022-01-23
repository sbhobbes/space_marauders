# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import os
import time
from sys import exit
from pygame.locals import *
from enemy import *
from starship import *
from projectile import *

# Main game function
def main():

    # Start the pygame engine
    pygame.init()

    # Declare constants
    SCREEN_WIDTH = 1200                 # width of the screen area
    SCREEN_HEIGHT = 900                 # height of the screen area
    FPS = 60                            # maximum frames per second (FPS)
    FPSCLOCK = pygame.time.Clock()      # clock object to control the maximum FPS
    LEFT = 'left'                       # movement direction for player starship
    RIGHT = 'right'                     # movement direction for player starship
    STARSHIP_SIZE = 50                  # player starship height and width
    ENEMY_SIZE = 50                     # enemy spaceship height and width
    LASER_WIDTH = 5                     # width of the player starship laser 
    LASER_HEIGHT = 25                   # height of the player starship laser
    BOMB_SIZE = 50                      # height and width of the enemy bomb image
    PLAYER = 'player'                   # value to pass to the projectile init function
    ENEMY = 'enemy'                     # value to pass to the projectile init function

    # Declare variables
    enemySpeed = 2                      # enemy ship starting speed, impacted by multipliers
    isLaser = False                     # flag to check if a player projectile active on the screen or not
    isEnemy = False                     # flag to check if an enemy is present on the screen or not
    isBomb = False
    lastBombTime = time.time()
    
    # Create the game display area, assign it to the SCREEN constant, and apply the background image
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BG_IMAGE = pygame.image.load(os.path.join('assets', 'backgroundSpace.png'))
    BG_IMAGE.set_alpha(150)
    BG_IMAGE = pygame.transform.scale(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # create enemy spaceship object
    enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SIZE, ENEMY_SIZE, 10, 10, 5, 'phaser', 'alpha', (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 8 * 0.5), enemySpeed, True)
    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy)

    # Create bombs for enemy spaceship

    # create player starship object
    starship = Starship(SCREEN_WIDTH, SCREEN_HEIGHT, STARSHIP_SIZE, STARSHIP_SIZE, 100, 100, 10, 'phaser', 'alpha', (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 8 * 7.5), 10, 10, 'ion')
    starship_group = pygame.sprite.Group()
    starship_group.add(starship)

    # Create a group to hold projectile objects
    projectile_group = pygame.sprite.Group()

    # Game loop
    while True:
        
        # Set maximum framerate
        FPSCLOCK.tick(FPS)
        
        # Check user input for quit events and escape key
        CheckForQuit()

        # Draw background image
        SCREEN.blit(BG_IMAGE, (0, 0))

        # Create laser object if spacebar is pressed
        for event in pygame.event.get(KEYUP):
            if event.key == K_SPACE:
                if isLaser == False:
                    starshipPosX, starshipPosY = starship.GetStarshipPosition()
                    laser = Projectile(SCREEN_WIDTH, SCREEN_HEIGHT, starshipPosX, starshipPosY, PLAYER, projectileWidth = LASER_WIDTH, projectileHeight = LASER_HEIGHT)
                    projectile_group.add(laser)
                    projectile_group.draw(SCREEN)
                    isLaser = True
            else:
                pygame.event.post(event)
        if isLaser == True:
            assert laser in projectile_group, 'projectile group is empty'
            projectile_group.draw(SCREEN)
            if laser.positionY < - 100:
                isLaser = False
            elif pygame.sprite.spritecollide(laser, enemy_group, True):
                laser.kill()
                isLaser = False

        if enemy in enemy_group and isEnemy == False:
            isEnemy = True
        elif not enemy in enemy_group and isEnemy == True:
            isEnemy = False
            enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SIZE, ENEMY_SIZE, 10, 10, 5, 'phaser', 'alpha', (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 8 * 0.5), enemySpeed, True)
            enemy_group = pygame.sprite.Group()
            enemy_group.add(enemy)

        # Check if enough time has passed to drop a bomb, if so, drop bomb
        # if lastBombTime + enemy.fireRate >= time.time():
        print(lastBombTime)
        if isBomb == False:
            enemyPosX, enemyPosY = enemy.GetEnemyPosition()
            bomb = Projectile(SCREEN_WIDTH, SCREEN_HEIGHT, enemyPosX, enemyPosY, ENEMY, projectileWidth = BOMB_SIZE, projectileHeight = BOMB_SIZE)
            projectile_group.add(bomb)
            projectile_group.draw(SCREEN)
            isBomb = True
        else:
            projectile_group.draw(SCREEN)

        # Draw spaceship groups
        enemy_group.draw(SCREEN)
        starship_group.draw(SCREEN)

        # Check user input for starship movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            starship_group.update(LEFT)
        if keys[K_RIGHT] or keys[K_d]:
            starship_group.update(RIGHT)

        # Update projectile positions
        projectile_group.update()

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