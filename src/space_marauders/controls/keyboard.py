# import pygame
# import space_marauders


# def check_player_input(groups, is_laser, game_active, player, new_game_button):
#     for event in pygame.event.get():
#         if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and game_active:
#             if is_laser is False and groups['starship_group']:
#                 groups['laser_group'] = space_marauders.game_management.fire.create_projectile(
#                     groups['starship_group'],
#                     player
#                 )
#                 lasers_fired += 1
#                 is_laser = True

#         elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
#             pass

#         elif event.type == pygame.MOUSEBUTTONDOWN and new_game_button.collidepoint(pygame.mouse.get_pos()):
#             game_active = True

#         elif event.type == pygame.MOUSEBUTTONDOWN and not new_game_button.collidepoint(pygame.mouse.get_pos()):
#             pass

#         else:
#             pygame.event.post(event)

#     return {
#         'groups': groups,
#         'is_laser': is_laser,
#         'player': player,
#         'lasers_i'
#     }
