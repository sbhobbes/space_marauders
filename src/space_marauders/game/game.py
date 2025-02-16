import numpy as np
import pygame
# import space_marauders
from .. import aliens, base_objects, game_management, utils


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
        self.alien_speed = 2
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
        self. groups = {
            'starship_group': pygame.sprite.Group(),
            'enemy_group': pygame.sprite.Group(),
            'laser_group': pygame.sprite.Group(),
            'bomb_group': pygame.sprite.Group()
        }
        self.interface = game_management.layout.Screen()
        self.SCREEN = self.interface.get_screen()
        self.SCORE_FONT = pygame.font.Font(self.setup['font_name'], 20)


    def check_events(self):
        # Iterate through all game events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and self.new_game_button.collidepoint(pygame.mouse.get_pos()):
                self.game_active = True


    def check_game_state(self):
        if self.game_active:
            if len(self.groups['enemy_group']) == 0:
                self.groups['enemy_group'] = game_management.deploy.create_enemies(10)

            if not self.groups['starship_group']:
                self.groups['starship_group'] = game_management.deploy.create_starship()

            for alien in self.groups['enemy_group']:
                alien.rect.x += self.alien_speed

            group_rect = self.groups['enemy_group'].sprites()[0].rect.copy()
            for alien in self.groups['enemy_group']:
                group_rect.union_ip(alien.rect)

            if group_rect.left < 0 or group_rect.right > self.setup['screen_width']:
                self.alien_speed *= -1
                for alien in self.groups['enemy_group']:
                    alien.rect.y += self.alien_drop_amount

            self.check_collisions()
            self.repaint_screen()
            self.update_score()

        else:
            self.new_game_button = self.interface.main_menu()

        self.check_game_over()

        pygame.display.update()


    def check_collisions(self):
        for alien in self.groups['enemy_group']:
            player_hit = pygame.sprite.spritecollide(self.groups['starship_group'], alien.projectiles, True)
            if player_hit:
                self.game_over = True

        for projectile in self.groups['starship_group'].projectiles:
            alien_hit = pygame.sprite.spritecollide(projectile, self.groups['enemy_group'], True)
            if alien_hit:
                projectile.kill()
                # Add scoring here

            for alien in self.groups['enemy_group']:
                projectile_collision = pygame.sprite.spritecollide(projectile, alien.projectiles, True)
                if projectile_collision:
                    projectile.kill()


    def repaint_screen(self):
        self.interface.blit(self.interface.background, (0, 0))       # background image; z-score = 1
        for _, obj in self.groups.items():
            if isinstance(obj, pygame.sprite.Group):
                for sprite in obj:
                    if isinstance(sprite, base_objects.base_starship.BaseStarship):
                        sprite.projectiles.draw(self.interface)

            obj.update()
            obj.draw(self.interface)


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
