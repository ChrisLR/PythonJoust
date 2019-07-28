# Joust by S Paget

import pygame

import keymap
from actors import Player
from levels import BasicLevel
from spriteloader import Spriteloader


class GodMode(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.pic = game.sprite_loader.get_image("god.png")
        self.image = self.pic
        self.on = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (850, 0)
        self.timer = pygame.time.get_ticks()

    def toggle(self, current_time):
        if current_time > self.timer:
            self.on = not self.on
            self.timer = current_time + 1000


class HUD(object):
    def __init__(self, game):
        self.game = game
        sprite_loader = game.sprite_loader
        self.life_image = sprite_loader.get_image("life.png").convert_alpha()
        self.digits_image = sprite_loader.get_sliced_sprites(21, 21, "digits.png")

    def draw(self):
        lives = self.game.lives
        score = self.game.score
        screen = self.game.screen
        self._draw_lives(lives, screen)
        self._draw_score(score, screen)

    def _draw_lives(self, lives, screen):
        start_x = 375
        for num in range(lives):
            x = start_x + num * 20
            screen.blit(self.life_image, [x, 570])

    def _draw_score(self, score, screen):
        digits_image = self.digits_image
        screen.blit(digits_image[score % 10], [353, 570])
        screen.blit(digits_image[(score % 100) // 10], [335, 570])
        screen.blit(digits_image[(score % 1000) // 100], [317, 570])
        screen.blit(digits_image[(score % 10000) // 1000], [299, 570])
        screen.blit(digits_image[(score % 100000) // 10000], [281, 570])
        screen.blit(digits_image[(score % 1000000) // 100000], [263, 570])


class Game(object):
    def __init__(self):
        self.sprite_loader = Spriteloader()
        self.god_mode = GodMode(self)
        self.enemies = []
        self.platforms = []
        self.players = []
        self.render_updates = {}
        self.window = pygame.display.set_mode((900, 650))
        pygame.display.set_caption('Joust')
        self.screen = pygame.display.get_surface()
        self.clear_surface = self.screen.copy()
        self.level = None
        self.hud = HUD(self)
        self.score = 0
        self.running = False

    @property
    def lives(self):
        return self.players[0].lives

    def register_sprite(self, sprite):
        render_update = self.render_updates.setdefault(
            type(sprite),
            pygame.sprite.RenderUpdates()
        )
        render_update.add(sprite)

    def start(self, level):
        self.level = level
        self.register_sprite(self.god_mode)
        player_spawn_point = level.get_player_spawn()
        player = Player(self, *player_spawn_point)
        self.players.append(player)
        self.register_sprite(player)
        level.prepare()
        pygame.display.update()
        self._run()

    def _run(self):
        self.running = True
        while self.running:
            current_time = pygame.time.get_ticks()
            self.level.update(current_time)
            self._handle_input(current_time)
            draw_rects = []
            for render_update in list(self.render_updates.values()):
                render_update.update(current_time)
                render_update.clear(self.screen, self.clear_surface)
                draw_rect = render_update.draw(self.screen)
                if draw_rect is not None:
                    draw_rects.extend(draw_rect)

            # TODO Handle not drawing god?
            # godrect = pygame.Rect(850, 0, 50, 50)

            self.level.draw(self.screen)
            self.hud.draw()
            draw_rects.extend(self.level.lava_rectangles)
            pygame.display.update(draw_rects)

    def _handle_input(self, current_time):
        all_keys = pygame.key.get_pressed()
        pygame.event.clear()
        global_actions = {
            action for key, action in keymap.global_keys.items()
            if all_keys[key]
        }
        # If they have pressed Escape, close down Pygame
        if keymap.ActionKey.GameExit in global_actions:
            self.running = False

        # check for God mode toggle
        if keymap.ActionKey.GodMode in global_actions:
            self.god_mode.toggle(current_time)

        # TODO Support more than one player
        player_one_actions = {
            action for key, action in keymap.player_one.items()
            if all_keys[key]
        }
        self.players[0].handle_input(player_one_actions)


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    game = Game()
    starting_level = BasicLevel(game)
    game.start(starting_level)
    pygame.quit()
