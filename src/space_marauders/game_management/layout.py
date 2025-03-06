'''
Module to configure the GUI.

Author: Seth Hobbes
Company: Springboro Technologies, LLC DBA Monarch Technologies
Date: 1/20/2022
Property of Seth Hobbes, member of Monarch Technologies, all rights reserved
Image assets credit to: https://github.com/exewin https://exewin.github.io/
'''
import pygame
import space_marauders


class Screen():
    def __init__(self):
        self.setup = space_marauders.utils.helpers.get_metadata('setup.yaml')
        self.screen = pygame.display.set_mode((self.setup['screen_width'], self.setup['screen_height']), pygame.SRCALPHA)
        self.background_image = space_marauders.utils.helpers.load_asset(self.setup['background_image'])
        # self.background_image.set_alpha(150)
        self.background = pygame.transform.scale(self.background_image, (self.setup['screen_width'], self.setup['screen_height']))
        self.button_font = pygame.font.Font(self.setup['font_name'], 50)
        self.title_font = pygame.font.Font(self.setup['font_name'], 100)
        self.button_font_color = (255, 0, 0)
        self.button_color = (0, 255, 0)
        self.title_color = (255, 165, 0)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.ORIGIN = (0, 0)
        self.SCORE_FONT = pygame.font.Font(self.setup['font_name'], 20)


    def get_screen(self):
        return self.screen


    def main_menu(self) -> pygame.rect:
        '''
        Function for the main menu screen, which should be displayed when the user first starts
        or when the escape key is pressed; however, the escape key would pull up the main menu
        in a pause game state.
        '''
        # self.screen.fill((180, 180, 180))
        self.screen.blit(self.background, (0, 0))
        _, new_game_rectangle = self.create_text_box(
            font=self.button_font,
            text='New Game',
            font_color=self.button_font_color,
            rectangle_center=(self.setup['screen_width'] / 2, self.setup['screen_height'] / 2),
            background=True,
            background_color=self.button_color
        )
        _, demo_mode_rectangle = self.create_text_box(
            font=self.button_font,
            text='Demo Mode',
            font_color=self.button_font_color,
            rectangle_center=(self.setup['screen_width'] / 2, self.setup['screen_height'] / 5 * 3),
            background=True,
            background_color=self.button_color
        )
        self.create_text_box(
            font=self.title_font,
            text='Space Marauders',
            font_color=self.title_color,
            rectangle_center=(self.setup['screen_width'] / 2, self.setup['screen_height'] / 6)
        )

        return new_game_rectangle, demo_mode_rectangle


    def create_text_box(
        self,
        font,
        text,
        font_color,
        rectangle_center,
        background=False,
        background_color=None,
        background_padding=0
    ):
        '''
        Create a pygame text box.
        '''
        surface = font.render(text, True, font_color)
        rectangle = surface.get_rect(center=rectangle_center)

        if background:
            surface_width = surface.get_width()
            surface_height = surface.get_height()
            surface_dimensions = (surface_width + background_padding, surface_height + background_padding)
            background_surface = pygame.Surface(surface_dimensions)
            # background_rectangle = surface.get_rect(center = ((self.setup['screen_width'] / 2), (self.setup['screen_height'] / 2)))
            # background_rectangle = surface.get_rect(center=rectangle_center)
            background_rectangle = rectangle.copy()
            background_surface.fill(background_color)
            self.screen.blit(background_surface, background_rectangle)
            self.screen.blit(surface, rectangle)
            return background_surface, background_rectangle

        else:
            self.screen.blit(surface, rectangle)
            return surface, rectangle


    def blit(self, *args, **kwargs):
        self.screen.blit(*args, **kwargs)


    def refresh_screen(self):
        self.screen.fill((180, 180, 180))
        self.blit(self.background, self.ORIGIN)


    def display_score(self):
        '''
        Display the scoreboard.
        '''
        pass


    def show_level_complete(self, player, level):
        splash_text =[
            f'Level {level} completed!',
            f'Level score: {player.get_current_score()}',
            f'Total score: {player.get_current_score()}',
            f'Shots fired: {player.shots_fired}',
            f'Alien ships hit: {player.aliens_hit}',
            f'Alien bombs hit: {player.bombs_hit}',
            f'Accuracy: {player.get_accuracy()} %'
        ]
        start_y = self.setup['screen_height'] // 3
        line_spacing = 30

        self.screen.fill(self.BLACK)
        for i, line in enumerate(splash_text):
            text = self.SCORE_FONT.render(line, True, self.WHITE)
            text_rect = text.get_rect(center=(self.setup['screen_width'] // 2, start_y + i * line_spacing))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

        pygame.time.delay(2000)

        level += 1

        return level


    def show_game_over(self, level, player):
        game_over_text = [
            'Game Over!',
            f'Highest level completed: {level - 1}',
            f'Level score: {player.get_current_score()}',
            f'Final score: {player.get_current_score()}',
            f'Shots fired: {player.shots_fired}',
            f'Alien ships hit: {player.aliens_hit}',
            f'Accuracy: {player.get_accuracy()} %'
        ]
        start_y = self.setup['screen_height'] // 3
        line_spacing = 30

        self.screen.fill(self.BLACK)
        for i, line in enumerate(game_over_text):
            text = self.SCORE_FONT.render(line, True, self.WHITE)
            text_rect = text.get_rect(center=(self.setup['screen_width'] // 2, start_y + i * line_spacing))
            self.screen.blit(text, text_rect)

        pygame.display.flip()
