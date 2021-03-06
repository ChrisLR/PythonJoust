import random

import pygame

from pythonjoust.actors import listing
from pythonjoust.actors.base import Rider, RiderState
from pythonjoust.input import keymap

# TODO Could be in game rules instead
EGGS_DESTROY_MAX_POINTS = 1000
EGGS_DESTROY_INCREMENT_POINTS = 250


@listing.register
class Player(Rider):
    name = "Player"
    update_cycle_time = 30

    def __init__(self, game, x, y, controller_input, player_number=1):
        sprite_loader = game.sprite_loader
        # TODO This way of setting the sprite needs to be improved
        try:
            bird_images = sprite_loader.get_autosized_sliced_sprites(f"player{player_number}Mounted.png", 8)
            unmounted_images = sprite_loader.get_autosized_sliced_sprites(f"player{player_number}UnMounted.png", 8)
            spawn_images = sprite_loader.get_sliced_sprites(60, 60, f"spawnPlayer{player_number}.png")
        except AttributeError:
            # We try to grab the newest player's specific image file but fallback to the first player.
            bird_images = sprite_loader.get_sliced_sprites(60, 60, f"player1Mounted.png")
            unmounted_images = sprite_loader.get_sliced_sprites(60, 60, f"player1UnMounted.png")
            spawn_images = sprite_loader.get_sliced_sprites(60, 60, "spawnPlayer1.png")

        super().__init__(game, x, y, bird_images, spawn_images, unmounted_images)
        self.action_keys = set()
        self.lives = 4
        self.frame_num = 2
        self.image = self.images[self.frame_num]
        self.rect = self.image.get_rect()
        self.sound_mixer = game.sound_mixer
        self.spawning = True
        self.score = 0
        self.eggs_killed = 0
        self.controller_input = controller_input

    def handle_input(self, keyboard_keys):
        # TODO Actions should be called from here
        self.controller_input.handle_keyboard_keys(keyboard_keys)
        self.action_keys = self.controller_input.get_keymaps()

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
                    self.sound_mixer.play_flap()
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
            self._handle_egg_collisions()
            # check for platform collision
            collided = self._handle_platform_collision()
            if collided:
                # play a bump sound
                self.sound_mixer.play_bump()
            self.rect.topleft = (self.x, self.y)
            if self.walking:
                # if walking
                if self.next_anim_time < current_time:
                    if self.x_speed != 0:
                        if (self.x_speed > 5 and walking_left) or (
                                self.x_speed < -5 and walking_right):

                            if self.frame_num != 4:
                                self.sound_mixer.play_skid()
                            self.frame_num = 4
                        else:
                            self.next_anim_time = current_time + 200 / abs(self.x_speed)
                            self.frame_num += 1
                            if self.frame_num > 3:
                                self.frame_num = 0
                    elif self.frame_num == 4:
                        self.frame_num = 3

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
            if bird.state is not RiderState.Mounted:
                continue

            # check each bird to see if above or below
            if bird.y > self.y:
                self.bounce(bird)
                bird.die()
                bird.bounce(self)
                self.score += bird.score_value
            elif bird.y < self.y - 5 and not god_mode.on:
                self.bounce(bird)
                bird.bounce(self)
                self.die()

                break
            elif bird.state:
                self.bounce(bird)
                bird.bounce(self)

    def _handle_egg_collisions(self):
        # check for enemy collision
        colliding_eggs = pygame.sprite.spritecollide(
            self, self.game.level.eggs, False,
            collided=pygame.sprite.collide_mask
        )
        for egg in colliding_eggs:
            egg.die()
            self.eggs_killed += 1
            points = self.eggs_killed * EGGS_DESTROY_INCREMENT_POINTS
            points = EGGS_DESTROY_MAX_POINTS if points > EGGS_DESTROY_MAX_POINTS else points
            self.score += points

    def die(self):
        self.state = RiderState.Unmounted
        self.lives -= 1

    def respawn(self):
        self.state = RiderState.Mounted
        self.facing_right = True
        self.flap = False
        self.frame_num = 1
        self.image = self.images[self.frame_num]
        self.rect = self.image.get_rect()
        self.spawning = True
        self.walking = True
        self.x = self.starting_x
        self.y = self.starting_y
        self.x_speed = 0
        self.y_speed = 0
