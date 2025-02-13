import pygame
import space_marauders


# Create player starship function
def create_starship():
    '''
    Create a player starship.
    '''
    # Create the starship group object
    group = space_marauders.starships.starship.PlayerStarshipGroup()
    group.deploy()

    # Return the starship group object to the calling function
    return group


# Create enemies function
def create_enemies(
    object_count: int
):
    '''
    Create enemies on the screen.
    '''
    # Create the enemies group object
    group = space_marauders.aliens.starship.AlienStarshipGroup(alien_count=object_count)
    group.deploy()

    # Return the group of enemy objects to the calling function
    return group
