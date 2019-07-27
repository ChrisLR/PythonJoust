import abc
import random

import pygame


class Actor(pygame.sprite.Sprite, metaclass=abc.ABCMeta):
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

        self.images = birdimages
        self.unmountedimages = playerUnmountedimages
        self.spawnimages = spawnimages
        self.frameNum = 2
        self.image = self.images[self.frameNum]
        self.rect = self.image.get_rect()
        self.next_update_time = 0
        self.next_anim_time = 0
        self.x = 415
        self.y = 350
        self.facingRight = True
        self.xspeed = 0
        self.yspeed = 0
        self.targetXSpeed = 10
        self.flap = False
        self.walking = True
        self.playerChannel = pygame.mixer.Channel(0)
        self.flapsound = pygame.mixer.Sound("joustflaedit.wav")
        self.skidsound = pygame.mixer.Sound("joustski.wav")
        self.bumpsound = pygame.mixer.Sound("joustthu.wav")
        self.lives = 4
        self.spawning = True
        self.alive = 2

    @abc.abstractmethod
    def bounce(self):
        pass

    @abc.abstractmethod
    def die(self):
        pass

    @abc.abstractmethod
    def killed(self):
        pass

    @abc.abstractmethod
    def respawn(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass


class enemyClass(pygame.sprite.Sprite):
    def __init__(self, enemyimages, spawnimages, unmountedimages, startPos, enemyType):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.images = enemyimages
        self.spawnimages = spawnimages
        self.unmountedimages = unmountedimages
        self.frameNum = 0
        self.enemyType = enemyType
        self.image = self.spawnimages[0]
        self.rect = self.image.get_rect()
        self.next_update_time = 0
        self.next_anim_time = 0
        self.x = startPos[0]
        self.y = startPos[1]
        self.flap = 0
        self.facingRight = True
        self.xspeed = random.randint(3, 10)
        self.targetXSpeed = 10
        self.yspeed = 0
        self.walking = True
        self.flapCount = 0
        self.spawning = True
        self.alive = True

    def killed(self, eggList, eggimages):
        # make an egg appear here
        eggList.add(eggClass(eggimages, self.x, self.y, self.xspeed, self.yspeed))
        self.alive = False

    def update(self, current_time, keys, platforms, god):
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
                if abs(self.xspeed) < self.targetXSpeed:
                    self.xspeed += self.xspeed / abs(self.xspeed) / 2
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
                if self.alive:
                    self.image = self.images[((self.enemyType * 7) + self.frameNum)]
                else:
                    # show the unmounted sprite
                    self.image = self.unmountedimages[self.frameNum]
                if self.xspeed < 0 or (self.xspeed == 0 and self.facingRight == False):
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.facingRight = False
                else:
                    self.facingRight = True

    def bounce(self, collidedThing):
        collided = False
        if self.y < (collidedThing.y - 20) and (
        (self.x > (collidedThing.x - 40) and self.x < (collidedThing.rect.right - 10))):
            # coming in from the top?
            self.walking = True
            self.yspeed = 0
            self.y = collidedThing.y - self.rect.height + 3
        elif self.x < collidedThing.x:
            # colliding from left side
            collided = True
            self.x = self.x - 10
            self.xspeed = -2
        elif self.x > collidedThing.rect.right - 50:
            # colliding from right side
            collided = True
            self.x = self.x + 10
            self.xspeed = 2
        elif self.y > collidedThing.y:
            # colliding from bottom
            collided = True
            self.y = self.y + 10
            self.yspeed = 0
        return collided


class playerClass(pygame.sprite.Sprite):
    def __init__(self, birdimages, spawnimages, playerUnmountedimages):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.images = birdimages
        self.unmountedimages = playerUnmountedimages
        self.spawnimages = spawnimages
        self.frameNum = 2
        self.image = self.images[self.frameNum]
        self.rect = self.image.get_rect()
        self.next_update_time = 0
        self.next_anim_time = 0
        self.x = 415
        self.y = 350
        self.facingRight = True
        self.xspeed = 0
        self.yspeed = 0
        self.targetXSpeed = 10
        self.flap = False
        self.walking = True
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

    def bounce(self, collidedThing):
        collided = False
        if self.y < (collidedThing.y - 20) and (
        (self.x > (collidedThing.x - 40) and self.x < (collidedThing.rect.right - 10))):
            # coming in from the top?
            self.walking = True
            self.yspeed = 0
            self.y = collidedThing.y - self.rect.height + 1
        elif self.x < collidedThing.x:
            # colliding from left side
            collided = True
            self.x = self.x - 10
            self.xspeed = -2
        elif self.x > collidedThing.rect.right - 50:
            # colliding from right side
            collided = True
            self.x = self.x + 10
            self.xspeed = 2
        elif self.y > collidedThing.y:
            # colliding from bottom
            collided = True
            self.y = self.y + 10
            self.yspeed = 0
        return collided

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

