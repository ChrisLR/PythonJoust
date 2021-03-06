import random

import pygame

from pythonjoust.actors import listing
from pythonjoust.actors.base import Rider, RiderState


@listing.register
class Enemy(Rider):
    name = "Enemy"

    def __init__(self, game, x, y):
        sprite_loader = game.sprite_loader
        enemy_images = sprite_loader.get_sliced_sprites(60, 58, "enemies2.png")
        spawn_images = sprite_loader.get_sliced_sprites(60, 60, "spawn1.png")
        unmounted_images = sprite_loader.get_sliced_sprites(60, 60, "unmounted.png")
        super().__init__(game, x, y, enemy_images, spawn_images, unmounted_images)
        self.score_value = 500

    def die(self):
        self.state = RiderState.Unmounted
        # make an egg appear here
        egg = listing.get("Egg")(self.game, self.x, self.y)
        egg.x_speed = self.x_speed
        egg.y_speed = self.y_speed
        self.game.register_sprite(egg)
        self.game.level.eggs.append(egg)
        self.game.level.enemies.remove(self)

    def _update_mounted(self, current_time):
        if self.spawning:
            self.frame_num += 1
            self.image = self.spawn_images[self.frame_num]
            self.next_update_time += 100
            self.rect.topleft = (self.x, self.y)
            if self.frame_num == 5:
                self.spawning = False
            return

        self._handle_platform_collision()
        self._accelerate_or_flap(current_time)
        self._handle_out_of_bounds(current_time)
        self.image = self.images[self.frame_num]
        self._flip_for_direction()

    def _update_unmounted(self, current_time):
        self._handle_platform_collision()
        self._accelerate_or_flap(current_time)
        self._handle_out_of_bounds(current_time, remove=True)
        self.image = self.unmounted_images[self.frame_num]
        self._flip_for_direction()

    def _update_dead(self, current_time):
        self.kill()

    def _accelerate_or_flap(self, current_time):
        # see if we need to accelerate
        if abs(self.x_speed) < self.target_x_speed:
            self.x_speed += self.x_speed / abs(self.x_speed) / 2
        # work out if flapping...
        if self.flap < 1:
            if random.randint(0, 10) > 8 or self.y > 450:  # flap to avoid lava
                self.y_speed -= 3
                self.flap = 3
        else:
            self.flap -= 1

        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed
        if not self.walking:
            self.y_speed += 0.4

        self.rect.topleft = (self.x, self.y)

        if self.walking:
            if self.next_anim_time < current_time:
                if self.x_speed != 0:
                    self.next_anim_time = current_time + 100 / abs(self.x_speed)
                    self.frame_num += 1
                    if self.frame_num > 3:
                        self.frame_num = 0
                    else:
                        self.frame_num = 3
        else:
            if self.flap > 0:
                self.frame_num = 6
            else:
                self.frame_num = 5

    def _flip_for_direction(self):
        if self.x_speed < 0 or (self.x_speed == 0 and self.facing_right is False):
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = False
        else:
            self.facing_right = True

    def respawn(self):
        pass


@listing.register
class Buzzard(Enemy):
    name = "Buzzard"

    def __init__(self, game, x, y, target_object):
        super().__init__(game, x, y)
        self.state = RiderState.Unmounted
        self.target_object = target_object

    def _update_unmounted(self, current_time):
        # TODO Try Direct the buzzard towards the egg
        self._handle_platform_collision()
        self._accelerate_or_flap(current_time)
        self._handle_egg_collisions()
        self._handle_out_of_bounds(current_time, self.target_object.broken)
        self.image = self.unmounted_images[self.frame_num]
        self._flip_for_direction()

    def _handle_egg_collisions(self):
        # check for enemy collision
        colliding_eggs = pygame.sprite.spritecollide(
            self, self.game.level.eggs, False,
            collided=pygame.sprite.collide_mask
        )
        for egg in colliding_eggs:
            if egg.hatched:
                egg.die()
                self.die()
                new_enemy = Enemy(self.game, self.x, self.y)
                self.game.level.enemies.append(new_enemy)
                self.game.register_sprite(new_enemy)
                break

    def _accelerate_or_flap(self, current_time):
        # see if we need to accelerate
        if abs(self.x_speed) < self.target_x_speed:
            self.x_speed += self.x_speed / abs(self.x_speed) / 2
        # work out if flapping...
        if self.flap < 1:
            if self.y > self.target_object.y:  # flap to get to level with the target
                self.y_speed -= 3
                self.flap = 3
        else:
            self.flap -= 1

        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed
        if not self.walking:
            self.y_speed += 0.4

        self.rect.topleft = (self.x, self.y)

        if self.walking:
            if self.next_anim_time < current_time:
                if self.x_speed != 0:
                    self.next_anim_time = current_time + 100 / abs(self.x_speed)
                    self.frame_num += 1
                    if self.frame_num > 3:
                        self.frame_num = 0
                    else:
                        self.frame_num = 3
        else:
            if self.flap > 0:
                self.frame_num = 6
            else:
                self.frame_num = 5

    def die(self):
        self.game.level.enemies.remove(self)
        self.kill()
