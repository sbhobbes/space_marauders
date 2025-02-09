'''
Module for firing projectiles.
'''
import pygame
import space_marauders


# Create laser function
def create_projectile(
    ship_group: pygame.sprite.Group,
    origin_type: str,
    projectile_type: str,
    projectile_width: int,
    projectile_length: int,
    projectile_speed: int
):
    '''
    Create a projectile fired from the player starship.
    '''
    # Create the projectile group object
    group = pygame.sprite.Group()

    # Create the projectile objects and add to a group
    for ship in ship_group:
        ship_x_position, ship_y_position = ship.get_current_position()
        projectile = space_marauders.objects.projectile.Projectile(
            original_x_position=ship_x_position,
            original_y_position=ship_y_position,
            projectile_origin=origin_type,
            projectile_type=projectile_type,
            projectile_width=projectile_width,
            projectile_length=projectile_length,
            projectile_speed=projectile_speed
        )
        group.add(projectile)

    # Return the group of projectile objects to the calling function
    return group
