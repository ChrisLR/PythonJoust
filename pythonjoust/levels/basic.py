import random

import pygame

from pythonjoust.actors import Enemy
from pythonjoust.terrain import Platform


class BasicLevel(object):
    def __init__(self, game):
        self.enemies = []
        self.enemies_to_spawn = 6  # test. make 6 enemies to start
        self.enemy_spawn_points = [
            [690, 248], [420, 500], [420, 80], [50, 255]
        ]
        self.game = game
        self.lava_rectangles = [
            [0, 600, 900, 50],
            [0, 620, 900, 30],
        ]
        sprite_loader = game.sprite_loader
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
        self.player_spawn_points = [
            (415, 350),
        ]
        self.next_spawn_time = 0
        self.eggs = []

    def clear(self):
        pass

    def draw(self, screen):
        self._draw_lava(screen)

    def _draw_lava(self, screen):
        for lava_rect in self.lava_rectangles:
            pygame.draw.rect(screen, (255, 0, 0), lava_rect)

    def get_player_spawn(self):
        return random.choice(self.player_spawn_points)

    def prepare(self):
        for platform in self.platforms:
            self.game.register_sprite(platform)
        self.spawn_enemies()
        self.next_spawn_time = pygame.time.get_ticks() + 2000

    def spawn_enemies(self):
        for count in range(2):
            spawn_point = random.choice(self.enemy_spawn_points)
            enemy = Enemy(self.game, *spawn_point)
            self.enemies.append(enemy)
            self.game.register_sprite(enemy)
            self.enemies_to_spawn -= 1

    def update(self, current_time):
        if current_time > self.next_spawn_time and self.enemies_to_spawn > 0:
            self.spawn_enemies()
            self.next_spawn_time = current_time + 5000
