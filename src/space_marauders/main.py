# Author: Seth Hobbes
# Company: Springboro Technologies, LLC DBA Monarch Technologies
# Date: 1/20/2022
# Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
# Image assets credit to: https://github.com/exewin https://exewin.github.io/

import sys
import pygame
import space_marauders


# Main game function
def main():
    '''
    The main function.
    '''
    # Start the pygame engine and font module
    pygame.init()
    pygame.font.init()

    # Get metadata
    setup = space_marauders.utils.helpers.get_metadata('setup.yaml')

    # Declare constants
    SCREEN_WIDTH = setup['screen_width']
    SCREEN_HEIGHT = setup['screen_height']
    FPSCLOCK = pygame.time.Clock()      # clock object to control the maximum FPS
    LEFT = 'left'                       # movement direction for player starship
    RIGHT = 'right'                     # movement direction for player starship
    PLAYER = 'player'                   # value to pass to the projectile class call for origin point
    ENEMY = 'enemy'                     # value to pass to the projectile class call for origin point
    BOMB = 'bomb'                       # value to pass into the projectile class call for projectile type
    LASER = 'laser'                     # value to pass into the projectile class call for projectile type

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Declare variables
    enemy_speed = 1                      # enemy ship starting speed, impacted by multipliers
    bomb_speed = 4                       # bomb speed starting value, impacted by multipliers
    laser_speed = 10                     # laser speed starting value, impacted by multipliers
    starship_fire_rate = 5000             # time in milliseconds between starship projectiles, impacted by multipliers
    enemy_fire_rate = 5000                # time in milliseconds between enemy projectiles, impacted by multipliers
    is_laser = False                     # flag to check if a player projectile active on the screen or not
    is_enemy = False                     # flag to check if an enemy is present on the screen or not
    is_bomb = False                      # flag to check if a bomb is present on the screen or not
    current_level = 0                    # value of the current level
    level_score = 0                      # score for the current level
    total_score = 0                      # cumulative score the game across all levels played
    lasers_fired = 0                     # the number of lasers fired
    enemies_hit = 0                      # the number of enemies hit by the player
    player_accuracy = 0                  # the accuracy percentage of lasers fired over enemies hit
    move_direction = LEFT                # holds the direction that all enemy objects should move along the x axis
    game_active = False                  # flag for the active game state
    game_over = False                    # flag for end of game state
    game_over_time = 0                    # the time that the game ended; used to hold the score screen for a preset amount of time
    calculate_score = False
    
    # Create the game display area, assign it to the SCREEN constant, and apply the background image
    game = space_marauders.game_management.layout.Screen()
    SCREEN = game.get_screen()
    SCORE_FONT = pygame.font.Font(setup['font_name'], 20)

    # Create groups to hold projectile objects
    groups = {
        'starship_group': pygame.sprite.Group(),
        'enemy_group': pygame.sprite.Group(),
        'laser_group': pygame.sprite.Group(),
        'bomb_group': pygame.sprite.Group()
    }

    # Game loop
    while True:
        drop_one_row = False

        # Set maximum framerate
        FPSCLOCK.tick(setup['fps'])

        # Check user input for quit events and escape key
        space_marauders.game_management.runtime.check_for_quit()

        # Create laser object if spacebar is pressed
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and game_active:
                if is_laser is False and groups['starship_group']:
                    groups['laser_group'] = space_marauders.game_management.fire.create_projectile(
                        groups['starship_group'],
                        PLAYER,
                        LASER,
                        setup['laser_width'],
                        setup['laser_length'],
                        laser_speed
                    )
                    lasers_fired += 1
                    is_laser = True

            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                pass

            elif event.type == pygame.MOUSEBUTTONDOWN and new_game_button.collidepoint(pygame.mouse.get_pos()):
                game_active = True

            elif event.type == pygame.MOUSEBUTTONDOWN and not new_game_button.collidepoint(pygame.mouse.get_pos()):
                pass

            else:
                pygame.event.post(event)

        # check game state for active game and update display accordingly
        if game_active:
            if len(groups['enemy_group']) == 0:
                # Create enemies
                groups['enemy_group'] = space_marauders.game_management.deploy.create_enemies(
                    enemy_fire_rate,
                    enemy_speed,
                    10
                )

            if len(groups['starship_group']) == 0:
                # create player starship object
                groups['starship_group'] = space_marauders.game_management.deploy.create_starship(starship_fire_rate)

            groups['starship_group'].update()

            # Check for laser existence and collision
            is_laser = space_marauders.game_management.runtime.check_collision(
                is_laser=is_laser,
                groups=groups,
                enemies_hit=enemies_hit,
                level_score=level_score
            )

            # Check to see if new enemy should be created; will later be replaced by levels, scoring, and resets
            if groups['enemy_group'] and is_enemy is False:
                is_enemy = True
            elif not groups['enemy_group'] and is_enemy is True:
                is_enemy = False
                groups['enemy_group'] = space_marauders.game_management.deploy.create_enemies(
                    fire_rate=enemy_fire_rate,
                    speed=enemy_speed,
                    object_count=10
                )

            # Check if enough time has passed to drop a bomb, if so, drop bomb
            if is_bomb is False:
                new_bombs = space_marauders.game_management.fire.create_projectile(
                    groups['enemy_group'],
                    ENEMY,
                    BOMB,
                    setup['bomb_size'],
                    setup['bomb_size'],
                    bomb_speed
                )
                groups['bomb_group'].add(new_bombs)
                last_bomb_time = pygame.time.get_ticks()
                is_bomb = True

            elif is_bomb is True and pygame.time.get_ticks() - last_bomb_time >= enemy.get_enemy_fire_rate():
                is_bomb = False

            else:
                for bomb in groups['bomb_group']:
                    if is_bomb is True and bomb.get_current_position()[1] > SCREEN_HEIGHT + 100:
                        bomb.kill()

                    elif pygame.sprite.groupcollide(groups['starship_group'], groups['bomb_group'], True, True):
                        # game_active = False
                        game_over_time = pygame.time.get_ticks()
                        calculate_score = True
                        game_over = True
                        space_marauders.game_management.runtime.clear_all_groups([
                            groups['bomb_group'],
                            groups['laser_group'],
                            groups['starship_group'],
                            groups['enemy_group']
                        ])

                    elif pygame.sprite.groupcollide(groups['bomb_group'], groups['laser_group'], True, True):
                        is_laser = False
                        level_score += 5

                if len(groups['bomb_group']) == 0:
                    is_bomb = False

            # If any enemy is nearing the edge of the screen, update the move_direction variable;
            # this variable is then passed into the enemy group update method to move all of the
            # enemies in the correct direction
            for enemy in groups['enemy_group']:
                x_position = enemy.get_current_position()[0]
                width = enemy.get_enemy_width()
                if x_position - (width / 2) < 10:
                    move_direction = RIGHT
                    drop_one_row = True
                    break

                if x_position + (width / 2) > SCREEN_WIDTH - 10:
                    move_direction = LEFT
                    drop_one_row = True
                    break

            # Draw group objects to the screen in order from lowest z-score to highest z-score;
            # if the display surface (SCREEN) has a z-score of 0, then:
            game.blit(game.background, (0, 0))       # background image; z-score = 1
            groups['laser_group'].draw(game)             # draw lasers; z-score = 2
            groups['bomb_group'].draw(game)              # draw bombs; z-score = 3
            groups['enemy_group'].draw(game)             # draw enemies; z-score = 4
            groups['starship_group'].draw(game)          # draw starship; z-score = 5

            # Update all object positions
            groups['laser_group'].update()                 # update the y coordinate of the laser; x coordinate is static
            groups['bomb_group'].update()                  # update the y coordinate of the bombs; x coordinate is static        
            if move_direction == LEFT:           
                groups['enemy_group'].update(LEFT, drop_one_row)         # update the x and y coordinates of the enemies

            elif move_direction == RIGHT:
                groups['enemy_group'].update(RIGHT, drop_one_row)        # update the x and y coordinates of the enemies

            # Display the current score
            score_surface = SCORE_FONT.render(f'Score: {level_score}', True, WHITE)
            score_rectangle = score_surface.get_rect(topleft = (SCREEN_WIDTH / 10, 8))
            SCREEN.blit(score_surface, score_rectangle)
            if enemies_hit > 0:
                player_accuracy = int((enemies_hit / lasers_fired) * 100)

            accuracy_surface = SCORE_FONT.render(f'Accuracy: {player_accuracy} %', True, WHITE)
            accuracy_rectangle = accuracy_surface.get_rect(topright = (SCREEN_WIDTH / 8 * 7, 8))
            SCREEN.blit(accuracy_surface, accuracy_rectangle)

        else:
            new_game_button = game.main_menu()

        if game_over and calculate_score:
            total_score = int(total_score + level_score + (10000 * (player_accuracy / 100)))
            calculate_score = False

        if game_over and game_over_time + 5000 > pygame.time.get_ticks():
            finalscore_surface = SCORE_FONT.render(f'Final Score: {total_score}', True, WHITE)
            finalscore_rectangle = finalscore_surface.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            SCREEN.fill(BLACK)
            SCREEN.blit(finalscore_surface, finalscore_rectangle)

        elif game_over and game_over_time + 5000 < pygame.time.get_ticks():
            game_active = False
            game_over = False
            lasers_fired = 0
            enemies_hit = 0
            player_accuracy = 0
            level_score = 0
            total_score = 0

        # apply all of the updates to the display surface
        pygame.display.update()


# Call main function
if __name__ == '__main__':
    main()
