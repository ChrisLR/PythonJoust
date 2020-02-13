from pythonjoust.actors import listing
from pythonjoust.actors.base import Actor


@listing.register
class Egg(Actor):
    name = "Egg"

    def __init__(self, game, x, y):
        egg_images = game.sprite_loader.get_sliced_sprites(40, 33, "egg.png")
        super().__init__(game, x, y, egg_images, None, None)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.next_update_time = 0
        self.lifetime = 0

    def move(self):
        # gravity
        if not self.walking:
            self.y_speed += 0.4
            if self.y_speed > 10:
                self.y_speed = 10
            self.y += self.y_speed

        self.x += self.x_speed
        if self.x_speed and self.walking:
            # Slow down gradually
            self.x_speed += -0.01 if self.x_speed > 0 else 0.01
            if abs(self.x_speed) < 0.01:
                self.x_speed = 0

        if self.y > 570:  # hit lava
            self.die()

    def update(self, current_time):
        # Update every 30 milliseconds
        if self.next_update_time < current_time:
            self.next_update_time = current_time + 30
            self.move()
            self.rect.topleft = (self.x, self.y)
            self._handle_platform_collision()
            self.lifetime += 1

            if self.lifetime >= 60000:
                self.hatch()

            # wrap round screens
            if self.x < -48:
                self.x = 900
            elif self.x > 900:
                self.x = 0

    def die(self):
        self.game.level.eggs.remove(self)
        self.kill()

    def respawn(self):
        pass

    def hatch(self):
        pass
