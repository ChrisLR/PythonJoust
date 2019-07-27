
class eggClass(pygame.sprite.Sprite):
    def __init__(self, eggimages, x, y, xspeed, yspeed):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.images = eggimages
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed
        self.rect.topleft = (x, y)
        self.right = self.rect.right
        self.top = self.rect.top
        self.next_update_time = 0

    def move(self):
        # gravity
        self.yspeed += 0.4
        if self.yspeed > 10:
            self.yspeed = 10
        self.y += self.yspeed
        self.x += self.xspeed
        if self.y > 570:  # hit lava
            self.kill()

    def update(self, current_time, platforms):
        # Update every 30 milliseconds
        if self.next_update_time < current_time:
            self.next_update_time = current_time + 30
            self.move()
            self.rect.topleft = (self.x, self.y)
            collidedPlatforms = pygame.sprite.spritecollide(self, platforms, False, collided=pygame.sprite.collide_mask)
            if (((self.y > 40 and self.y < 45) or (self.y > 250 and self.y < 255)) and (
                    self.x < 0 or self.x > 860)):  # catch when it is rolling between screens
                self.yspeed = 0
            else:
                collided = False
                for collidedPlatform in collidedPlatforms:
                    collided = self.bounce(collidedPlatform)
            # wrap round screens
            if self.x < -48:
                self.x = 900
            if self.x > 900:
                self.x = -48

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
