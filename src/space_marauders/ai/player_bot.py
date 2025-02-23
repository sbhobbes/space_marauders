import numpy as np
from space_marauders.player.player_starship import PlayerStarship
from space_marauders.game_management.linear_algebra import PositionMatrix, VelocityMatrix, DifferenceMatrix, DistanceMatrix


class Bot(PlayerStarship):
    def __init__(self, x, y, game, **kwargs):
        super().__init__(x, y, **kwargs)
        self.game = game
        self.current_direction = None
        self.move_timer = 0
        self.move_cooldown = 60
        self.position_vector = np.array([[self.rect.centerx, self.rect.top]])
        self.laser_velocity = np.array([-1, self.game.setup['player']['projectile_speed']])
        # self.reaction_time = int(0.2 * self.setup['fps'])


    def update(self):
        # Get position and velocity vectors of all objects
        positions_list = []
        velocity_list = []
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
        for bomb in self.game.alien_projectiles_group:
            x = bomb.rect.centerx
            y = bomb.rect.bottom

            positions_list.append(np.array([x, y]))

        bomb_positions_matrix = PositionMatrix(positions_list)

        # Find distance to nearest alien
        bot_position_times_aliens = PositionMatrix((self.position_vector.transpose() * np.array([1] * alien_positions_matrix.shape[0])).transpose())
        bot_to_aliens_difference = DifferenceMatrix(alien_positions_matrix, bot_position_times_aliens)
        bot_to_aliens_distance = DistanceMatrix(bot_to_aliens_difference).get_distances()
        nearest_alien_index = np.argmin(bot_to_aliens_distance)
        nearest_alien_position = alien_positions_matrix[nearest_alien_index, :]

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
        distance_alien_will_travel_x = time_to_target_y * alien_velocity_matrix[-1, 1]
        print(distance_alien_will_travel_x)
        
        # Calculate bot's target x position and time, ensuring that bot arrives in time and fires laser
        # Also ensure that any bomb in the path which would hit the bot is avoided
        pass


        # if self.game.alien_projectiles_group and self.move_timer == 0:
        #     closest_bomb = min(
        #         self.game.alien_projectiles_group,
        #         key=lambda bomb: abs(bomb.rect.centerx - self.rect.centerx),
        #         default=None
        #     )
        #     if closest_bomb:
        #         self.move_timer = 0 # Not sure about this one
        #         self.avoid_projectile(closest_bomb)

        # elif self.move_timer > 0:
        #     self.move_timer -= 1
        # if self.game.alien_projectiles_group:
        #     for bomb in self.game.alien_projectiles_group:
        #         if (
        #             bomb.rect.left - 20 <= self.rect.right and
        #             bomb.rect.left + 20 >= self.rect.left and
        #             bomb.rect.left > self.rect.centerx and
        #             self.rect.left > 0
        #         ):
        #             self.move_left()

        #         elif (
        #             bomb.rect.right + 20 >= self.rect.left and
        #             bomb.rect.right - 20 <= self.rect.right and
        #             bomb.rect.right < self.rect.centerx and
        #             self.rect.right < self.setup['screen_width']
        #         ):
        #             self.move_right()


    # def avoid_projectile(self, bomb):
    #     screen_width = self.setup['screen_width']
    #     buffer = 30

    #     if self.current_direction:
    #         if self.current_direction == 'left' and self.rect.left <= buffer:
    #             self.current_direction = 'right'
    #         elif self.current_direction == 'right' and self.rect.right >= screen_width - buffer:
    #             self.current_direction = 'left'

    #     if bomb.rect.left - 15 < self.rect.right and bomb.rect.centerx > self.rect.centerx:
    #         if self.current_direction != 'left' and self.rect.left > buffer:
    #             self.current_direction = 'left'
    #             self.move_timer = self.move_cooldown

    #     elif bomb.rect.right + 15 > self.rect.left and bomb.rect.centerx < self.rect.centerx:
    #         if self.current_direction != 'right' and self.rect.right < screen_width - buffer:
    #             self.current_direction = 'right'
    #             self.move_timer = self.move_cooldown

    #     if self.current_direction == 'left':
    #         self.move_left()

    #     elif self.current_direction == 'right':
    #         self.move_right()


    # def update(self):
    #     if not self.game.alien_projectiles_group:
    #         return

    #     if self.move_timer > 0:
    #         self.move_timer -= 1
    #     else:
    #         self.decide_movement()
    #         self.move_timer = self.reaction_time  # Reset cooldown

    #     # Keep moving in the chosen direction every frame
    #     if self.current_direction == "left":
    #         self.move_left()
    #     elif self.current_direction == "right":
    #         self.move_right()

    # def decide_movement(self):
    #     screen_width = self.game.setup['screen_width']
    #     buffer = 30  

    #     # Find the closest bomb
    #     closest_bomb = min(
    #         self.game.alien_projectiles_group,
    #         key=lambda bomb: abs(bomb.rect.centerx - self.rect.centerx),
    #         default=None
    #     )

    #     if closest_bomb:
    #         # Move left if the bomb is coming from the right
    #         if closest_bomb.rect.left < self.rect.right and closest_bomb.rect.centerx > self.rect.centerx:
    #             if self.rect.left > buffer:
    #                 self.current_direction = "left"

    #         # Move right if the bomb is coming from the left
    #         elif closest_bomb.rect.right > self.rect.left and closest_bomb.rect.centerx < self.rect.centerx:
    #             if self.rect.right < screen_width - buffer:
    #                 self.current_direction = "right"


    def move_left(self):
        self.rect.x -= self.speed


    def move_right(self):
        self.rect.x += self.speed


    def handle_event(self, *args, **kwargs):
        # Override parent class function and do nothing
        pass
