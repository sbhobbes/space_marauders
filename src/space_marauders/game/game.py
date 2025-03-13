'''

Author: Seth Hobbes
Company: Springboro Technologies, LLC DBA Monarch Technologies
Date: 1/20/2022
Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
Image assets credit to: https://github.com/exewin https://exewin.github.io/
'''
import pygame
from .. import game_management, utils


class Game():
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.delta_time = 0
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.level = 1
        # self.alien_speed = 1
        self.alien_drop_amount = 10
        self.game_over = False
        self.level_completed = False
        self.calculate_score = False
        self.x_accumulator = 0.0
        self.setup = utils.helpers.get_metadata('setup.yaml')
        self.alien_speed = self.setup['alien']['ship_speed']
        self.fps_clock = pygame.time.Clock()
        self.active_game = False
        self.demo_mode = False
        self.player = None
        self.aliens = None
        self.projectiles = None
        self.alien_projectiles_group = pygame.sprite.Group()
        self.player_projectiles_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.interface = game_management.layout.Screen()
        self.SCREEN = self.interface.get_screen()
        self.SCORE_FONT = pygame.font.Font(self.setup['font_name'], 20)


    def check_events(self):
        hover_color = ()
        normal_color = ()

        for event in pygame.event.get():
            game_management.runtime.check_for_quit(event)

            self.interface.check_for_esc(self, event)

            if hasattr(self, 'new_game_button'):
                if event.type == pygame.MOUSEMOTION:
                    if self.new_game_button.collidepoint(event.pos):
                        if self.interface.new_game_button_state != 'pressed':
                            self.interface.new_game_button_state = 'hover'
                            current_color = hover_color

                        else:
                            self.interface.new_game_button_state = 'normal'
                            new_game_current_color = normal_color

                    elif self.demo_mode_button.collidepoint(event.pos):
                        if self.interface.demo_mode_button_state != 'pressed':
                            self.interface.demo_mode_button_state = 'hover'

                        else:
                            self.interface.demo_mode_button_state = 'normal'
                            demo_mode_current_color = normal_color

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.new_game_button.collidepoint(pygame.mouse.get_pos()):
                        self.interface.new_game_button_state = 'pressed'

                    elif self.demo_mode_button.collidepoint(pygame.mouse.get_pos()):
                        self.interface.demo_mode_button_state = 'pressed'

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.new_game_button.collidepoint(event.pos):
                        self.interface.new_game_button_state = 'normal'
                        self.active_game = True

                    elif self.demo_mode_button.collidepoint(event.pos):
                        self.interface.demo_mode_button_state = 'normal'
                        self.active_game = True
                        self.demo_mode = True

            if self.player is not None:
                self.player.handle_event(event)


    def check_game_state(self):
        if self.active_game:# or self.demo_mode:
            if not self.aliens:
                self.aliens = game_management.deploy.create_enemies(object_count=10, projectile_group=self.alien_projectiles_group)
                self.all_sprites.add(self.aliens)

            self.all_sprites.add(self.alien_projectiles_group)
            self.all_sprites.add(self.player_projectiles_group)

            if not self.player:
                self.player = game_management.deploy.create_starship(
                    projectile_group=self.player_projectiles_group,
                    game=self if self.demo_mode else None
                )
                self.all_sprites.add(self.player)

            self.x_accumulator += self.alien_speed * self.delta_time
            if abs(self.x_accumulator) >= 1.0:
                pixels_to_move = int(abs(self.x_accumulator))
                direction = 1 if self.alien_speed > 0 else -1

                for alien in self.aliens:
                    alien.rect.x += (pixels_to_move * direction)

                self.x_accumulator -= (pixels_to_move * direction)

            group_rect = self.aliens.sprites()[0].rect.copy()
            for alien in self.aliens:
                group_rect.union_ip(alien.rect)

            if (group_rect.left < 5 and self.alien_speed < 0) or (group_rect.right > self.setup['screen_width'] - 5 and self.alien_speed > 0):
                self.alien_speed *= -1
                for alien in self.aliens:
                    alien.rect.y += self.alien_drop_amount# * self.delta_time

            self.check_collisions()
            self.repaint_screen()
            self.update_score()

        else:
            self.new_game_button, self.demo_mode_button = self.interface.main_menu(self.all_sprites)

        self.check_end_of_level()
        self.check_game_over()


    def check_collisions(self):
        if pygame.sprite.spritecollide(self.player, self.alien_projectiles_group, True):
            self.player.kill()
            self.game_over = True

        for projectile in self.player_projectiles_group:
            if pygame.sprite.spritecollide(projectile, self.aliens, True):
                projectile.kill()
                self.player.update_score(50 * self.level)
                self.player.update_aliens_hit()

            if pygame.sprite.spritecollide(projectile, self.alien_projectiles_group, True):
                projectile.kill()
                self.player.update_score(5 * self.level)
                self.player.update_bombs_hit()

            if projectile.rect.bottom < 0:
                projectile.kill()

        for projectile in self.alien_projectiles_group:
            if projectile.rect.top > self.setup['screen_height']:
                projectile.kill()


    def repaint_screen(self):
        self.interface.refresh_screen()
        self.all_sprites.draw(self.interface)
        self.all_sprites.update(delta_time=self.delta_time)


    def update_score(self):
        score_surface = self.SCORE_FONT.render(f'Score: {self.player.get_current_score()}', True, self.WHITE)
        score_rectangle = score_surface.get_rect(topleft = (self.setup['screen_width'] / 10, 8))
        self.SCREEN.blit(score_surface, score_rectangle)

        accuracy_surface = self.SCORE_FONT.render(f'Accuracy: {self.player.get_accuracy()} %', True, self.WHITE)
        accuracy_rectangle = accuracy_surface.get_rect(topleft = (self.setup['screen_width'] / 10 * 8, 8))
        self.SCREEN.blit(accuracy_surface, accuracy_rectangle)


    def check_end_of_level(self):
        if not self.aliens and self.active_game:
            self.level_completed = True
            self.level = self.interface.show_level_complete(self.player, self.level)
            self.reset_for_next_level()


    def reset_for_next_level(self):
        self.level_completed = False
        self.all_sprites.empty()

        self.alien_speed = round((self.alien_speed * 1.1), 2)
        self.player.reset_position()
        self.all_sprites.add(self.player)

        self.active_game = True
        self.fps_clock.tick()


    def check_game_over(self):
        if self.game_over and not self.level_completed:
            self.interface.show_game_over(self.level, self.player)


    def run(self):
        run_game = True

        while run_game is True:
            self.delta_time = self.fps_clock.tick(self.setup['fps']) / 1000
            self.check_events()
            self.check_game_state()
            pygame.display.flip()
            # self.fps_clock.tick(self.setup['fps'])
