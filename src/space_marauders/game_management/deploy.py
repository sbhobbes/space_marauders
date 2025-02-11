import pygame
import space_marauders


# Create player starship function
def create_starship():
    '''
    Create a player starship.
    '''
    setup = space_marauders.utils.helpers.get_metadata('setup.yaml')

    # Create the starship group object
    group = pygame.sprite.Group()

    # Create the starship object
    starship = space_marauders.starships.starship.Starship(
        width=setup['player_ship_size'],
        height=setup['player_ship_size'],
        fire_rate=setup['player_fire_rate'],
        starting_x_position=(setup['screen_width'] / 2),
        starting_y_position=(setup['screen_height'] / 8 * 7.5),
        move_rate=10
    )
    group.add(starship)

    # Return the starship group object to the calling function
    return group


# Create enemies function
def create_enemies(
    object_count: int
):
    '''
    Create enemies on the screen.
    '''
    setup = space_marauders.utils.helpers.get_metadata('setup.yaml')

    # Create the enemies group object
    group = pygame.sprite.Group()

    # create enemy spaceship objects and add to a group
    for enemy in range(object_count):
        new_enemy = space_marauders.aliens.starship.Enemy(
            width=setup['alien_ship_size'],
            height=setup['alien_ship_size'],
            fire_rate=setup['alien_fire_rate'],
            starting_x_position=((setup['screen_width'] / (object_count + 1)) * (enemy + 1)),
            starting_y_position=(setup['screen_height'] / 8 * 0.5),
            move_rate=setup['alien_speed']
        )
        group.add(new_enemy)

    # Return the group of enemy objects to the calling function
    return group
