import random

import pygame

from actors import Enemy
from terrain import Platform


class BasicLevel(object):
    def __init__(self, game):
        self.game = game
        self._lava_rectangles = [
            [0, 600, 900, 50],
            [0, 620, 900, 30],
        ]
        sprite_loader = game.sprite_loader
        # we create each platform by sending it the relevant platform image,
        # the x position of the platform and the y position
        self.platforms = [
            Platform(sprite_loader.get_image("plat1.png"), 200, 550),
            Platform(sprite_loader.get_image("plat2.png"), 350, 395),
            Platform(sprite_loader.get_image("plat3.png"), 350, 130),
            Platform(sprite_loader.get_image("plat4.png"), 0, 100),
            Platform(sprite_loader.get_image("plat5.png"), 759, 100),
            Platform(sprite_loader.get_image("plat6.png"), 0, 310),
            Platform(sprite_loader.get_image("plat7.png"), 759, 310),
            Platform(sprite_loader.get_image("plat8.png"), 600, 290),
        ]
        self.enemies_to_spawn = 6  # test. make 6 enemies to start
        self.enemy_spawn_points = [
            [690, 248], [420, 500], [420, 80], [50, 255]
        ]

    def prepare(self):
        for platform in self.platforms:
            self.game.register_sprite(platform)
        self.spawn_enemies()

    def clear(self):
        pass

    def draw(self):
        pass

    def update(self):
        pass

    def _draw_lava(self, screen):
        for lava_rect in self._lava_rectangles:
            pygame.draw.rect(screen, (255, 0, 0), lava_rect)

    def _draw_platforms(self):
        pass

    def spawn_enemies(self):
        # makes 2 enemies at a time, at 2 random spawn points
        for count in range(2):
            spawn_point = random.choice(self.enemy_spawn_points)
            enemy = Enemy(self.game, *spawn_point)
            self.game.register_sprite(enemy)
            self.enemies_to_spawn -= 1
