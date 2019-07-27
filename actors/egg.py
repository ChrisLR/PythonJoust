import pygame

from actors import listing
from actors.base import Actor


@listing.register
class Egg(Actor):
    name = "Egg"

    def __init__(self, game, x, y):
        egg_images = game.spriteloader.get_sliced_sprites(40, 33, "egg.png")
        super().__init__(game, x, y, egg_images, None, None)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.next_update_time = 0

    def move(self):
        # gravity
        self.yspeed += 0.4
        if self.y_speed > 10:
            self.y_speed = 10
        self.y += self.y_speed
        self.x += self.x_speed
        if self.y > 570:  # hit lava
            self.kill()

    def update(self, current_time, platforms):
        # Update every 30 milliseconds
        if self.next_update_time < current_time:
            self.next_update_time = current_time + 30
            self.move()
            self.rect.topleft = (self.x, self.y)
            collidedPlatforms = pygame.sprite.spritecollide(self, platforms, False, collided=pygame.sprite.collide_mask)
            if (((self.y > 40 and self.y < 45) or (self.y > 250 and self.y < 255)) and (
                    self.x < 0 or self.x > 860)):  # catch when it is rolling between screens
                self.yspeed = 0
            else:
                collided = False
                for collidedPlatform in collidedPlatforms:
                    collided = self.bounce(collidedPlatform)
            # wrap round screens
            if self.x < -48:
                self.x = 900
            if self.x > 900:
                self.x = -48
