import random

import pygame

from actors import listing
from actors.base import Rider


@listing.register
class Enemy(Rider):
    name = "Enemy"

    def __init__(self, game, x, y):
        sprite_loader = game.sprite_loader
        enemy_images = sprite_loader.get_sliced_sprites(60, 58, "enemies2.png")
        spawn_images = sprite_loader.get_sliced_sprites(60, 60, "spawn1.png")
        unmounted_images = sprite_loader.get_sliced_sprites(60, 60, "unmounted.png")
        super().__init__(game, x, y, enemy_images, spawn_images, unmounted_images)

    def die(self):
        # make an egg appear here
        egg = listing.get("Egg")(self.game, self.x, self.y)
        egg.x_speed = self.x_speed
        egg.y_speed = self.y_speed
        self.game.register_sprite(egg)
        self.alive = False

    def update(self, current_time):
        if self.next_update_time < current_time:  # only update every 30 millis
            self.next_update_time = current_time + 50
            if self.spawning:
                self.frameNum += 1
                self.image = self.spawnimages[self.frameNum]
                self.next_update_time += 100
                self.rect.topleft = (self.x, self.y)
                if self.frameNum == 5:
                    self.spawning = False
            else:
                # see if we need to accelerate
                if abs(self.x_speed) < self.targetXSpeed:
                    self.x_speed += self.x_speed / abs(self.x_speed) / 2
                # work out if flapping...
                if self.flap < 1:
                    if (random.randint(0, 10) > 8 or self.y > 450):  # flap to avoid lava
                        self.y_speed -= 3
                        self.flap = 3
                else:
                    self.flap -= 1

                self.x = self.x + self.x_speed
                self.y = self.y + self.y_speed
                if not self.walking:
                    self.y_speed += 0.4
                if self.y_speed > 10:
                    self.y_speed = 10
                if self.y_speed < -10:
                    self.y_speed = -10
                if self.y < 0:  # can't go off the top
                    self.y = 0
                    self.y_speed = 2
                if self.y > 570:  # hit lava
                    self.kill()

                if self.x < -48:  # off the left. If enemy is dead then remove entirely
                    if self.alive:
                        self.x = 900
                    else:
                        self.kill()
                if self.x > 900:  # off the right. If enemy is dead then remove entirely
                    if self.alive:
                        self.x = -48
                    else:
                        self.kill()
                self.rect.topleft = (self.x, self.y)
                self._handle_platform_collision()

                self.rect.topleft = (self.x, self.y)
                if self.walking:
                    if self.next_anim_time < current_time:
                        if self.x_speed != 0:
                            self.next_anim_time = current_time + 100 / abs(self.x_speed)
                            self.frameNum += 1
                            if self.frameNum > 3:
                                self.frameNum = 0
                            else:
                                self.frameNum = 3
                else:
                    if self.flap > 0:
                        self.frameNum = 6
                    else:
                        self.frameNum = 5
                if self.alive:
                    self.image = self.images[((self.enemyType * 7) + self.frameNum)]
                else:
                    # show the unmounted sprite
                    self.image = self.unmountedimages[self.frameNum]
                if self.x_speed < 0 or (self.x_speed == 0 and self.facingRight == False):
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.facingRight = False
                else:
                    self.facingRight = True
