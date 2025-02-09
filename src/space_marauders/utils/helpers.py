import pygame
import yaml
from importlib import resources


def load_asset(asset_name, base_path=None):
    '''
    Loads an image asset into the game.
    '''
    if base_path is None:
        with resources.path('space_marauders.assets', asset_name) as image_path:
            loaded_image = pygame.image.load(image_path).convert_alpha()

    else:
        with resources.path(f'space_marauders.assets.{base_path}', asset_name) as image_path:
            loaded_image = pygame.image.load(image_path).convert_alpha()

    return loaded_image


def get_metadata(file_name):
    '''
    Reads a yaml metadata file into a dict.
    '''
    if not file_name.endswith('.yaml'):
        file_name += '.yaml'

    with resources.path('space_marauders.metadata', file_name) as file_path:
        with open(file_path, encoding='utf-8') as stream:
            metadata = yaml.load(stream, Loader=yaml.Loader)

    return metadata
