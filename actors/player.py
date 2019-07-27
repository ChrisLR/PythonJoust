from actors.base import Rider
import pygame


class Player(Rider):
    def __init__(self, game, x, y, bird_images, spawn_images, player_unmounted_images):
        super().__init__(game, x, y, bird_images, spawn_images, player_unmounted_images)
        self.frameNum = 2
        self.image = self.images[self.frameNum]
        self.rect = self.image.get_rect()
        self.playerChannel = pygame.mixer.Channel(0)
        self.flapsound = pygame.mixer.Sound("joustflaedit.wav")
        self.skidsound = pygame.mixer.Sound("joustski.wav")
        self.bumpsound = pygame.mixer.Sound("joustthu.wav")
        self.lives = 4
        self.spawning = True
        self.alive = 2

    def update(self, current_time, keys, platforms, enemies, god, eggList, eggimages):
        # Update every 30 milliseconds

        if self.next_update_time < current_time:
            self.next_update_time = current_time + 30
            if self.alive == 2:
                if self.spawning:
                    self.frameNum += 1
                    self.image = self.spawnimages[self.frameNum]
                    self.next_update_time += 100
                    self.rect.topleft = (self.x, self.y)
                    if self.frameNum == 5:
                        self.frameNum = 4
                        self.spawning = False
                else:
                    if keys[pygame.K_LEFT]:
                        if self.xspeed > -10:
                            self.xspeed -= 0.5
                    elif keys[pygame.K_RIGHT]:
                        if self.xspeed < 10:
                            self.xspeed += 0.5
                    if keys[pygame.K_SPACE]:
                        if self.flap == False:
                            self.playerChannel.stop()
                            self.flapsound.play(0)
                            if self.yspeed > -250:
                                self.yspeed -= 3
                            self.flap = True
                    else:
                        self.flap = False
                    self.x = self.x + self.xspeed
                    self.y = self.y + self.yspeed
                    if not self.walking:
                        self.yspeed += 0.4
                    if self.yspeed > 10:
                        self.yspeed = 10
                    if self.yspeed < -10:
                        self.yspeed = -10
                    if self.y < 0:
                        self.y = 0
                        self.yspeed = 2
                    if self.y > 570:
                        self.die()
                    if self.x < -48:
                        self.x = 900
                    if self.x > 900:
                        self.x = -48
                    self.rect.topleft = (self.x, self.y)
                    # check for enemy collision
                    collidedBirds = pygame.sprite.spritecollide(self, enemies, False,
                                                                collided=pygame.sprite.collide_mask)
                    for bird in collidedBirds:
                        # check each bird to see if above or below
                        if bird.y > self.y and bird.alive:
                            self.bounce(bird)
                            bird.killed(eggList, eggimages)
                            bird.bounce(self)
                        elif bird.y < self.y - 5 and bird.alive and not god.on:
                            self.bounce(bird)
                            bird.bounce(self)
                            self.die()

                            break
                        elif bird.alive:
                            self.bounce(bird)
                            bird.bounce(self)
                    # check for platform collision
                    collidedPlatforms = pygame.sprite.spritecollide(self, platforms, False,
                                                                    collided=pygame.sprite.collide_mask)
                    self.walking = False
                    if (((self.y > 40 and self.y < 45) or (self.y > 250 and self.y < 255)) and (
                            self.x < 0 or self.x > 860)):  # catch when it is walking between screens
                        self.walking = True
                        self.yspeed = 0
                    else:
                        collided = False
                        for collidedPlatform in collidedPlatforms:
                            collided = self.bounce(collidedPlatform)
                        if collided:
                            # play a bump sound
                            self.playerChannel.play(self.bumpsound)
                    self.rect.topleft = (self.x, self.y)
                    if self.walking:
                        # if walking
                        if self.next_anim_time < current_time:
                            if self.xspeed != 0:
                                if (self.xspeed > 5 and keys[pygame.K_LEFT]) or (
                                        self.xspeed < -5 and keys[pygame.K_RIGHT]):

                                    if self.frameNum != 4:
                                        self.playerChannel.play(self.skidsound)
                                    self.frameNum = 4
                                else:
                                    self.next_anim_time = current_time + 200 / abs(self.xspeed)
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
                    if self.xspeed < 0 or (self.xspeed == 0 and self.facingRight == False):
                        self.image = pygame.transform.flip(self.image, True, False)
                        self.facingRight = False
                    else:
                        self.facingRight = True
            elif self.alive == 1:
                # unmounted player, lone bird
                # see if we need to accelerate
                if abs(self.xspeed) < self.targetXSpeed:
                    if abs(self.xspeed) > 0:
                        self.xspeed += self.xspeed / abs(self.xspeed) / 2
                    else:
                        self.xspeed += 0.5
                # work out if flapping...
                if self.flap < 1:
                    if (random.randint(0, 10) > 8 or self.y > 450):  # flap to avoid lava
                        self.yspeed -= 3
                        self.flap = 3
                else:
                    self.flap -= 1

                self.x = self.x + self.xspeed
                self.y = self.y + self.yspeed
                if not self.walking:
                    self.yspeed += 0.4
                if self.yspeed > 10:
                    self.yspeed = 10
                if self.yspeed < -10:
                    self.yspeed = -10
                if self.y < 0:  # can't go off the top
                    self.y = 0
                    self.yspeed = 2

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
                collidedPlatforms = pygame.sprite.spritecollide(self, platforms, False,
                                                                collided=pygame.sprite.collide_mask)
                self.walking = False
                if (((self.y > 40 and self.y < 45) or (self.y > 220 and self.y < 225)) and (
                        self.x < 0 or self.x > 860)):  # catch when it is walking between screens
                    self.walking = True
                    self.yspeed = 0
                else:
                    for collidedPlatform in collidedPlatforms:
                        self.bounce(collidedPlatform)
                self.rect.topleft = (self.x, self.y)
                if self.walking:
                    if self.next_anim_time < current_time:
                        if self.xspeed != 0:
                            self.next_anim_time = current_time + 100 / abs(self.xspeed)
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
                self.image = self.unmountedimages[self.frameNum]
                if self.xspeed < 0 or (self.xspeed == 0 and self.facingRight == False):
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.facingRight = False
                else:
                    self.facingRight = True
            else:
                # player respawn
                self.respawn()

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
        self.xspeed = 0
        self.yspeed = 0
        self.flap = False
        self.walking = True
        self.spawning = True
        self.alive = 2
