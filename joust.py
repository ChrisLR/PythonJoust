# Joust by S Paget

import random
import pygame
from spriteloader import Spriteloader
from terrain.platform import Platform

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
        self.render_updates = {}
        self.window = pygame.display.set_mode((900, 650))
        pygame.display.set_caption('Joust')
        self.screen = pygame.display.get_surface()
        self.clear_surface = self.screen.copy()

    def register_sprite(self, sprite):
        render_update = self.render_updates.setdefault(
            type(sprite),
            pygame.sprite.RenderUpdates()
        )
        render_update.add(sprite)


def main():



    enemyimages = spriteloader.get_sliced_sprites(60, 58, "enemies2.png")

    unmountedimages = spriteloader.get_sliced_sprites(60, 60, "unmounted.png")


    lifeimage = pygame.image.load("life.png")
    lifeimage = lifeimage.convert_alpha()
    digits = spriteloader.get_sliced_sprites(21, 21, "digits.png")
    platformImages = spriteloader.load_platforms()
    playerbird = playerClass(birdimages, spawnimages, playerUnmountedimages)
    god = godmode()
    godSprite.add(godmode())


    player.add(playerbird)
    pygame.display.update()
    nextSpawnTime = pygame.time.get_ticks() + 2000

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
