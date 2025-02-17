from space_marauders.player.player_starship import PlayerStarship


class Bot(PlayerStarship):
    def __init__(self, x, y, game, **kwargs):
        super().__init__(x, y, **kwargs)
        self.game = game
        self.current_direction = None
        self.move_timer = 0
        self.move_cooldown = 60
        # self.reaction_time = int(0.2 * self.setup['fps'])


    def update(self):
        if self.game.alien_projectiles_group and self.move_timer == 0:
            closest_bomb = min(
                self.game.alien_projectiles_group,
                key=lambda bomb: abs(bomb.rect.centerx - self.rect.centerx),
                default=None
            )
            if closest_bomb:
                self.move_timer = 0 # Not sure about this one
                self.avoid_projectile(closest_bomb)

        elif self.move_timer > 0:
            self.move_timer -= 1
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


    def avoid_projectile(self, bomb):
        screen_width = self.setup['screen_width']
        buffer = 30

        if self.current_direction:
            if self.current_direction == 'left' and self.rect.left <= buffer:
                self.current_direction = 'right'
            elif self.current_direction == 'right' and self.rect.right >= screen_width - buffer:
                self.current_direction = 'left'

        if bomb.rect.left - 15 < self.rect.right and bomb.rect.centerx > self.rect.centerx:
            if self.current_direction != 'left' and self.rect.left > buffer:
                self.current_direction = 'left'
                self.move_timer = self.move_cooldown

        elif bomb.rect.right + 15 > self.rect.left and bomb.rect.centerx < self.rect.centerx:
            if self.current_direction != 'right' and self.rect.right < screen_width - buffer:
                self.current_direction = 'right'
                self.move_timer = self.move_cooldown

        if self.current_direction == 'left':
            self.move_left()

        elif self.current_direction == 'right':
            self.move_right()


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
