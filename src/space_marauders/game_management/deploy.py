import pygame
import space_marauders


# Create player starship function
def create_starship(screen_width, screen_height, starship_height, starship_width, starship_fire_rate):
    '''
    Create a player starship.
    '''
    # Create the starship group object
    group = pygame.sprite.Group()

    # Create the starship object
    starship = space_marauders.starships.starship.Starship(
        width=starship_width,
        height=starship_height,
        fire_rate=starship_fire_rate,
        starting_x_position=(screen_width / 2),
        starting_y_position=(screen_height / 8 * 7.5),
        move_rate=10
    )
    group.add(starship)

    # Return the starship group object to the calling function
    return group


# Create enemies function
def create_enemies(
    screen_width: int,
    screen_height: int,
    size: int,
    fire_rate: int,
    speed: int,
    enemy_count: int
):
    '''
    Create enemies on the screen.
    '''
    # Create the enemies group object
    group = pygame.sprite.Group()

    # create enemy spaceship objects and add to a group
    for enemy in range(enemy_count):
        new_enemy = space_marauders.aliens.starship.Enemy(
            width=size,
            height=size,
            fire_rate=fire_rate,
            starting_x_position=((screen_width / (enemy_count + 1)) * (enemy + 1)),
            starting_y_position=(screen_height / 8 * 0.5),
            move_rate=speed
        )
        group.add(new_enemy)

    # Return the group of enemy objects to the calling function
    return group
