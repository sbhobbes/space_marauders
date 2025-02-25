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
        self.move_cooldown = 60
        self.position_vector = np.array([[self.rect.centerx, self.rect.top]])
        self.laser_velocity = np.array([-1, self.game.setup['player']['projectile_speed']])
        self.setup = helpers.get_metadata('setup.yaml')
        self.average_delta_time = 1 / self.setup['fps']
        # self.reaction_time = int(0.2 * self.setup['fps'])


    def update(self, **kwargs):
        # Get position and velocity vectors of all objects
        positions_list = []
        velocity_list = []
        target_firing_position = None

        for alien in self.game.aliens:
            x = alien.rect.centerx
            y = alien.rect.bottom
            direction = -1 if self.game.alien_speed < 0 else 1
            speed = alien.speed

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
        bomb_velocity_matrix = VelocityMatrix(velocity_list)

        # Find distance to nearest alien
        bot_position_times_aliens = PositionMatrix((self.position_vector.transpose() * np.array([1] * alien_positions_matrix.shape[0])).transpose())
        bot_to_aliens_difference = DifferenceMatrix(alien_positions_matrix, bot_position_times_aliens)
        bot_to_aliens_distance = DistanceMatrix(bot_to_aliens_difference).get_distances()
        nearest_alien_index = np.argmin(bot_to_aliens_distance)
        nearest_alien_position = alien_positions_matrix[nearest_alien_index, :]

        # Find distance to all bombs - may not be necessary
        # if not bomb_positions_matrix.empty:
        #     bot_position_times_bombs = PositionMatrix((self.position_vector.transpose() * np.array([1] * bomb_positions_matrix.shape[0])).transpose())
        #     bot_to_bombs_difference = DifferenceMatrix(bomb_positions_matrix, bot_position_times_bombs)
        #     bot_to_bombs_distance = DistanceMatrix(bot_to_bombs_difference).get_distances()

        # Calculate laser time to target based on change in y
        y_target = alien_positions_matrix[-1, 1]
        y_distance = self.position_vector[0, 1] - y_target
        time_to_target_y = y_distance / self.laser_velocity[1]

        # Calculate target change in x during that same time
        distance_alien_will_travel_x = time_to_target_y * alien_velocity_matrix[-1, 1]

        # Determine current direction of aliens, and get the x position of the outer-most alien
        if alien_velocity_matrix[0, 0] < 0:
            # Relevant outer-most alien is on the left-hand side, or the first position in the matrix
            outer_alien_x = alien_positions_matrix[0, 0]

            # Determine if the aliens are going to change directions before the bot could arrive at the target firing position
            if outer_alien_x <= distance_alien_will_travel_x:
                # Aliens are moving to the left, but will switch and come back to the right
                distance_alien_will_travel_x = distance_alien_will_travel_x - (self.setup['screen_width'] - outer_alien_x)
                target_firing_position = nearest_alien_position[0] + (distance_alien_will_travel_x * alien_velocity_matrix[-1, 0] * -1)

        elif alien_velocity_matrix[0, 0] > 0:
            # Relevant outer-most alien is on the right-hand side, or the last position in the matrix
            outer_alien_x = alien_positions_matrix[-1, 0]

            # Determine if the aliens are going to change directions before the bot could arrive at the target firing position
            if (self.setup['screen_width'] - outer_alien_x) <= distance_alien_will_travel_x:
                # Aliens are moving to the right, but will switch and come back to the left
                # print('Next')
                # print('total travel distance', distance_alien_will_travel_x)
                distance_alien_will_travel_x = distance_alien_will_travel_x - (self.setup['screen_width'] - outer_alien_x)
                target_firing_position = nearest_alien_position[0] + (distance_alien_will_travel_x * alien_velocity_matrix[-1, 0] * -1)
                # print('distance to edge of screen', self.setup['screen_width'] - outer_alien_x + (self.setup['alien']['size'] // 2))
                # print('remaining travel distance', distance_alien_will_travel_x)
                # print('distance from target to alien', (distance_alien_will_travel_x * alien_velocity_matrix[-1, 0] * -1))
                # print('nearest alien position', nearest_alien_position[0])
                # print('firing position', target_firing_position)
                

        if not target_firing_position:
            # Calculate bot's target x position and time, ensuring that bot arrives in time and fires laser
            target_firing_position = nearest_alien_position[0] + (distance_alien_will_travel_x * alien_velocity_matrix[-1, 0])

        # Also ensure that any bomb in the path which would hit the bot is avoided
        if bomb_positions_matrix.shape[0] > 0:
            bomb_distance_to_target_matrix = self.rect.centery - bomb_positions_matrix[:, 1]
            bomb_time_to_target_matrix = bomb_distance_to_target_matrix / bomb_velocity_matrix[-1, 1]
            # print(bomb_positions_matrix[:, 0])
            bot_distance_from_bombs_matrix = self.rect.centerx - bomb_positions_matrix[:, 1]
            bot_time_to_bombs_matrix = bot_distance_from_bombs_matrix / self.speed
            problem_bombs = np.where(bomb_time_to_target_matrix - 1 <= bot_time_to_bombs_matrix)
            problem_bomb_positions = bomb_positions_matrix[problem_bombs]

            if len(problem_bomb_positions) > 1:
                for bomb_x, _ in problem_bomb_positions:
                    if bomb_x + 15 > self.rect.left and bomb_x + 15 <= self.rect.centerx + 5:
                        self.rect.x += self.speed * self.average_delta_time

                    elif bomb_x - 15 < self.rect.right and bomb_x >= self.rect.centerx - 5:
                        self.rect.x -= self.speed * self.average_delta_time

                    else:
                        self.move_and_fire(target_firing_position)

            else:
                self.move_and_fire(target_firing_position)

        else:
            self.move_and_fire(target_firing_position)


    def move_and_fire(self, target_firing_position):
        if self.rect.centerx < target_firing_position - 5:
            self.rect.x += self.speed * self.average_delta_time

        elif self.rect.centerx > target_firing_position + 5:
            self.rect.x -= self.speed * self.average_delta_time

        elif len(self.projectiles) < 1:
            self.fire()


    def move_left(self):
        self.rect.x -= self.speed


    def move_right(self):
        self.rect.x += self.speed


    def handle_event(self, *args, **kwargs):
        # Override parent class function and do nothing
        pass
