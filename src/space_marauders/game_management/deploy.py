'''

Author: Seth Hobbes
Company: Springboro Technologies, LLC DBA Monarch Technologies
Date: 1/20/2022
Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
Image assets credit to: https://github.com/exewin https://exewin.github.io/
'''
import pygame
from .. import aliens, player, utils


def create_starship(projectile_group: pygame.sprite.Group):
    '''
    Create a player starship.
    '''
    setup = utils.helpers.get_metadata('setup.yaml')

    player_ship = player.player_starship.PlayerStarship(
        x=(setup['screen_width'] / 2),
        y=(setup['screen_height'] / 8 * 7.5),
        projectile_group=projectile_group
        # image_path='sky_blanc_2.png',
        # speed=5
    )

    return player_ship


def create_enemies(
    object_count: int,
    projectile_group: pygame.sprite.Group
) -> pygame.sprite.Group:
    '''
    Create enemies on the screen.
    '''
    setup = utils.helpers.get_metadata('setup.yaml')

    alien_group = pygame.sprite.Group()
    for i in range(object_count):
        alien = aliens.alien_starship.AlienStarship(
            x=100 + i * 100,
            y=50,
            projectile_group=projectile_group
            # image_path='moroder_2.png',
            # speed=1
        )
        alien_group.add(alien)

    return alien_group
