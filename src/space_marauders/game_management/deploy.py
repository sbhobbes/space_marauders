'''

Author: Seth Hobbes
Company: Springboro Technologies, LLC DBA Monarch Technologies
Date: 1/20/2022
Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
Image assets credit to: https://github.com/exewin https://exewin.github.io/
'''
import pygame
from .. import ai, aliens, player, utils


def create_starship(projectile_group: pygame.sprite.Group, game):
    '''
    Create a player starship.
    '''
    setup = utils.helpers.get_metadata('setup.yaml')

    if game is not None:
        player_ship = ai.player_bot.Bot(
            x=float(setup['screen_width'] / 2),
            y=float(setup['screen_height'] / 8 * 7),
            projectile_group=projectile_group,
            game=game
        )

    else:
        player_ship = player.player_starship.PlayerStarship(
            x=float(setup['screen_width'] / 2),
            y=float(setup['screen_height'] / 8 * 7),
            projectile_group=projectile_group
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
            # x=100.0 + i * 100.0,
            x=(1920 // (object_count + 2)) * i + 200,
            y=100.0,
            projectile_group=projectile_group
        )
        alien_group.add(alien)

    return alien_group
