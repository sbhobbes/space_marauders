'''
This module contains the runtime functions for the game state.
'''
import sys
import pygame
import space_marauders


# Level start animation
def game_start_animation():
    '''
    Call the animation at the start of the game.
    '''
    pass


def check_collision(is_laser, groups, enemies_hit, level_score):
    laser_group = groups['laser_group']
    enemy_group = groups['enemy_group']
    bomb_group = groups['bomb_group']
    starship_group = groups['starship_group']

    if is_laser is True:
        for laser in laser_group:
            if laser.get_current_position()[1] < - 100:
                is_laser = False

            elif pygame.sprite.groupcollide(laser_group, enemy_group, True, True):
                is_laser = False
                enemies_hit += 1
                level_score += 25
                if len(enemy_group) == 0:
                    game_over_time = pygame.time.get_ticks()
                    calculate_score = True
                    game_over = True
                    space_marauders.game_management.runtime.clear_all_groups([
                        bomb_group,
                        laser_group,
                        starship_group,
                        enemy_group
                    ])
                    level_score += 1000

    return is_laser


# Display game over animation upon player death
def game_over_animation():
    '''
    Call the game over animation.
    '''
    pass


def clear_all_groups(groups):
    '''
    Remove all groups from the screen.
    '''
    for _, group in groups.items():
        group.empty()


# Check for quit event
def check_for_quit():
    """check user inputs to see if the game should continue or terminate"""

    # Loop through all events of type QUIT
    for event in pygame.event.get(pygame.QUIT):

        # If QUIT event found, call terminate function
        terminate()

    # Loop through keyup events to check for Esc key input
    for event in pygame.event.get(pygame.KEYUP):

        # if key up is the Esc key then call terminate function to exit game
        if event.key == pygame.K_ESCAPE:
            terminate()

        # if key up is not the Esc key then put it back into the event queue
        else:
            pygame.event.post(event)


# Quit function
def terminate():
    """This function quits the game and terminates code execution"""
    pygame.quit()
    sys.exit()
