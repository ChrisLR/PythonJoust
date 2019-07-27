from actors.base import Rider


class Enemy(Rider):
    def __init__(self, game, x, y, enemy_images, spawn_images, unmounted_images, enemy_type):
        super().__init__(game, x, y, enemy_images, spawn_images, unmounted_images)
        self.enemy_type = enemy_type

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

