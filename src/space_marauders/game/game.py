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
        self.alien_speed = 1
        self.alien_drop_amount = 20
        self.enemies_hit = 0
        self.level_score = 0
        self.total_score = 0
        self.lasers_fired = 0
        self.player_accuracy = 0
        self.game_over = False
        self.game_over_time = 0
        self.calculate_score = False
        self.setup = utils.helpers.get_metadata('setup.yaml')
        self.fps_clock = pygame.time.Clock()
        self.game_active = False
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
            if event.type == pygame.MOUSEBUTTONDOWN and self.new_game_button.collidepoint(pygame.mouse.get_pos()):
                self.game_active = True


    def check_game_state(self):
        if self.game_active:
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

        self.check_game_over()


    def check_collisions(self):
        for alien in self.aliens:
            if pygame.sprite.spritecollide(self.player, alien.projectiles, True):
                self.game_over = True

        for projectile in self.player.projectiles:
            if pygame.sprite.spritecollide(projectile, self.aliens, True):
                projectile.kill()

            for alien in self.aliens:
                if pygame.sprite.spritecollide(projectile, alien.projectiles, True):
                    projectile.kill()


    def repaint_screen(self):
        # self.SCREEN.fill((180, 180, 180))
        # self.SCREEN.blit(self.interface.background, (0, 0))
        # self.interface.blit(self.interface.background, (0, 0))
        self.interface.refresh_screen()
        # for sprite in self.all_sprites:
            # if isinstance(sprite, base_objects.base_starship.BaseStarship):
                # sprite.projectiles.draw(self.interface)

            # sprite.update()
        # self.alien_projectiles_group.draw(self.interface)
        self.player.projectiles.draw(self.interface)
        self.all_sprites.draw(self.interface)
        self.all_sprites.update()


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
            game_management.runtime.check_for_quit()
            self.check_events()
            self.check_game_state()
            pygame.display.flip()
            self.fps_clock.tick(self.setup['fps'])
