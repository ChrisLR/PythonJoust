import abc
import random
from enum import IntEnum

import pygame


class Actor(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    name = ""
    render_priority = 5

    def __init__(self, game, x, y, images, spawn_images, unmounted_images):
        super().__init__()
        self.state = RiderState.Mounted
        self.facing_right = True
        self.flap = 0
        self.flap_count = 0
        self.game = game
        self.images = images
        self.spawn_images = spawn_images
        self.unmounted_images = unmounted_images
        self.frame_num = 0
        self.image = self.spawn_images[0] if spawn_images else images[0]
        self.rect = self.image.get_rect()
        self.next_update_time = 0
        self.next_anim_time = 0
        self.starting_x = x
        self.starting_y = y
        self.target_x_speed = 10
        self.x = x
        self.y = y
        self.x_speed = random.randint(3, 10)
        self.y_speed = 0
        self.spawning = True
        self.walking = True

    def bounce(self, colliding_object):
        collided = False
        if self.y < (colliding_object.y - 20) and ((self.x > (colliding_object.x - 40) and self.x < (colliding_object.rect.right - 10))):
            # coming in from the top?
            self.walking = True
            self.y_speed = 0
            self.y = colliding_object.y - self.rect.height + 3
        elif self.x < colliding_object.x:
            # colliding from left side
            collided = True
            self.x = self.x - 10
            self.x_speed = -2
        elif self.x > colliding_object.rect.right - 50:
            # colliding from right side
            collided = True
            self.x = self.x + 10
            self.x_speed = 2
        elif self.y > colliding_object.y:
            # colliding from bottom
            collided = True
            self.y = self.y + 10
            self.y_speed = 0

        return collided

    @abc.abstractmethod
    def die(self):
        pass

    @abc.abstractmethod
    def respawn(self):
        pass

    @abc.abstractmethod
    def update(self, current_time):
        pass

    def _handle_platform_collision(self):
        level = self.game.level
        collidable_terrain = []
        collidable_terrain.extend(level.platforms)
        collidable_terrain.extend(level.bridges)
        collided_platforms = pygame.sprite.spritecollide(
            self, collidable_terrain, False,
            collided=pygame.sprite.collide_mask
        )
        collided = False

        if (((40 < self.y < 45) or (250 < self.y < 255)) and (
                self.x < 0 or self.x > 860)):  # catch when it is rolling between screens
            self.y_speed = 0
            self.walking = True
        else:
            self.walking = False
            for collided_platform in collided_platforms:
                collided = self.bounce(collided_platform)

        return collided


class Rider(Actor, metaclass=abc.ABCMeta):
    update_cycle_time = 50

    def update(self, current_time):
        if self.next_update_time < current_time:
            self.next_update_time = current_time + self.update_cycle_time
            if self.state == 2:
                self._update_mounted(current_time)
            elif self.state == 1:
                self._update_unmounted(current_time)
            else:
                self._update_dead(current_time)

    @abc.abstractmethod
    def _update_mounted(self, current_time):
        pass

    @abc.abstractmethod
    def _update_unmounted(self, current_time):
        pass

    @abc.abstractmethod
    def _update_dead(self, current_time):
        pass

    def _handle_out_of_bounds(self, current_time, remove=False):
        if self.y < 0:
            self.y = 0
            self.y_speed = 2
        if self.y > 570:
            self.die()
            self.state = RiderState.Dead
            self.next_update_time = current_time + 2000
            self.y = 800
            return
        if self.x < -64:
            if remove is True:
                self.image = self.images[-1]
                self.state = RiderState.Dead
                self.next_update_time = current_time + 2000
            else:
                self.x = 900
        if self.x > 900:
            if remove is True:
                self.image = self.images[-1]
                self.state = RiderState.Dead
                self.next_update_time = current_time + 2000
            else:
                self.x = -48


class RiderState(IntEnum):
    Dead = 0
    Unmounted = 1
    Mounted = 2
