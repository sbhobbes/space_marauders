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
        self.button_font = pygame.font.Font(self.setup['font_name'], 30)
        self.title_font = pygame.font.Font(self.setup['font_name'], 100)
        # self.button_font_color = (255, 0, 0)
        # self.button_color = (0, 255, 0)
        # self.title_color = (255, 165, 0)
        self.button_font_color = (255, 250, 205)
        self.button_color = (0, 128, 128)
        self.title_color = (0, 128, 128)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.ORIGIN = (0, 0)
        self.SCORE_FONT = pygame.font.Font(self.setup['font_name'], 20)
        self.new_game_button_state = 'normal'
        self.demo_mode_button_state = 'normal'
        self.demo_mode_checkbox = self.create_demo_mode_checkbox()


    def get_screen(self):
        return self.screen


    def check_for_esc(self, game, event):
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE and game.active_game:
            game.active_game = False
            game.demo_mode = False
            game.all_sprites.empty()
            game.player = None
            game.aliens = None
            game.projectiles = None
            game.alien_projectiles_group.empty()
            game.player_projectiles_group.empty()


    def main_menu(self, all_sprites) -> pygame.rect:
        '''
        Function for the main menu screen, which should be displayed when the user first starts
        or when the escape key is pressed; however, the escape key would pull up the main menu
        in a pause game state.
        '''
        all_sprites.empty()
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

        self.demo_mode_checkbox.draw(self.screen)
        self.screen.blit(self.demo_mode_label, self.demo_mode_label_rect)

        self.create_text_box(
            font=self.title_font,
            text='Space Marauders',
            font_color=self.title_color,
            rectangle_center=(self.setup['screen_width'] / 2, self.setup['screen_height'] / 6)
        )

        return new_game_rectangle#, demo_mode_rectangle


    def create_demo_mode_checkbox(self):
        text_position_x = 150
        text_position_y = self.setup['screen_height'] // 15 * 14

        font = pygame.font.Font(None, 36)
        self.demo_mode_label = font.render('Demo Mode', True, self.button_font_color)
        self.demo_mode_label_rect = self.demo_mode_label.get_rect()

        self.demo_mode_label_rect.center = (text_position_x, text_position_y)

        checkbox_size = 30
        checkbox_x = self.demo_mode_label_rect.left - checkbox_size - 10
        checkbox_y = self.demo_mode_label_rect.centery - checkbox_size // 2

        checkbox = Checkbox(checkbox_x, checkbox_y)
        checkbox.draw(self.screen)

        return checkbox


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
        normal_background_color = (50, 100, 150)
        hover_backround_color = (70, 120, 170)
        pressed_background_color = (30, 80, 130)

        surface = font.render(text, True, font_color)
        rectangle = surface.get_rect(center=rectangle_center)

        if self.new_game_button_state == 'normal' and background_color is not None:
            self.draw_gradient_button(
                surface=surface,
                background_padding=background_padding,
                rectangle=rectangle,
                background_color=normal_background_color
            )

        elif self.new_game_button_state == 'hover' and background_color is not None:
            self.draw_gradient_button(
                surface=surface,
                background_padding=background_padding,
                rectangle=rectangle,
                background_color=hover_backround_color
            )

        elif self.new_game_button_state == 'pressed' and background_color is not None:
            self.draw_gradient_button(
                surface=surface,
                background_padding=background_padding,
                rectangle=rectangle,
                background_color=pressed_background_color
            )

        self.screen.blit(surface, rectangle)

        return surface, rectangle


    def draw_gradient_button(self, surface, background_padding, rectangle, background_color, border_radius=10):
        # Get dimensions of the text surface
        text_width = surface.get_width()
        text_height = surface.get_height()
        
        # Set explicit padding amounts
        horizontal_padding = 30  # Total horizontal padding (15px on each side)
        vertical_padding = 20    # Total vertical padding (10px on each side)
        
        # Calculate button dimensions based on text size plus padding
        button_width = text_width + horizontal_padding
        button_height = text_height + vertical_padding
        
        # Create button surface with transparency
        button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        
        # Draw rounded rectangle on button surface
        pygame.draw.rect(
            button_surface,
            background_color,
            pygame.Rect(0, 0, button_width, button_height),
            border_radius=border_radius
        )
        
        # Calculate position to center the text on the button
        text_x = (button_width - text_width) // 2
        text_y = (button_height - text_height) // 2
        
        # Blit the text onto the button surface
        button_surface.blit(surface, (text_x, text_y))
        
        # Blit the entire button onto the screen
        # Use the center of the original rectangle to position the new button
        original_center = rectangle.center
        new_rect = button_surface.get_rect(center=original_center)
        
        self.screen.blit(button_surface, new_rect)


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


class Checkbox:
    def __init__(self, x, y, size=30, color=(255, 255, 255), checked=False):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.checked = checked
        self.size = size
        self.check_thickness = max(2, int(size / 10))


    def draw(self, surface):
        self.surface = surface
        pygame.draw.rect(surface, self.color, self.rect, 2)

        if self.checked:
            start_pos1 = (self.rect.x + self.size * 0.2, self.rect.y + self.size * 0.2)
            end_pos1 = (self.rect.x + self.size * 0.8, self.rect.y + self.size * 0.8)
            start_pos2 = (self.rect.x + self.size * 0.8, self.rect.y + self.size * 0.2)
            end_pos2 = (self.rect.x + self.size * 0.2, self.rect.y + self.size * 0.8)

            pygame.draw.line(surface, self.color, start_pos1, end_pos1, self.check_thickness)
            pygame.draw.line(surface, self.color, start_pos2, end_pos2, self.check_thickness)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                print(self.checked)
                self.checked = not self.checked
                self.draw(self.surface)

                return True

        else:
            self.draw(self.surface)
            return False
