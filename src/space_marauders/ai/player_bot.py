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
        self.position_vector = np.array([[self.rect.centerx, self.rect.top]])

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
        # bomb_velocity_matrix = VelocityMatrix(velocity_list)

        # Find distance to nearest alien
        bot_position_times_aliens = PositionMatrix((self.position_vector.transpose() * np.array([1] * alien_positions_matrix.shape[0])).transpose())
        bot_to_aliens_difference = DifferenceMatrix(alien_positions_matrix, bot_position_times_aliens)
        bot_to_aliens_distance = DistanceMatrix(bot_to_aliens_difference).get_distances()
        nearest_alien_index = np.argmin(bot_to_aliens_distance)
        nearest_alien_position = alien_positions_matrix[nearest_alien_index, :]
        print('--' * 100)
        print('Bot position:', bot_position_times_aliens)
        print('Alien positions:', alien_positions_matrix)
        print('Bot difference from aliens:', bot_to_aliens_difference)
        print('Bot distance to aliens:', bot_to_aliens_distance)
        print('Nearest alien index:', nearest_alien_index)
        print('Nearest alien position:', alien_positions_matrix[nearest_alien_index, :])

        # Find distance to all bombs - may not be necessary
        if not bomb_positions_matrix.empty:
            bot_position_times_bombs = PositionMatrix((self.position_vector.transpose() * np.array([1] * bomb_positions_matrix.shape[0])).transpose())
            bot_to_bombs_difference = DifferenceMatrix(bomb_positions_matrix, bot_position_times_bombs)
            bot_to_bombs_distance = DistanceMatrix(bot_to_bombs_difference).get_distances()

        # Calculate laser time to target based on change in y
        y_target = alien_positions_matrix[-1, 1]
        y_distance = self.position_vector[0, 1] - y_target
        time_to_target_y = y_distance / self.laser_velocity[1]
        print('Y target:', y_target)
        print('Y distance:', y_distance)
        print('Y time to target:', time_to_target_y)

        # Calculate target change in x during that same time
        distance_alien_will_travel_x = time_to_target_y * alien_velocity_matrix[-1, 1]

        # New distance formula
        alien_rate = alien_velocity_matrix[-1, 1]
        bot_rate = self.speed * self.average_delta_time
        alien_origin = nearest_alien_position[0]
        bot_origin = self.position_vector[0, 0]
        distance = alien_rate * ((abs(bot_origin - alien_origin) + abs(distance_alien_will_travel_x)) / abs(alien_rate - bot_rate))
        print('Alien rate:', alien_rate)
        print('Bot rate:', bot_rate)
        print('Alien origin:', alien_origin)
        print('Bot origin:', bot_origin)
        print('Distance:', distance)

        # Determine current direction of aliens, and get the x position of the outer-most alien
        print('Alien velocity:', alien_velocity_matrix[0, :])
        if alien_velocity_matrix[0, 0] < 0:
            # Relevant outer-most alien is on the left-hand side, or the first position in the matrix
            outer_alien_x = alien_positions_matrix[0, 0]

            # Determine if the aliens are going to change directions before the bot could arrive at the target firing position
            # if outer_alien_x <= distance_alien_will_travel_x:
            if outer_alien_x <= distance:
                # Aliens are moving to the left, but will switch and come back to the right
                # distance_alien_will_travel_x = distance_alien_will_travel_x - (self.setup['screen_width'] - outer_alien_x)
                distance = distance - (self.setup['screen_width'] - outer_alien_x)
                # target_firing_position = nearest_alien_position[0] + (distance_alien_will_travel_x * alien_velocity_matrix[-1, 0] * -1) + ((self.setup['alien']['size'] // 2) * alien_velocity_matrix[-1, 0])
                target_firing_position = nearest_alien_position[0] + (distance * alien_velocity_matrix[-1, 0] * -1)# + ((self.setup['alien']['size'] // 2) * alien_velocity_matrix[-1, 0])

        elif alien_velocity_matrix[0, 0] > 0:
            # Relevant outer-most alien is on the right-hand side, or the last position in the matrix
            outer_alien_x = alien_positions_matrix[-1, 0]

            # Determine if the aliens are going to change directions before the bot could arrive at the target firing position
            # if (self.setup['screen_width'] - outer_alien_x) <= distance_alien_will_travel_x:
            if (self.setup['screen_width'] - outer_alien_x) <= distance:
                # distance_alien_will_travel_x = distance_alien_will_travel_x - (self.setup['screen_width'] - outer_alien_x)
                distance = distance - (self.setup['screen_width'] - outer_alien_x)
                # target_firing_position = nearest_alien_position[0] + (distance_alien_will_travel_x * alien_velocity_matrix[-1, 0] * -1) + ((self.setup['alien']['size'] // 2) * alien_velocity_matrix[-1, 0] * -1)
                target_firing_position = nearest_alien_position[0] + (distance * alien_velocity_matrix[-1, 0])# + ((self.setup['alien']['size'] // 2) * alien_velocity_matrix[-1, 0])

        if not target_firing_position:
            # Calculate bot's target x position and time, ensuring that bot arrives in time and fires laser
            # target_firing_position = nearest_alien_position[0] + (distance_alien_will_travel_x * alien_velocity_matrix[-1, 0]) + ((self.setup['alien']['size'] // 2) * alien_velocity_matrix[-1, 0])
            target_firing_position = bot_origin + (distance * alien_velocity_matrix[-1, 0])# + ((self.setup['alien']['size'] // 2) * alien_velocity_matrix[-1, 0])

        print('Alien travel distance:', distance_alien_will_travel_x)
        print('Target firing position:', target_firing_position)

        # Also ensure that any bomb in the path which would hit the bot is avoided
        if bomb_positions_matrix.shape[0] > 0:
            problem_bombs = np.where(bot_to_bombs_distance <= 100)
            print('Bomb distances:', bot_to_bombs_distance)
            print('Problem bombs:', bot_to_bombs_distance[problem_bombs], 'at indices', problem_bombs[0])

            if len(problem_bombs[0]) > 0:
                nearest_problem_index = np.argmin(bot_to_bombs_distance[problem_bombs])
                nearest_bomb_position = bomb_positions_matrix[problem_bombs[0][nearest_problem_index], :]
                bomb_x = nearest_bomb_position[0]

                if bomb_x + 15 > self.rect.left and bomb_x <= self.rect.centerx - 5:
                    self.rect.x += self.speed * self.average_delta_time

                elif bomb_x - 15 < self.rect.right and bomb_x >= self.rect.centerx + 5:
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
