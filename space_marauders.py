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
    ORANGE = (255, 165, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

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
    moveDirection = LEFT                # holds the direction that all enemy objects should move along the x axis
    gameActive = False                  # flag for the active game state
    gameOver = False                    # flag for end of game state
    gameOverTime = 0                    # the time that the game ended; used to hold the score screen for a preset amount of time
    calculateScore = False
    
    # Create the game display area, assign it to the SCREEN constant, and apply the background image
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BG_IMAGE = pygame.image.load(os.path.join('assets', 'backgroundSpace.png'))
    BG_IMAGE.set_alpha(150)
    BG_IMAGE = pygame.transform.scale(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    BUTTON_FONT = pygame.font.Font('freesansbold.ttf', 50)
    TITLE_FONT = pygame.font.Font('freesansbold.ttf', 100)
    SCORE_FONT = pygame.font.Font('freesansbold.ttf', 20)

    # Create groups to hold projectile objects
    starshipGroup = pygame.sprite.Group()
    enemyGroup = pygame.sprite.Group()
    laserGroup = pygame.sprite.Group()
    bombGroup = pygame.sprite.Group()

    # Game loop
    while True:

        dropOneRow = False

        # Set maximum framerate
        FPSCLOCK.tick(FPS)

        # Check user input for quit events and escape key
        CheckForQuit()

        # Create laser object if spacebar is pressed
        for event in pygame.event.get():
            if event.type == KEYUP and event.key == K_SPACE and gameActive:
                if isLaser == False and starshipGroup:
                    laserGroup = CreateProjectile(SCREEN_WIDTH, SCREEN_HEIGHT, starshipGroup, PLAYER, LASER, LASER_WIDTH, LASER_HEIGHT, laserSpeed)
                    lasersFired += 1
                    isLaser = True
            elif event.type == KEYUP and event.key == K_SPACE:
                pass
            elif event.type == MOUSEBUTTONDOWN and newGameButton.collidepoint(pygame.mouse.get_pos()):
                gameActive = True
            elif event.type == MOUSEBUTTONDOWN and not newGameButton.collidepoint(pygame.mouse.get_pos()):
                pass
            else:
                pygame.event.post(event)
        
        # check game state for active game and update display accordingly
        if gameActive:

            if len(enemyGroup) == 0:
                # Create enemies
                enemyGroup = CreateEnemies(SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SIZE, enemyFireRate, enemySpeed, 10)

            if len(starshipGroup) == 0:
                # create player starship object
                starshipGroup = CreateStarship(SCREEN_WIDTH, SCREEN_HEIGHT, STARSHIP_SIZE, STARSHIP_SIZE, starshipFireRate)
            
            starshipGroup.update()

            # Check for laser existence and collision
            if isLaser == True:
                for laser in laserGroup:
                    if laser.GetCurrentPosition()[1] < - 100:
                        isLaser = False
                    elif pygame.sprite.groupcollide(laserGroup, enemyGroup, True, True):
                        isLaser = False
                        enemiesHit += 1
                        levelScore += 25
                        if len(enemyGroup) == 0:
                            # gameActive = False
                            gameOverTime = pygame.time.get_ticks()
                            calculateScore = True
                            gameOver = True
                            ClearAllGroups((bombGroup, laserGroup, starshipGroup, enemyGroup))
                            levelScore += 1000

            # Check to see if new enemy should be created; will later be replaced by levels, scoring, and resets
            if enemyGroup and isEnemy == False:
                isEnemy = True
            elif not enemyGroup and isEnemy == True:
                isEnemy = False
                enemyGroup = CreateEnemies(SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SIZE, enemyFireRate, enemySpeed, 10)

            # Check if enough time has passed to drop a bomb, if so, drop bomb
            if isBomb == False:
                newBombs = CreateProjectile(SCREEN_WIDTH, SCREEN_HEIGHT, enemyGroup, ENEMY, BOMB, BOMB_SIZE, BOMB_SIZE, bombSpeed)
                bombGroup.add(newBombs)
                lastBombTime = pygame.time.get_ticks()
                isBomb = True
            elif isBomb == True and pygame.time.get_ticks() - lastBombTime >= enemy.GetEnemyFireRate():
                isBomb = False
            else:
                for bomb in bombGroup:
                    if isBomb == True and bomb.GetCurrentPosition()[1] > SCREEN_HEIGHT + 100:
                        bomb.kill()
                    elif pygame.sprite.groupcollide(starshipGroup, bombGroup, True, True):
                        # gameActive = False
                        gameOverTime = pygame.time.get_ticks()
                        calculateScore = True
                        gameOver = True
                        ClearAllGroups((bombGroup, laserGroup, starshipGroup, enemyGroup))
                    elif pygame.sprite.groupcollide(bombGroup, laserGroup, True, True):
                        isLaser = False
                        levelScore += 5
                if len(bombGroup) == 0:
                    isBomb = False

            # If any enemy is nearing the edge of the screen, update the moveDirection variable;
            # this variable is then passed into the enemy group update method to move all of the
            # enemies in the correct direction
            for enemy in enemyGroup:
                xPosition = enemy.GetCurrentPosition()[0]
                width = enemy.GetEnemyWidth()
                if xPosition - (width / 2) < 10:
                    moveDirection = RIGHT
                    dropOneRow = True
                    break
                elif xPosition + (width / 2) > SCREEN_WIDTH - 10:
                    moveDirection = LEFT
                    dropOneRow = True
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
                enemyGroup.update(LEFT, dropOneRow)         # update the x and y coordinates of the enemies
            elif moveDirection == RIGHT:
                enemyGroup.update(RIGHT, dropOneRow)        # update the x and y coordinates of the enemies

            # Display the current score
            scoreSurf = SCORE_FONT.render(f'Score: {levelScore}', True, WHITE)
            scoreRect = scoreSurf.get_rect(topleft = (SCREEN_WIDTH / 10, 8))
            SCREEN.blit(scoreSurf, scoreRect)
            if enemiesHit > 0:
                playerAccuracy = int((enemiesHit / lasersFired) * 100)
            accuracySurf = SCORE_FONT.render(f'Accuracy: {playerAccuracy} %', True, WHITE)
            accuracyRect = accuracySurf.get_rect(topright = (SCREEN_WIDTH / 8 * 7, 8))
            SCREEN.blit(accuracySurf, accuracyRect)

        else:
            newGameButton = MainMenu(SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, BG_IMAGE, TITLE_FONT, ORANGE, BUTTON_FONT, RED, GREEN)

        if gameOver and calculateScore:
            totalScore = int(totalScore + levelScore + (10000 * (playerAccuracy / 100)))
            calculateScore = False

        if gameOver and gameOverTime + 5000 > pygame.time.get_ticks():
            finalScoreSurf = SCORE_FONT.render(f'Final Score: {totalScore}', True, WHITE)
            finalScoreRect = finalScoreSurf.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            SCREEN.fill(BLACK)
            SCREEN.blit(finalScoreSurf, finalScoreRect)
        elif gameOver and gameOverTime + 5000 < pygame.time.get_ticks():
            gameActive = False
            gameOver = False
            lasersFired = 0
            enemiesHit = 0
            playerAccuracy = 0
            levelScore = 0
            totalScore = 0
            
        # apply all of the updates to the display surface
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

def CreateTextBox(screen, screenWidth, screenHeight, font, text, fontColor, rectCenter, background = False, backgroundColor = None, backgroundPadding = 0):
    surf = font.render(text, True, fontColor)
    rect = surf.get_rect(center = rectCenter)

    if background:
        bgSurf = pygame.Surface((surf.get_width() + backgroundPadding, surf.get_height() + backgroundPadding))
        bgRect = surf.get_rect(center = ((screenWidth / 2), (screenHeight / 2)))
        bgSurf.fill(backgroundColor)
        screen.blit(bgSurf, bgRect)
        screen.blit(surf, rect)
        return bgSurf, bgRect
    else:
        screen.blit(surf, rect)
        return surf, rect

# Function for the main menu screen, which should be displayed when the user first starts
# or when the escape key is pressed; however, the escape key would pull up the main menu
# in a pause game state.
def MainMenu(screen, screenWidth, screenHeight, background, titleFont, titleColor, buttonFont, buttonFontColor, buttonColor):
    screen.blit(background, (0, 0))
    _, newGameRect = CreateTextBox(screen, screenWidth, screenHeight, buttonFont, 'New Game', buttonFontColor, (screenWidth / 2, screenHeight / 2), True, buttonColor)
    CreateTextBox(screen, screenWidth, screenHeight, titleFont, 'Space Marauders', titleColor, (screenWidth / 2, screenHeight / 6))
    
    return newGameRect

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

def DisplayScore():
    pass

def ClearAllGroups(groupList):
    for group in groupList:
        group.empty()

# Call main function
if __name__ == '__main__':
    main()