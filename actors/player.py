import os
import random

import pygame

import keymap
from actors import listing
from actors.base import Rider


@listing.register
class Player(Rider):
    name = "Player"

    def __init__(self, game, x, y):
        sprite_loader = game.sprite_loader
        bird_images = sprite_loader.get_sliced_sprites(60, 60, "playerMounted.png")
        spawn_images = sprite_loader.get_sliced_sprites(60, 60, "spawn1.png")
        unmounted_images = sprite_loader.get_sliced_sprites(60, 60, "playerUnMounted.png")
        super().__init__(game, x, y, bird_images, spawn_images, unmounted_images)
        self.frameNum = 2
        self.image = self.images[self.frameNum]
        self.rect = self.image.get_rect()
        self.playerChannel = pygame.mixer.Channel(0)
        self.flap_sound = pygame.mixer.Sound(os.path.join("sounds", "joustflaedit.wav"))
        self.skid_sound = pygame.mixer.Sound(os.path.join("sounds", "joustski.wav"))
        self.bump_sound = pygame.mixer.Sound(os.path.join("sounds", "joustthu.wav"))
        self.lives = 4
        self.spawning = True
        self.alive = 2
        self.action_keys = None

    def handle_input(self, action_keys):
        # TODO This needs to handle actions.
        self.action_keys = action_keys

    def update(self, current_time):
        # TODO Can't we set the update time at the basic game level?
        # Update every 30 milliseconds

        if self.next_update_time < current_time:
            self.next_update_time = current_time + 30
            if self.alive == 2:
                if self.spawning:
                    self.frameNum += 1
                    self.image = self.spawn_images[self.frameNum]
                    self.next_update_time += 100
                    self.rect.topleft = (self.x, self.y)
                    if self.frameNum == 5:
                        self.frameNum = 4
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
                            self.playerChannel.stop()
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
                    if self.y < 0:
                        self.y = 0
                        self.y_speed = 2
                    if self.y > 570:
                        self.die()
                    if self.x < -48:
                        self.x = 900
                    if self.x > 900:
                        self.x = -48
                    self.rect.topleft = (self.x, self.y)
                    self._handle_bird_collisions()
                    # check for platform collision
                    collided = self._handle_platform_collision()
                    if collided:
                        # play a bump sound
                        self.playerChannel.play(self.bump_sound)
                    self.rect.topleft = (self.x, self.y)
                    if self.walking:
                        # if walking
                        if self.next_anim_time < current_time:
                            if self.x_speed != 0:
                                if (self.x_speed > 5 and walking_left) or (
                                        self.x_speed < -5 and walking_right):

                                    if self.frameNum != 4:
                                        self.playerChannel.play(self.skid_sound)
                                    self.frameNum = 4
                                else:
                                    self.next_anim_time = current_time + 200 / abs(self.x_speed)
                                    self.frameNum += 1
                                    if self.frameNum > 3:
                                        self.frameNum = 0
                            elif self.frameNum == 4:
                                self.frameNum = 3
                                self.playerChannel.stop()

                        self.image = self.images[self.frameNum]
                    else:
                        if self.flap:
                            self.image = self.images[6]

                        else:
                            self.image = self.images[5]
                    if self.x_speed < 0 or (self.x_speed == 0 and self.facingRight is False):
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.facingRight = False
                    else:
                        self.facingRight = True
            elif self.alive == 1:
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
                if self.y < 0:  # can't go off the top
                    self.y = 0
                    self.y_speed = 2

                if self.x < -48:  # off the left. remove entirely
                    self.image = self.images[7]
                    self.alive = 0
                    self.next_update_time = current_time + 2000
                if self.x > 900:  # off the right. remove entirely
                    self.image = self.images[7]
                    self.alive = 0
                    self.next_update_time = current_time + 2000
                self.rect.topleft = (self.x, self.y)
                # check for platform collision
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
                self.image = self.unmounted_images[self.frameNum]
                if self.x_speed < 0 or (self.x_speed == 0 and self.facingRight is False):
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.facingRight = False
                else:
                    self.facingRight = True
            else:
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
        self.frameNum = 1
        self.image = self.images[self.frameNum]
        self.rect = self.image.get_rect()
        self.x = 415
        self.y = 350
        self.facingRight = True
        self.x_speed = 0
        self.y_speed = 0
        self.flap = False
        self.walking = True
        self.spawning = True
        self.alive = 2
