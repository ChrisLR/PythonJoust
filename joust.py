# Joust by S Paget

import pygame, random
from spriteloader import Spriteloader

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


class GodMode(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pic = pygame.image.load("god.png")
        self.image = self.pic
        self.on = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (850, 0)
        self.timer = pygame.time.get_ticks()

    def toggle(self, current_time):
        if current_time > self.timer:
            self.on = not self.on
            self.timer = current_time + 1000


def drawLava(screen):
    lavaRect = [0, 600, 900, 50]
    pygame.draw.rect(screen, (255, 0, 0), lavaRect)
    return lavaRect


def drawLava2(screen):
    lavaRect = [0, 620, 900, 30]
    pygame.draw.rect(screen, (255, 0, 0), lavaRect)
    return lavaRect


def drawLives(lives, screen, lifeimage):
    startx = 375
    for num in range(lives):
        x = startx + num * 20
        screen.blit(lifeimage, [x, 570])


def drawScore(score, screen, digits):
    screen.blit(digits[score % 10], [353, 570])
    screen.blit(digits[(score % 100) // 10], [335, 570])
    screen.blit(digits[(score % 1000) // 100], [317, 570])
    screen.blit(digits[(score % 10000) // 1000], [299, 570])
    screen.blit(digits[(score % 100000) // 10000], [281, 570])
    screen.blit(digits[(score % 1000000) // 100000], [263, 570])


class Game(object):
    def __init__(self):
        self.sprite_loader = Spriteloader()
        self.god_mode = GodMode()
        self.enemies = []
        self.platforms = []
        self.players = []

    def prepare_platforms(self, sprite_loader):
        platform_images = [
            sprite_loader.get_image("plat1.png"),
            sprite_loader.get_image("plat2.png"),
            sprite_loader.get_image("plat3.png"),
            sprite_loader.get_image("plat4.png"),
            sprite_loader.get_image("plat5.png"),
            sprite_loader.get_image("plat6.png"),
            sprite_loader.get_image("plat7.png"),
            sprite_loader.get_image("plat8.png"),
        ]

        return platform_images

    def generateEnemies(self, enemyimages, spawnimages, unmountedimages, enemyList, spawnPoints, enemiesToSpawn):
        # makes 2 enemies at a time, at 2 random spawn points
        for count in range(2):
            enemyList.add(enemyClass(enemyimages, spawnimages, unmountedimages, spawnPoints[random.randint(0, 3)],
                                     0))  # last 0 is enemytype
            enemiesToSpawn -= 1

        return enemyList, enemiesToSpawn


def main():
    window = pygame.display.set_mode((900, 650))
    pygame.display.set_caption('Joust')
    screen = pygame.display.get_surface()
    clearSurface = screen.copy()
    player = pygame.sprite.RenderUpdates()
    enemyList = pygame.sprite.RenderUpdates()
    eggList = pygame.sprite.RenderUpdates()
    platforms = pygame.sprite.RenderUpdates()
    godSprite = pygame.sprite.RenderUpdates()
    birdimages = spriteloader.get_sliced_sprites(60, 60, "playerMounted.png")
    enemyimages = spriteloader.get_sliced_sprites(60, 58, "enemies2.png")
    spawnimages = spriteloader.get_sliced_sprites(60, 60, "spawn1.png")
    unmountedimages = spriteloader.get_sliced_sprites(60, 60, "unmounted.png")
    playerUnmountedimages = spriteloader.get_sliced_sprites(60, 60, "playerUnmounted.png")
    eggimages = spriteloader.get_sliced_sprites(40, 33, "egg.png")
    lifeimage = pygame.image.load("life.png")
    lifeimage = lifeimage.convert_alpha()
    digits = spriteloader.get_sliced_sprites(21, 21, "digits.png")
    platformImages = spriteloader.load_platforms()
    playerbird = playerClass(birdimages, spawnimages, playerUnmountedimages)
    god = godmode()
    godSprite.add(godmode())
    spawnPoints = [[690, 248], [420, 500], [420, 80], [50, 255]]
    plat1 = platformClass(platformImages[0], 200,
                          550)  # we create each platform by sending it the relevant platform image, the x position of the platform and the y position
    plat2 = platformClass(platformImages[1], 350, 395)
    plat3 = platformClass(platformImages[2], 350, 130)
    plat4 = platformClass(platformImages[3], 0, 100)
    plat5 = platformClass(platformImages[4], 759, 100)
    plat6 = platformClass(platformImages[5], 0, 310)
    plat7 = platformClass(platformImages[6], 759, 310)
    plat8 = platformClass(platformImages[7], 600, 290)
    player.add(playerbird)
    platforms.add(plat1, plat2, plat3, plat4, plat5, plat6, plat7, plat8)
    pygame.display.update()
    nextSpawnTime = pygame.time.get_ticks() + 2000
    enemiesToSpawn = 6  # test. make 6 enemies to start
    score = 0
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        # make enemies
        if current_time > nextSpawnTime and enemiesToSpawn > 0:
            enemyList, enemiesToSpawn = generateEnemies(enemyimages, spawnimages, unmountedimages, enemyList,
                                                        spawnPoints, enemiesToSpawn)
            nextSpawnTime = current_time + 5000
        keys = pygame.key.get_pressed()
        pygame.event.clear()
        # If they have pressed Escape, close down Pygame
        if keys[pygame.K_ESCAPE]:
            running = False
        # check for God mode toggle
        if keys[pygame.K_g]:
            god.toggle(current_time)
        player.update(current_time, keys, platforms, enemyList, god, eggList, eggimages)
        platforms.update()
        enemyList.update(current_time, keys, platforms, god)
        eggList.update(current_time, platforms)
        enemiesRects = enemyList.draw(screen)
        if god.on:
            godrect = godSprite.draw(screen)
        else:
            godrect = pygame.Rect(850, 0, 50, 50)
        playerRect = player.draw(screen)
        eggRects = eggList.draw(screen)
        lavaRect = drawLava(screen)
        platRects = platforms.draw(screen)
        lavarect2 = drawLava2(screen)
        drawLives(playerbird.lives, screen, lifeimage)
        drawScore(score, screen, digits)
        pygame.display.update(playerRect)
        pygame.display.update(lavaRect)
        pygame.display.update(lavarect2)
        pygame.display.update(platRects)
        pygame.display.update(enemiesRects)
        pygame.display.update(eggRects)
        pygame.display.update(godrect)
        player.clear(screen, clearSurface)
        enemyList.clear(screen, clearSurface)
        eggList.clear(screen, clearSurface)
        godSprite.clear(screen, clearSurface)


main()
pygame.quit()
