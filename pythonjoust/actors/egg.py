import random

from pythonjoust.actors import listing
from pythonjoust.actors.base import Actor


@listing.register
class Egg(Actor):
    name = "Egg"

    def __init__(self, game, x, y):
        egg_images = game.sprite_loader.get_sliced_sprites(40, 33, "egg.png")
        super().__init__(game, x, y, egg_images, None, None)
        self.image = self.images[0]
        self.image_index = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.next_update_time = 0
        self.lifetime = 0
        self._is_hatching = False
        self._hatch_cumulated_time = 0
        self.hatched = False
        self.broken = False

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
            self.x_speed += -0.1 if self.x_speed > 0 else 0.1
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

            if self.lifetime >= 1000 and not self.hatched:
                self._is_hatching = True

            if self._is_hatching:
                self.hatch()

            # wrap round screens
            if self.x < -48:
                self.x = 900
            elif self.x > 900:
                self.x = 0

    def die(self):
        self.game.level.eggs.remove(self)
        self.kill()
        self.broken = True

    def respawn(self):
        pass

    def hatch(self):
        self._hatch_cumulated_time += 1
        if self._hatch_cumulated_time >= 5:
            image_length = len(self.images)
            if self.image_index < image_length - 1:
                self.image_index += 1
                self.image = self.images[self.image_index]
                self._hatch_cumulated_time = 0
            elif self.image_index == image_length - 1:
                self.hatched = True
                self._is_hatching = False
                # TODO Spawn the buzzard off screen
                x_choices = [0, 900]
                buzzard = listing.get("Buzzard")(self.game, x=random.choice(x_choices), y=self.y, target_object=self)
                self.game.level.enemies.append(buzzard)
                self.game.register_sprite(buzzard)
