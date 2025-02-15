import pygame
import space_marauders


class Starship(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, speed, faction):
        super().__init__()
        self.image = space_marauders.utils.helpers.load_asset(image_path, base_path='ships')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.faction = faction
        self.projectiles = pygame.sprite.Group()


    def update(self):
        self.projectiles.update()


    def fire(self, projectile_image_path, projectile_speed):
        if len(self.projectiles) == 0:
            projectile = Projectile(
                self.rect.centerx,
                self.rect.top,
                projectile_image_path,
                projectile_speed,
                self.faction
            )
            self.projectiles.add(projectile)


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.projectiles.draw(screen)


class PlayerStarship(Starship):
    def __init__(self, x, y, image_path, speed, faction):
        super().__init__(x, y, image_path, speed, faction)


    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE]:
            self.fire('laser_03.png', 10)


class AlienStarship(Starship):
    def __init__(self, x, y, image_path, speed, faction):
        super().__init__(x, y, image_path, speed, faction)
        self.fire_timer = pygame.time.get_ticks()


    def update(self):
        super().update()
        # self.rect.y += self.speed
        # if self.rect.y > 600:
        #     self.rect.y = 0

        current_time = pygame.time.get_ticks()
        if current_time - self.fire_timer > 2000:
            self.fire('machine_gun_03.png', 5)
            self.fire_timer = current_time


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, speed, faction):
        super().__init__()
        self.image = space_marauders.utils.helpers.load_asset(image_path, base_path='projectiles')
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.faction = faction


    def update(self):
        if self.faction == 'player':
            self.rect.y -= self.speed

        else:
            self.rect.y += self.speed

        if self.rect.y < 0 or self.rect.y > 600:
            self.kill()


    def draw(self, screen):
        screen.blit(self.image, self.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 900))
    clock = pygame.time.Clock()

    player = PlayerStarship(400, 550, 'sky_blanc_2.png', 5, 'player')
    all_sprites = pygame.sprite.Group(player)

    aliens = pygame.sprite.Group()
    for i in range(10):
        alien = AlienStarship(100 + i * 100, 50, 'moroder_2.png', 2, 'aliens')
        aliens.add(alien)
        all_sprites.add(alien)

    alien_speed = 2
    alien_drop_amount = 20

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        screen.fill((0, 0, 0))

        all_sprites.update()

        # group_rect = aliens.sprites()[0].rect.copy()
        for alien in aliens:
            alien.rect.x += alien_speed

        group_rect = aliens.sprites()[0].rect.copy()
        for alien in aliens:
            group_rect.union_ip(alien.rect)

        if group_rect.left < 0 or group_rect.right > 1200:
            alien_speed *= -1
            for alien in aliens:
                alien.rect.y += alien_drop_amount

        for sprite in all_sprites:
            if isinstance(sprite, Starship):
                sprite.projectiles.draw(screen)

        all_sprites.draw(screen)

        for alien in aliens:
            collisions = pygame.sprite.spritecollide(player, alien.projectiles, True)
            if collisions:
                print('Player hit!')
                # Handle player hit

        for projectile in player.projectiles:
            collisions = pygame.sprite.spritecollide(projectile, aliens, True)
            if collisions:
                print('Alien hit!')
                projectile.kill()
                # Handle alien hit

            for alien in aliens:
                alien_projectile_collisions = pygame.sprite.spritecollide(projectile, alien.projectiles, True)
                if alien_projectile_collisions:
                    print('Projectiles collided!')
                    projectile.kill()
                    # No need to remove alien projectile, because spritecollide already removed it.

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
