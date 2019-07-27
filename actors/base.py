import abc
import random

import pygame


class Actor(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
    name = ""

    def __init__(self, game, x, y, images, spawn_images, unmounted_images):
        super().__init__()
        self.game = game
        self.images = images
        self.spawn_images = spawn_images
        self.unmounted_images = unmounted_images
        self.frameNum = 0
        self.image = self.spawn_images[0]
        self.rect = self.image.get_rect()
        self.next_update_time = 0
        self.next_anim_time = 0
        self.starting_x = x
        self.starting_y = y
        self.x = x
        self.y = y
        self.flap = 0
        self.facingRight = True
        self.x_speed = random.randint(3, 10)
        self.target_x_speed = 10
        self.y_speed = 0
        self.walking = True
        self.flapCount = 0
        self.spawning = True
        self.alive = True

    @abc.abstractmethod
    def bounce(self, colliding_object):
        pass

    @abc.abstractmethod
    def die(self):
        pass

    @abc.abstractmethod
    def respawn(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass


class Rider(Actor, metaclass=abc.ABCMeta):
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
