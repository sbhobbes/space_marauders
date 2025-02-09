'''
This module holds the base class for all starships.  This class is not
intended to be used directly, but rather as a super class for the 
indivdual player and alien starships.
'''

import pygame
import space_marauders


class BaseStarship(pygame.sprite.Sprite):
    '''
    This is the base starship class.
    '''
    def __init__(self):
        super().__init__()
        setup = space_marauders.utils.helpers.get_metadata('screen_config.yaml')
        base_stats = space_marauders.utils.helpers.get_metadata('base_stats.yaml')

        self.LEFT = 'left'
        self.RIGHT = 'right'
