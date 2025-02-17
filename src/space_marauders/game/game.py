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

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.level = 1
        self.alien_speed = 1
        self.alien_drop_amount = 20
        self.game_over = False
        self.level_completed = False
        self.calculate_score = False
        self.setup = utils.helpers.get_metadata('setup.yaml')
        self.fps_clock = pygame.time.Clock()
        self.active_game = False
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
        for event in pygame.event.get():
            game_management.runtime.check_for_quit(event)
            if event.type == pygame.MOUSEBUTTONDOWN and self.new_game_button.collidepoint(pygame.mouse.get_pos()):
                self.active_game = True

            if self.player is not None:
                self.player.handle_event(event)


    def check_game_state(self):
        if self.active_game:
            if not self.aliens:
                self.aliens = game_management.deploy.create_enemies(object_count=10, projectile_group=self.alien_projectiles_group)
                self.all_sprites.add(self.aliens)

            self.all_sprites.add(self.alien_projectiles_group)
            self.all_sprites.add(self.player_projectiles_group)

            if not self.player:
                self.player = game_management.deploy.create_starship(projectile_group=self.player_projectiles_group)
                self.all_sprites.add(self.player)

            for alien in self.aliens:
                alien.rect.x += self.alien_speed

            group_rect = self.aliens.sprites()[0].rect.copy()
            for alien in self.aliens:
                group_rect.union_ip(alien.rect)

            if group_rect.left < 0 or group_rect.right > self.setup['screen_width']:
                self.alien_speed *= -1
                for alien in self.aliens:
                    alien.rect.y += self.alien_drop_amount

            self.check_collisions()
            self.repaint_screen()
            self.update_score()

        else:
            self.new_game_button = self.interface.main_menu()

        self.check_end_of_level()
        self.check_game_over()


    def check_collisions(self):
        # for alien in self.aliens:
        if pygame.sprite.spritecollide(self.player, self.alien_projectiles_group, True):
            self.game_over = True

        for projectile in self.player_projectiles_group:
            if pygame.sprite.spritecollide(projectile, self.aliens, True):
                projectile.kill()
                self.player.update_score(50 * self.level)
                self.player.update_aliens_hit()

            if pygame.sprite.spritecollide(projectile, self.alien_projectiles_group, True):
                projectile.kill()
                self.player.update_score(5 * self.level)


    def repaint_screen(self):
        self.interface.refresh_screen()
        self.player.projectiles.draw(self.interface)
        self.all_sprites.draw(self.interface)
        self.all_sprites.update()


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
            self.end_of_level_splash_screen()


    def end_of_level_splash_screen(self):
        splash_text =[
            f'Level {self.level} completed!',
            f'Level score: {self.player.get_current_score()}',
            f'Total score: {self.player.get_current_score()}',
            f'Shots fired: {self.player.shots_fired}',
            f'Alien ships hit: {self.player.aliens_hit}',
            f'Accuracy: {self.player.get_accuracy()} %'
        ]
        start_y = self.setup['screen_height'] // 3
        line_spacing = 30

        self.SCREEN.fill(self.BLACK)
        for i, line in enumerate(splash_text):
            text = self.SCORE_FONT.render(line, True, self.WHITE)
            text_rect = text.get_rect(center=(self.setup['screen_width'] // 2, start_y + i * line_spacing))
            self.SCREEN.blit(text, text_rect)

        pygame.display.flip()

        pygame.time.delay(2000)

        self.level += 1
        self.reset_for_next_level()


    def reset_for_next_level(self):
        self.level_completed = False
        self.all_sprites.empty()

        self.alien_speed = round((self.alien_speed * 1.1), 2)
        self.player.reset_position()
        self.all_sprites.add(self.player)

        self.active_game = True


    def game_over_screen(self):
        game_over_text = [
            'Game Over!',
            f'High level completed: {self.level - 1}',
            f'Level score: {self.player.get_current_score()}',
            f'Final score: {self.player.get_current_score()}',
            f'Shots fired: {self.player.shots_fired}',
            f'Alien ships hit: {self.player.aliens_hit}',
            f'Accuracy: {self.player.get_accuracy()} %'
        ]
        start_y = self.setup['screen_height'] // 3
        line_spacing = 30

        self.SCREEN.fill(self.BLACK)
        for i, line in enumerate(game_over_text):
            text = self.SCORE_FONT.render(line, True, self.WHITE)
            text_rect = text.get_rect(center=(self.setup['screen_width'] // 2, start_y + i * line_spacing))
            self.SCREEN.blit(text, text_rect)

        pygame.display.flip()


    def check_game_over(self):
        if self.game_over and not self.level_completed:
            self.game_over_screen()
            # self.total_score = int(self.total_score + self.level_score + (10000 * (self.player_accuracy / 100)))
            # self.calculate_score = False

        # if self.game_over and self.game_over_time + 5000 > pygame.time.get_ticks():
        #     finalscore_surface = self.SCORE_FONT.render(f'Final Score: {self.total_score}', True, self.WHITE)
        #     finalscore_rectangle = finalscore_surface.get_rect(center = (self.setup['screen_width'] / 2, self.setup['screen_height'] / 2))
        #     self.SCREEN.fill(self.BLACK)
        #     self.SCREEN.blit(finalscore_surface, finalscore_rectangle)

        # if self.active_game and self.level_completed:
        #     self.all_sprites.remove()

        # elif self.game_over and self.game_over_time + 5000 < pygame.time.get_ticks():
        #     self.active_game = False
        #     self.game_over = False
        #     self.lasers_fired = 0
        #     self.enemies_hit = 0
        #     self.player_accuracy = 0
        #     self.level_score = 0
        #     self.total_score = 0


    def run(self):
        run_game = True

        while run_game is True:
            self.check_events()
            self.check_game_state()
            pygame.display.flip()
            self.fps_clock.tick(self.setup['fps'])
