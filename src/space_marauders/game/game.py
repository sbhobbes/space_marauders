import numpy as np
import pygame
import space_marauders


class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.LASER = 'laser'
        self.PLAYER = 'player'
        self.ALIEN = 'enemy'
        self.BOMB = 'bomb'
        self.LEFT = 'left'
        self.RIGHT = 'right'
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.enemies_hit = 0
        self.level_score = 0
        self.total_score = 0
        self.lasers_fired = 0
        self.player_accuracy = 0
        self.is_laser = False
        self.is_enemy = False
        self.is_bomb = False
        self.drop_one_row = False
        self.move_direction = self.LEFT
        self.game_over = False
        self.game_over_time = 0
        self.last_bomb_time = 0
        self.calculate_score = False
        self.setup = space_marauders.utils.helpers.get_metadata('setup.yaml')
        self.fps_clock = pygame.time.Clock()
        self.game_active = False
        self. groups = {
            'starship_group': pygame.sprite.Group(),
            'enemy_group': pygame.sprite.Group(),
            'laser_group': pygame.sprite.Group(),
            'bomb_group': pygame.sprite.Group()
        }
        self.interface = space_marauders.game_management.layout.Screen()
        self.SCREEN = self.interface.get_screen()
        self.SCORE_FONT = pygame.font.Font(self.setup['font_name'], 20)


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and self.game_active:
                if self.is_laser is False and self.groups['starship_group']:
                    self.groups['laser_group'] = space_marauders.game_management.fire.create_projectile(
                        self.groups['starship_group'],
                        self.PLAYER
                    )
                    self.lasers_fired += 1
                    self.is_laser = True

            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                pass

            elif event.type == pygame.MOUSEBUTTONDOWN and self.new_game_button.collidepoint(pygame.mouse.get_pos()):
                self.game_active = True

            elif event.type == pygame.MOUSEBUTTONDOWN and not self.new_game_button.collidepoint(pygame.mouse.get_pos()):
                pass

            else:
                pygame.event.post(event)


    def check_game_state(self):
        if self.game_active:
            if len(self.groups['enemy_group']) == 0:
                # Create enemies
                self.groups['enemy_group'] = space_marauders.aliens.starship.AlienStarshipGroup()
                self.groups['enemy_group'].deploy()
                # self.groups['enemy_group'] = space_marauders.game_management.deploy.create_enemies(10)

            if len(self.groups['starship_group']) == 0:
                # create player starship object
                self.groups['starship_group'] = space_marauders.game_management.deploy.create_starship()

            self.groups['starship_group'].update()

            # Check for laser existence and collision
            self.is_laser = space_marauders.game_management.runtime.check_collision(
                is_laser=self.is_laser,
                groups=self.groups,
                enemies_hit=self.enemies_hit,
                level_score=self.level_score
            )

            self.check_enemy_state()
            self.check_bomb_state()
            self.check_enemy_position()
            self.repaint_screen()
            self.update_score()

        else:
            self.new_game_button = self.interface.main_menu()

        self.check_game_over()

        # apply all of the updates to the display surface
        pygame.display.update()


    def check_enemy_state(self):
        if self.groups['enemy_group'] and self.is_enemy is False:
            self.is_enemy = True

        elif not self.groups['enemy_group'] and self.is_enemy is True:
            self.is_enemy = False
            self.groups['enemy_group'] = space_marauders.game_management.deploy.create_enemies(10)


    def check_bomb_state(self):
        if self.is_bomb is False:
            new_bombs = space_marauders.game_management.fire.create_projectile(
                self.groups['enemy_group'],
                self.ALIEN
            )
            self.groups['bomb_group'].add(new_bombs)
            self.last_bomb_time = pygame.time.get_ticks()
            self.is_bomb = True

        elif self.is_bomb is True and pygame.time.get_ticks() - self.last_bomb_time >= np.max([x.get_enemy_fire_rate() for x in self.groups['enemy_group']]):
            self.is_bomb = False

        else:
            for bomb in self.groups['bomb_group']:
                if self.is_bomb is True and bomb.get_current_position()[1] > self.setup['screen_height'] + 100:
                    bomb.kill()

                elif pygame.sprite.groupcollide(self.groups['starship_group'], self.groups['bomb_group'], True, True):
                    self.game_over_time = pygame.time.get_ticks()
                    self.calculate_score = True
                    self.game_over = True
                    space_marauders.game_management.runtime.clear_all_groups(self.groups)

                elif pygame.sprite.groupcollide(self.groups['bomb_group'], self.groups['laser_group'], True, True):
                    self.is_laser = False
                    self.level_score += 5

            if len(self.groups['bomb_group']) == 0:
                self.is_bomb = False


    def check_enemy_position(self):
        self.move_direction, self.drop_one_row = self.groups['enemy_group'].check_boundary_collision()


    def repaint_screen(self):
        self.interface.blit(self.interface.background, (0, 0))       # background image; z-score = 1
        self.groups['laser_group'].draw(self.interface)             # draw lasers; z-score = 2
        self.groups['bomb_group'].draw(self.interface)              # draw bombs; z-score = 3
        self.groups['enemy_group'].draw(self.interface)             # draw enemies; z-score = 4
        self.groups['starship_group'].draw(self.interface)          # draw starship; z-score = 5

        # Update all object positions
        self.groups['laser_group'].update()                 # update the y coordinate of the laser; x coordinate is static
        self.groups['bomb_group'].update()                  # update the y coordinate of the bombs; x coordinate is static        
        if self.move_direction == self.LEFT:           
            self.groups['enemy_group'].update(self.LEFT, self.drop_one_row)         # update the x and y coordinates of the enemies
            self.drop_one_row = False

        elif self.move_direction == self.RIGHT:
            self.groups['enemy_group'].update(self.RIGHT, self.drop_one_row)        # update the x and y coordinates of the enemies
            self.drop_one_row = False


    def update_score(self):
        score_surface = self.SCORE_FONT.render(f'Score: {self.level_score}', True, self.WHITE)
        score_rectangle = score_surface.get_rect(topleft = (self.setup['screen_width'] / 10, 8))
        self.SCREEN.blit(score_surface, score_rectangle)
        if self.enemies_hit > 0:
            self.player_accuracy = int((self.enemies_hit / self.lasers_fired) * 100)

        accuracy_surface = self.SCORE_FONT.render(f'Accuracy: {self.player_accuracy} %', True, self.WHITE)
        accuracy_rectangle = accuracy_surface.get_rect(topright = (self.setup['screen_width'] / 8 * 7, 8))
        self.SCREEN.blit(accuracy_surface, accuracy_rectangle)


    def check_game_over(self):
        if self.game_over and self.calculate_score:
            self.total_score = int(self.total_score + self.level_score + (10000 * (self.player_accuracy / 100)))
            self.calculate_score = False

        if self.game_over and self.game_over_time + 5000 > pygame.time.get_ticks():
            finalscore_surface = self.SCORE_FONT.render(f'Final Score: {self.total_score}', True, self.WHITE)
            finalscore_rectangle = finalscore_surface.get_rect(center = (self.setup['screen_width'] / 2, self.setup['screen_height'] / 2))
            self.SCREEN.fill(self.BLACK)
            self.SCREEN.blit(finalscore_surface, finalscore_rectangle)

        elif self.game_over and self.game_over_time + 5000 < pygame.time.get_ticks():
            self.game_active = False
            self.game_over = False
            self.lasers_fired = 0
            self.enemies_hit = 0
            self.player_accuracy = 0
            self.level_score = 0
            self.total_score = 0


    def run(self):
        run_game = True

        while run_game is True:
            self.fps_clock.tick(self.setup['fps'])
            space_marauders.game_management.runtime.check_for_quit()
            self.check_events()
            self.check_game_state()
