# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import pygame
import os
from sys import exit
from pygame.locals import *
from enemy import *
from starship import *
from projectile import *

# Main game function
def main():

    # Start the pygame engine and font module
    pygame.init()
    pygame.font.init()

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
    BOMB_SIZE = 15                      # height and width of the enemy bomb image
    PLAYER = 'player'                   # value to pass to the projectile class call for origin point
    ENEMY = 'enemy'                     # value to pass to the projectile class call for origin point
    BOMB = 'bomb'                       # value to pass into the projectile class call for projectile type
    LASER = 'laser'                     # value to pass into the projectile class call for projectile type

    # Colors
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # Declare variables
    enemySpeed = 1                      # enemy ship starting speed, impacted by multipliers
    bombSpeed = 4                       # bomb speed starting value, impacted by multipliers
    laserSpeed = 10                     # laser speed starting value, impacted by multipliers
    starshipFireRate = 5000             # time in milliseconds between starship projectiles, impacted by multipliers
    enemyFireRate = 5000                # time in milliseconds between enemy projectiles, impacted by multipliers
    isLaser = False                     # flag to check if a player projectile active on the screen or not
    isEnemy = False                     # flag to check if an enemy is present on the screen or not
    isBomb = False                      # flag to check if a bomb is present on the screen or not
    currentLevel = 0                    # value of the current level
    levelScore = 0                      # score for the current level
    totalScore = 0                      # cumulative score the game across all levels played
    lasersFired = 0                     # the number of lasers fired
    enemiesHit = 0                      # the number of enemies hit by the player
    playerAccuracy = 0                  # the accuracy percentage of lasers fired over enemies hit
    mainMenu = True                     # condition to display the main menu or not
    moveDirection = LEFT                # holds the direction that all enemy objects should move along the x axis
    
    # Create the game display area, assign it to the SCREEN constant, and apply the background image
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BG_IMAGE = pygame.image.load(os.path.join('assets', 'backgroundSpace.png'))
    BG_IMAGE.set_alpha(150)
    BG_IMAGE = pygame.transform.scale(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    BUTTON_FONT = pygame.font.Font('freesansbold.ttf', 100)

    # Create enemies
    enemyGroup = CreateEnemies(SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SIZE, enemyFireRate, enemySpeed, 10)

    # create player starship object
    starshipGroup = CreateStarship(SCREEN_WIDTH, SCREEN_HEIGHT, STARSHIP_SIZE, STARSHIP_SIZE, starshipFireRate)

    # Create groups to hold projectile objects
    laserGroup = pygame.sprite.Group()
    bombGroup = pygame.sprite.Group()

    # Game loop
    while True:
        
        while mainMenu:
            surface = BUTTON_FONT.render('New Game', True, RED)
            surface2 = BUTTON_FONT.render('New Game', True, RED)
            buttonRect = surface.get_rect()
            buttonRect2 = surface.get_rect()
            buttonRect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            buttonRect2.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            surface2.fill(GREEN)
            SCREEN.blit(BG_IMAGE, (0, 0))
            SCREEN.blit(surface2, buttonRect2)
            SCREEN.blit(surface, buttonRect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and buttonRect.collidepoint(pygame.mouse.get_pos()):
                    mainMenu = False

        # Set maximum framerate
        FPSCLOCK.tick(FPS)
        
        # Check user input for quit events and escape key
        CheckForQuit()

        # Create laser object if spacebar is pressed
        for event in pygame.event.get(KEYUP):
            if event.key == K_SPACE:
                if isLaser == False and starshipGroup:
                    laserGroup = CreateProjectile(SCREEN_WIDTH, SCREEN_HEIGHT, starshipGroup, PLAYER, LASER, LASER_WIDTH, LASER_HEIGHT, laserSpeed)
                    lasersFired += 1
                    print('lasers fired: ' + str(lasersFired))
                    isLaser = True
            else:
                pygame.event.post(event)

        # Check user input for starship movement
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            starshipGroup.update(LEFT)
        if keys[K_RIGHT] or keys[K_d]:
            starshipGroup.update(RIGHT)

        # Check for laser existence and collision
        if isLaser == True:
            for laser in laserGroup:
                if laser.GetCurrentPosition()[1] < - 100:
                    isLaser = False
                elif pygame.sprite.groupcollide(laserGroup, enemyGroup, True, True):
                    isLaser = False
                    enemiesHit += 1

        # Check to see if new enemy should be created; will later be replaced by levels, scoring, and resets
        if enemyGroup and isEnemy == False:
            isEnemy = True
        elif not enemyGroup and isEnemy == True:
            isEnemy = False
            enemyGroup = CreateEnemies(SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SIZE, enemyFireRate, enemySpeed, 10)

        # Check if enough time has passed to drop a bomb, if so, drop bomb
        if isBomb == False:
            for enemy in enemyGroup:
                bombGroup = CreateProjectile(SCREEN_WIDTH, SCREEN_HEIGHT, enemyGroup, ENEMY, BOMB, BOMB_SIZE, BOMB_SIZE, bombSpeed)
                isBomb = True
                lastBombTime = pygame.time.get_ticks()
        elif isBomb == True and pygame.time.get_ticks() - lastBombTime >= enemy.GetEnemyFireRate():
            isBomb = False
        else:
            for bomb in bombGroup:
                if isBomb == True and bomb.GetCurrentPosition()[1] > SCREEN_HEIGHT + 100:
                    bomb.kill()
                    isBomb = False
                elif pygame.sprite.groupcollide(starshipGroup, bombGroup, True, True):
                    isBomb = False

        # calculate accuracy, score, etc.
        accuracyChanged = False
        if enemiesHit > 0:
            tempPlayerAccuracy = playerAccuracy
            playerAccuracy = round((enemiesHit / lasersFired * 100))
            if playerAccuracy != tempPlayerAccuracy:
                accuracyChanged = True
        
        if accuracyChanged:
            print('enemies hit: %s' %enemiesHit)
            print('laser count: %s' % lasersFired)
            print('accuracy: %s%%' %playerAccuracy)

        # If any enemy is nearing the edge of the screen, update the moveDirection variable;
        # this variable is then passed into the enemy group update method to move all of the
        # enemies in the correct direction
        for enemy in enemyGroup:
            xPosition = enemy.GetCurrentPosition()[0]
            width = enemy.GetEnemyWidth()
            if xPosition - (width / 2) < 10:
                moveDirection = RIGHT
                break
            elif xPosition + (width / 2) > SCREEN_WIDTH - 10:
                moveDirection = LEFT
                break

        # Draw group objects to the screen in order from lowest z-score to highest z-score;
        # if the display surface (SCREEN) has a z-score of 0, then:
        SCREEN.blit(BG_IMAGE, (0, 0))       # background image; z-score = 1
        laserGroup.draw(SCREEN)             # draw lasers; z-score = 2
        bombGroup.draw(SCREEN)              # draw bombs; z-score = 3
        enemyGroup.draw(SCREEN)             # draw enemies; z-score = 4
        starshipGroup.draw(SCREEN)          # draw starship; z-score = 5

        # Update all object positions
        laserGroup.update()                 # update the y coordinate of the laser; x coordinate is static
        bombGroup.update()                  # update the y coordinate of the bombs; x coordinate is static        
        if moveDirection == LEFT:           
            enemyGroup.update(LEFT)         # update the x and y coordinates of the enemies
        elif moveDirection == RIGHT:
            enemyGroup.update(RIGHT)        # update the x and y coordinates of the enemies
        pygame.display.update()             # apply all of the updates to the display surface

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

# Function for the main menu screen, which should be displayed when the user first starts
# or when the escape key is pressed; however, the escape key would pull up the main menu
# in a pause game state.
def MainMenu():
    pass

# Level start animation
def GameStartAnimation():
    pass

# Display game over animation upon player death
def GameOverAnimation():
    pass

# Create player starship function
def CreateStarship(screenWidth, screenHeight, starshipHeight, starshipWidth, starshipFireRate):

    # Create the starship group object
    group = pygame.sprite.Group()

    # Create the starship object
    starship = Starship(screenWidth, screenHeight, starshipWidth, starshipHeight, 100, 100, starshipFireRate, 'phaser', 'alpha', (screenWidth / 2), (screenHeight / 8 * 7.5), 10, 10, 'ion')
    group.add(starship)

    # Return the starship group object to the calling function
    return group

# Create enemies function
def CreateEnemies(screenWidth, screenHeight, size, fireRate, speed, enemyCount):
    
    # Create the enemies group object
    group = pygame.sprite.Group()

    # create enemy spaceship objects and add to a group
    for enemy in range(enemyCount):
        newEnemy = Enemy(screenWidth, screenHeight, size, size, 10, 10, fireRate, 'phaser', 'alpha', ((screenWidth / (enemyCount + 1)) * (enemy + 1)), (screenHeight / 8 * 0.5), speed, True)
        group.add(newEnemy)
    
    # Return the group of enemy objects to the calling function
    return group

# Create laser function
def CreateProjectile(screenWidth, screenHeight, shipGroup, originType, projectileType, projectileWidth, projectileHeight, projectileSpeed):
    
    # Create the projectile group object
    group = pygame.sprite.Group()
    
    # Create the projectile objects and add to a group
    for ship in shipGroup:
        shipX, shipY = ship.GetCurrentPosition()
        projectile = Projectile(screenWidth, screenHeight, shipX, shipY, originType, projectileType, projectileWidth, projectileHeight, projectileSpeed)
        group.add(projectile)

    # Return the group of projectile objects to the calling function
    return group

# Call main function
if __name__ == '__main__':
    main()