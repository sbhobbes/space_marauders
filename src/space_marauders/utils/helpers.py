from importlib import resources
import pygame


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
