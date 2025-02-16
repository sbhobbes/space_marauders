'''
Module for firing projectiles.
'''
import pygame
import space_marauders


# Create laser function
def create_projectile(
    ship_group: pygame.sprite.Group,
    origin: str
):
    '''
    Create a projectile fired from the player starship.
    '''
    # Create the projectile group object
    # group = space_marauders.objects.projectile.ProjectileGroup(projectile_origin=origin, starship_group=ship_group)
    # group.fire()
    ship_group.update()

    # Return the group of projectile objects to the calling function
    # return group
