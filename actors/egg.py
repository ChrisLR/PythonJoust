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
        self.y_speed += 0.4
        if self.y_speed > 10:
            self.y_speed = 10
        self.y += self.y_speed
        self.x += self.x_speed
        if self.y > 570:  # hit lava
            self.kill()

    def update(self, current_time):
        # Update every 30 milliseconds
        if self.next_update_time < current_time:
            self.next_update_time = current_time + 30
            self.move()
            self.rect.topleft = (self.x, self.y)
            self._handle_platform_collision()
            # wrap round screens
            if self.x < -48:
                self.x = 900
            if self.x > 900:
                self.x = -48
