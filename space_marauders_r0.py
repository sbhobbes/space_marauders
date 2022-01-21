import pygame, sys
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height, color, startingHealth, currentHealth, fireRate, weaponType, shipType, startPosX, 
    StartPosY, currentPosX, currentPosY, descentRate, baseDamage = 1, lastAttackTime = None):
        super().__init__()
        self.startingHealth = startingHealth
        self.currentHealth = currentHealth
        self.fireRate = fireRate
        self.weaponType = weaponType
        self.shipType = shipType
        self.currentPosX = currentPosX
        self.currentPosY = currentPosY
        self.descentRate = descentRate
        self.baseDamage = baseDamage
        self.lastAttackTime = lastAttackTime

        self.image = pygame.Surface((width, height))
        self.image.fill(color)
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
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

        pygame.display.flip()
        enemy_group.draw(SCREEN)
        starship_group.draw(SCREEN)
        FPSCLOCK.tick(FPS)

# Quit function
def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()