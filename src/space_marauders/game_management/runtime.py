'''
This module contains the runtime functions for the game state.
'''
import sys
import pygame


# Level start animation
def game_start_animation():
    '''
    Call the animation at the start of the game.
    '''
    pass


# Display game over animation upon player death
def game_over_animation():
    '''
    Call the game over animation.
    '''
    pass


def clear_all_groups(group_list):
    '''
    Remove all groups from the screen.
    '''
    for group in group_list:
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
