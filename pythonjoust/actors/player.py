import os
import random

import pygame

from pythonjoust import keymap
from pythonjoust.actors import listing
from pythonjoust.actors.base import Rider


@listing.register
class Player(Rider):
    name = "Player"
    update_cycle_time = 30

    # TODO The Player should not be the one to handle sound
    sound_folder = os.path.join("pythonjoust", "sounds")

    def __init__(self, game, x, y):
        sprite_loader = game.sprite_loader
        bird_images = sprite_loader.get_sliced_sprites(60, 60, "playerMounted.png")
        spawn_images = sprite_loader.get_sliced_sprites(60, 60, "spawn1.png")
        unmounted_images = sprite_loader.get_sliced_sprites(60, 60, "playerUnMounted.png")
        super().__init__(game, x, y, bird_images, spawn_images, unmounted_images)
        self.frame_num = 2
        self.image = self.images[self.frame_num]
        self.rect = self.image.get_rect()
        self.player_channel = pygame.mixer.Channel(0)
        self.flap_sound = pygame.mixer.Sound(os.path.join(self.sound_folder, "joustflaedit.wav"))
        self.skid_sound = pygame.mixer.Sound(os.path.join(self.sound_folder, "joustski.wav"))
        self.bump_sound = pygame.mixer.Sound(os.path.join(self.sound_folder, "joustthu.wav"))
        self.lives = 4
        self.spawning = True
        self.alive = 2
        self.action_keys = None

    def handle_input(self, action_keys):
        # TODO This needs to handle actions.
        self.action_keys = action_keys

    def _update_mounted(self, current_time):
        if self.spawning:
            self.frame_num += 1
            self.image = self.spawn_images[self.frame_num]
            self.next_update_time += 100
            self.rect.topleft = (self.x, self.y)
            if self.frame_num == 5:
                self.frame_num = 4
                self.spawning = False
        else:
            walking_left = False
            walking_right = False
            flapping = False
            if keymap.ActionKey.Left in self.action_keys:
                walking_left = True
                if self.x_speed > -10:
                    self.x_speed -= 0.5
            elif keymap.ActionKey.Right in self.action_keys:
                walking_right = True
                if self.x_speed < 10:
                    self.x_speed += 0.5
            if keymap.ActionKey.Flap in self.action_keys:
                if not self.flap:
                    self.player_channel.stop()
                    self.flap_sound.play(0)
                    if self.y_speed > -250:
                        self.y_speed -= 3
                    flapping = True
                    self.flap = True
            else:
                self.flap = False
            self.x = self.x + self.x_speed
            self.y = self.y + self.y_speed
            if not flapping:
                self.y_speed += 0.4
            if self.y_speed > 10:
                self.y_speed = 10
            if self.y_speed < -10:
                self.y_speed = -10
            self._handle_out_of_bounds(current_time)
            self.rect.topleft = (self.x, self.y)
            self._handle_bird_collisions()
            # check for platform collision
            collided = self._handle_platform_collision()
            if collided:
                # play a bump sound
                self.player_channel.play(self.bump_sound)
            self.rect.topleft = (self.x, self.y)
            if self.walking:
                # if walking
                if self.next_anim_time < current_time:
                    if self.x_speed != 0:
                        if (self.x_speed > 5 and walking_left) or (
                                self.x_speed < -5 and walking_right):

                            if self.frame_num != 4:
                                self.player_channel.play(self.skid_sound)
                            self.frame_num = 4
                        else:
                            self.next_anim_time = current_time + 200 / abs(self.x_speed)
                            self.frame_num += 1
                            if self.frame_num > 3:
                                self.frame_num = 0
                    elif self.frame_num == 4:
                        self.frame_num = 3
                        self.player_channel.stop()

                self.image = self.images[self.frame_num]
            else:
                if self.flap:
                    self.image = self.images[6]

                else:
                    self.image = self.images[5]
            if self.x_speed < 0 or (self.x_speed == 0 and self.facing_right is False):
                self.image = pygame.transform.flip(self.image, True, False)
                self.facing_right = False
            else:
                self.facing_right = True

    def _update_unmounted(self, current_time):
        # unmounted player, lone bird
        # see if we need to accelerate
        if abs(self.x_speed) < self.target_x_speed:
            if abs(self.x_speed) > 0:
                self.x_speed += self.x_speed / abs(self.x_speed) / 2
            else:
                self.x_speed += 0.5
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

        self._handle_out_of_bounds(current_time, remove=True)

        self.rect.topleft = (self.x, self.y)
        # check for platform collision
        self._handle_platform_collision()
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
        self.image = self.unmounted_images[self.frame_num]
        if self.x_speed < 0 or (self.x_speed == 0 and self.facing_right is False):
            self.image = pygame.transform.flip(self.image, True, False)
            self.facing_right = False
        else:
            self.facing_right = True

    def _update_dead(self, current_time):
        # player respawn
        self.respawn()

    def _handle_bird_collisions(self):
        # check for enemy collision
        colliding_birds = pygame.sprite.spritecollide(
            self, self.game.level.enemies, False,
            collided=pygame.sprite.collide_mask
        )
        god_mode = self.game.god_mode
        for bird in colliding_birds:
            # check each bird to see if above or below
            if bird.y > self.y and bird.alive:
                self.bounce(bird)
                bird.die()
                bird.bounce(self)
            elif bird.y < self.y - 5 and bird.alive and not god_mode.on:
                self.bounce(bird)
                bird.bounce(self)
                self.die()

                break
            elif bird.alive:
                self.bounce(bird)
                bird.bounce(self)

    def die(self):
        self.lives -= 1
        self.alive = 1

    def respawn(self):
        self.frame_num = 1
        self.image = self.images[self.frame_num]
        self.rect = self.image.get_rect()
        self.x = self.starting_x
        self.y = self.starting_y
        self.facing_right = True
        self.x_speed = 0
        self.y_speed = 0
        self.flap = False
        self.walking = True
        self.spawning = True
        self.alive = 2
