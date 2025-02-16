import pygame
from .. import aliens, player, utils


# Create player starship function
def create_starship():
    '''
    Create a player starship.
    '''
    setup = utils.helpers.get_metadata('setup.yaml')
    # Create the starship group object
    # group = space_marauders.player.player_starship.PlayerStarshipGroup()
    # group.deploy()
    player_ship = player.player_starship.PlayerStarship(
        x=(setup['screen_width'] / 2),
        y=(setup['screen_height'] / 8 * 7.5),
        image_path='sky_blanc_2.png',
        speed=5,
        faction='player'
    )

    # Return the starship group object to the calling function
    # return group
    return player_ship


# Create enemies function
def create_enemies(
    object_count: int
):
    '''
    Create enemies on the screen.
    '''
    setup = utils.helpers.get_metadata('setup.yaml')
    # Create the enemies group object
    # group = aliens.alien_starship.AlienStarshipGroup(alien_count=object_count)
    # group.deploy()
    alien_group = pygame.sprite.Group()
    for i in range(object_count):
        alien = aliens.alien_starship.AlienStarship(
            100 + i * 100, 50, 'moroder_2.png', 2, 'aliens'
        )
        alien_group.add(alien)

    # Return the group of enemy objects to the calling function
    # return group
    return alien_group
