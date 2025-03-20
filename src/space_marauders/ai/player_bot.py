import numpy as np
from space_marauders.utils import helpers
from space_marauders.player.player_starship import PlayerStarship
from space_marauders.game_management.linear_algebra import PositionMatrix, VelocityMatrix, DifferenceMatrix, DistanceMatrix
import pygame


class Bot(PlayerStarship):
    def __init__(self, x, y, game, **kwargs):
        super().__init__(x, y, **kwargs)
        self.game = game
        self.current_direction = None
        self.move_timer = 0
        self.move_cooldown = 20
        self.position_vector = np.array([[self.rect.centerx, self.rect.top]])
        self.laser_velocity = np.array([-1, self.game.setup['player']['projectile_speed']])
        self.setup = helpers.get_metadata('setup.yaml')
        self.average_delta_time = 1 / self.setup['fps']
        # self.reaction_time = int(0.2 * self.setup['fps'])
        # self.current_score = 0
        self.shots_fired = 0
        self.aliens_hit = 0
        self.target_firing_position = None
        self.nearest_bomb = None
        self.problem_bombs = None
        self.nearest_alien_index = None
        self.nearest_alien = None
        self.previous_frame_alien_count = 0
        self.retarget_cooldown = 0


    def update(self, **kwargs):
        if self.game.aliens:
            # Get position and velocity vectors of all objects
            positions_list = []
            velocity_list = []
            self.target_firing_position = None
            self.nearest_bomb = None
            self.problem_bombs = None
            # self.nearest_alien = None
            self.position_vector = np.array([[self.rect.centerx, self.rect.top]])
            self.move_timer += 1
            self.retarget_cooldown += 1

            for alien in self.game.aliens:
                x = alien.rect.centerx
                y = alien.rect.bottom
                direction = -1 if self.game.alien_speed < 0 else 1
                # speed = alien.speed
                speed = abs(self.game.alien_speed)

                positions_list.append(np.array([x, y]))
                velocity_list.append(np.array([direction, speed]))

            alien_positions_matrix = PositionMatrix(positions_list)
            alien_velocity_matrix = VelocityMatrix(velocity_list)

            positions_list = []
            velocity_list = []
            for bomb in self.game.alien_projectiles_group:
                x = bomb.rect.centerx
                y = bomb.rect.bottom
                speed = self.game.alien_projectiles_group.sprites()[-1].speed
                direction = -1 if speed < 0 else 1

                positions_list.append(np.array([x, y]))
                velocity_list.append(np.array([direction, speed]))

            bomb_positions_matrix = PositionMatrix(positions_list)

            # Find distance to nearest alien
            bot_position_times_aliens = PositionMatrix((self.position_vector.transpose() * np.array([1] * alien_positions_matrix.shape[0])).transpose())
            bot_to_aliens_difference = DifferenceMatrix(alien_positions_matrix, bot_position_times_aliens)
            bot_to_aliens_distance = DistanceMatrix(bot_to_aliens_difference).get_distances()

            if self.nearest_alien is None or (np.argmin(bot_to_aliens_distance) != self.nearest_alien_index and self.retarget_cooldown > 100):
                self.nearest_alien_index = np.argmin(bot_to_aliens_distance)
                self.nearest_alien = self.game.aliens.sprites()[self.nearest_alien_index]
                self.retarget_cooldown = 0

            # elif not self.nearest_alien.alive():
            elif alien_positions_matrix.shape[0] < self.previous_frame_alien_count or not self.nearest_alien.alive():
                self.nearest_alien = None

            if self.nearest_alien is not None:
                nearest_alien_position = alien_positions_matrix[self.nearest_alien_index, :]

            else:
                nearest_alien_position = alien_positions_matrix[0, :]

            # Find distance to all bombs - may not be necessary
            if not bomb_positions_matrix.empty:
                bot_position_times_bombs = PositionMatrix((self.position_vector.transpose() * np.array([1] * bomb_positions_matrix.shape[0])).transpose())
                bot_to_bombs_difference = DifferenceMatrix(bomb_positions_matrix, bot_position_times_bombs)
                bot_to_bombs_distance = DistanceMatrix(bot_to_bombs_difference).get_distances()

            # Calculate laser time to target based on change in y
            y_target = alien_positions_matrix[-1, 1]
            y_distance = self.position_vector[0, 1] - y_target
            time_to_target_y = y_distance / self.laser_velocity[1]

            # Calculate target change in x during that same time
            distance_alien_will_travel_x = time_to_target_y * alien_velocity_matrix[0, 1]

            # New distance formula
            alien_rate = alien_velocity_matrix[-1, 1]# * self.average_delta_time
            bot_rate = self.speed# * self.average_delta_time
            alien_origin = nearest_alien_position[0]
            bot_origin = self.position_vector[0, 0]# + distance_alien_will_travel_x
            relative_rate = bot_rate - alien_rate
            relative_distance = abs(bot_origin - alien_origin)# + distance_alien_will_travel_x# + (alien_rate * self.average_delta_time * time_to_target_y)

            if alien_velocity_matrix[0, 0] > 0:# + distance_alien_will_travel_x:
                if bot_origin > alien_origin + distance_alien_will_travel_x:
                    alien_travel_distance = relative_distance - distance_alien_will_travel_x
                    bot_travel_distance = relative_distance - distance_alien_will_travel_x
                    meeting_point = bot_origin - bot_travel_distance

                elif bot_origin < alien_origin:# - distance_alien_will_travel_x:
                    alien_travel_distance = alien_rate * (relative_distance / relative_rate)
                    bot_travel_distance = alien_travel_distance + relative_distance + distance_alien_will_travel_x
                    meeting_point = bot_origin + bot_travel_distance

                else:
                    alien_travel_distance = distance_alien_will_travel_x
                    bot_travel_distance = distance_alien_will_travel_x
                    meeting_point = alien_origin + alien_travel_distance

                outer_alien_x = alien_positions_matrix[-1, 0]
                outer_alien_distance_from_edge = self.setup['screen_width'] - outer_alien_x# - 30

                if outer_alien_distance_from_edge - 30 <= distance_alien_will_travel_x:
                    self.target_firing_position = meeting_point - outer_alien_distance_from_edge - distance_alien_will_travel_x

            elif alien_velocity_matrix[0, 0] < 0:
                if bot_origin > alien_origin:
                    alien_travel_distance = alien_rate * (relative_distance / relative_rate)
                    bot_travel_distance = alien_travel_distance + relative_distance + distance_alien_will_travel_x
                    meeting_point = bot_origin - bot_travel_distance

                elif bot_origin < alien_origin - distance_alien_will_travel_x:
                    alien_travel_distance = distance_alien_will_travel_x
                    bot_travel_distance = relative_distance - distance_alien_will_travel_x
                    meeting_point = bot_origin + bot_travel_distance

                else:
                    alien_travel_distance = distance_alien_will_travel_x
                    bot_travel_distance = distance_alien_will_travel_x
                    meeting_point = alien_origin - alien_travel_distance

                outer_alien_x = alien_positions_matrix[0, 0]
                # self.gradient_highlight((255, 0, 0), self.game.aliens.sprites()[0])
                outer_alien_distance_from_edge = outer_alien_x - 30
                # print(f'Distance: {outer_alien_distance_from_edge}, will travel: {distance_alien_will_travel_x}, meeting point: {meeting_point}')

                if outer_alien_distance_from_edge <= distance_alien_will_travel_x:
                    # print('Alien is close to the left edge')
                    self.target_firing_position = meeting_point + 30 + (distance_alien_will_travel_x - outer_alien_distance_from_edge)

            else:
                alien_travel_distance = alien_rate * (relative_distance / relative_rate)
                meeting_point = alien_origin + distance_alien_will_travel_x
                bot_travel_distance = 0

            if not self.target_firing_position:
                # Calculate bot's target x position and time, ensuring that bot arrives in time and fires laser
                self.target_firing_position = meeting_point

            # Also ensure that any bomb in the path which would hit the bot is avoided
            if bomb_positions_matrix.shape[0] > 0:
                self.problem_bombs = np.where(bot_to_bombs_distance <= 100)

                if len(self.problem_bombs[0]) > 0:
                    move_right = 0
                    move_left = 0

                    # Track the closest bomb from each direction
                    # closest_left_bomb_distance = float('inf')
                    # closest_right_bomb_distance = float('inf')
                    # closest_vertical_bomb_distance = float('inf')

                    # Loop through all of the problem bombs
                    for i in range(len(self.problem_bombs[0])):
                        bomb_index = self.problem_bombs[0][i]
                        bomb_position = bomb_positions_matrix[bomb_index, :]
                        bomb = self.game.alien_projectiles_group.sprites()[bomb_index]
                        bomb_x = bomb_position[0]
                        # bomb_y = bomb_position[1]

                        # Calculate horizontal and vertical distance
                        # h_distance = abs(bomb_x - self.rect.centerx)
                        # v_distance = self.rect.top - bomb_y

                        # If bomb is directly above/below (Or nearly so)
                        # if h_distance < 20:
                        #     if v_distance < closest_vertical_bomb_distance:
                        #         closest_vertical_bomb_distance = v_distance

                        # If bomb is to the left
                        # elif bomb_x < self.rect.centerx:
                        #     h_distance = self.rect.centerx - bomb_x
                        #     if h_distance < closest_left_bomb_distance:
                        #         closest_left_bomb_distance = h_distance
                        #         move_right += h_distance / 10 # Weight by distance, where closer bombs have higher weight

                        # If bomb is to the right
                        # elif bomb_x > self.rect.centerx:
                        #     h_distance = bomb_x - self.rect.centerx
                        #     if h_distance < closest_right_bomb_distance:
                        #         closest_right_bomb_distance = h_distance
                        #         move_left += h_distance / 10 # Weight by distance, where closer bombs have higher weight

                        # If bomb is to the left and bot can move right
                        if bomb_x + 20 > self.rect.left and bomb_x <= self.rect.centerx + 5 and self.rect.left > 10:
                            move_right += 1

                        # If bomb is to the right and bot can move left
                        elif bomb_x - 20 < self.rect.right and bomb_x >= self.rect.centerx - 5 and self.rect.right < self.setup['screen_width'] - 10:
                            move_left += 1

                    # Determine movement based on weighted scores and screen boundaries
                    # can_move_left = self.rect.left > 10
                    # can_move_right = self.rect.right < self.setup['screen_width'] - 10

                    # # If bombs on both sides, choose the safer direction
                    # if move_right > 0 and move_left > 0:
                    #     # If we can't move in one direction, automatically pick the other
                    #     if not can_move_left:
                    #         move_right = move_left + 1
                    #     elif not can_move_right:
                    #         move_left = move_right + 1
                    #     # If close to screen edge, favor moving away from edge
                    #     elif self.rect.left < 50:
                    #         move_right *= 1.5
                    #     elif self.rect.right > self.setup['screen_width'] - 50:
                    #         move_left *= 1.5

                    # Set nearest bomb for reference (Might be useful elsewhere)
                    nearest_problem_index = np.argmin(bot_to_bombs_distance[self.problem_bombs])
                    nearest_bomb_position = bomb_positions_matrix[self.problem_bombs[0][nearest_problem_index], :]
                    self.nearest_bomb = self.game.alien_projectiles_group.sprites()[self.problem_bombs[0][nearest_problem_index]]

                    # Determine final movement direction based on all problem bombs
                    # if self.move_timer >= self.move_cooldown:
                    if move_right > move_left:# and can_move_right:
                        self.rect.x += self.speed * self.average_delta_time
                        self.current_direction = 'right'
                        self.move_timer = 0

                    elif move_left > move_right:# and can_move_left:
                        self.rect.x -= self.speed * self.average_delta_time
                        self.current_direction = 'left'
                        self.move_timer = 0

                        # elif can_move_right and not can_move_left:
                        #     # If we can only go right, go right
                        #     self.rect.x += self.speed * self.average_delta_time
                        #     self.current_direction = 'right'
                        #     self.move_timer = 0

                        # elif can_move_left and not can_move_right:
                        #     # If we can only go left, go left
                        #     self.rect.x -= self.speed * self.average_delta_time
                        #     self.current_direction = 'left'
                        #     self.move_timer = 0

                    elif move_right > 0:
                        if self.rect.left < (self.setup['screen_width'] - self.rect.right):
                            self.rect.x -= self.speed * self.average_delta_time
                        else:
                            self.rect.x += self.speed * self.average_delta_time

                    # else:
                    #     if self.current_direction == 'right':# and can_move_right:
                    #         self.rect.x += self.speed * self.average_delta_time

                    #     elif self.current_direction == 'left':# and can_move_left:
                    #         self.rect.x -= self.speed * self.average_delta_time

                    # else:
                    #     self.move_and_fire()

                else:
                    self.move_and_fire()

            else:
                self.move_and_fire()

            self.previous_frame_alien_count = alien_positions_matrix.shape[0]

        self.draw_highlights()


    def move_and_fire(self):
        if len(self.projectiles) < 1:
            if self.rect.centerx < self.target_firing_position - 2 and self.rect.right < self.game.setup['screen_width'] + 10:
                self.rect.x += self.speed * self.average_delta_time

            elif self.rect.centerx > self.target_firing_position + 2 and self.rect.left > 10:
                self.rect.x -= self.speed * self.average_delta_time

            else:
                self.fire()
                self.shots_fired += 1


    def handle_event(self, *args, **kwargs):
        # Override parent class function and do nothing
        pass


    def draw_highlights(self):
        # Highlight the nearest alien with a rectangle
        if self.nearest_alien is not None:
            highlight_color = (255, 165, 0)
            self.gradient_highlight(highlight_color, self.nearest_alien)
            
        # Highlight the nearest problem bomb with a rectangle
        # if self.nearest_bomb is not None:
        if self.problem_bombs is not None:
            for i in range(len(self.problem_bombs[0])):
                bomb_index = self.problem_bombs[0][i]
                bomb = self.game.alien_projectiles_group.sprites()[bomb_index]

                highlight_color = (0, 255, 0)
                self.gradient_highlight(highlight_color, bomb)

        # font = pygame.font.Font(self.setup['font_name'], 20)
        # stats_text =[
        #     f'Alien speed: {self.game.alien_speed}',
        #     f'Bot speed: {self.speed}',
            # f'Target alien: {round(self.nearest_alien.rect.centerx)}',
            # f'Target position: {round(self.target_firing_position)}',
            # f'Bot position: {round(self.rect.centerx)}'
        # ]
        # start_y = 300
        # line_spacing = 30

        # for i, line in enumerate(stats_text):
        #     text = font.render(line, True, (255, 255, 255))
        #     text_rect = text.get_rect(center=(100, start_y + i * line_spacing))
        #     self.game.interface.screen.blit(text, text_rect)


    def gradient_highlight(self, highlight_color, object_to_highlight):
        highlight_rect = object_to_highlight.rect.inflate(15, 15)
        
        # Create multiple layers of borders with decreasing opacity for glow effect
        # Outer glow layer (most transparent)
        glow_surf = pygame.Surface((highlight_rect.width + 20, highlight_rect.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(
            glow_surf,
            (*highlight_color, 30),
            pygame.Rect(0, 0, highlight_rect.width + 20, highlight_rect.height + 20),
            width=3,
            border_radius=25
        )
        
        # Middle glow layer
        pygame.draw.rect(
            glow_surf,
            (*highlight_color, 60),
            pygame.Rect(4, 4, highlight_rect.width + 12, highlight_rect.height + 12),
            width=3,
            border_radius=23
        )
        
        # Inner glow layer
        pygame.draw.rect(
            glow_surf,
            (*highlight_color, 90),
            pygame.Rect(8, 8, highlight_rect.width + 4, highlight_rect.height + 4),
            width=2,
            border_radius=21
        )
        
        # Main border (most opaque)
        pygame.draw.rect(
            glow_surf,
            (*highlight_color, 150),
            pygame.Rect(10, 10, highlight_rect.width, highlight_rect.height),
            width=2,
            border_radius=18
        )

        glow_rect = glow_surf.get_rect(center=highlight_rect.center)
        self.game.interface.screen.blit(glow_surf, glow_rect)
