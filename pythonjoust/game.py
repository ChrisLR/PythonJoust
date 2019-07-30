# Original Joust Code by S Paget

import pygame

from pythonjoust import keymap
from pythonjoust.actors import Player
from pythonjoust.hud import HUD
from pythonjoust.spriteloader import Spriteloader
from pythonjoust.soundmixer import SoundMixer


class GodMode(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = game.sprite_loader.get_image("god.png")
        self.on = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (850, 0)
        self.timer = pygame.time.get_ticks()

    def toggle(self, current_time):
        if current_time >= self.timer:
            if self.on is True:
                self.on = False
                self.game.unregister_sprite(self)
            else:
                self.on = True
                self.game.register_sprite(self)
            self.timer = current_time + 1000


class Game(object):
    def __init__(self):
        self.window = pygame.display.set_mode((900, 650))
        pygame.display.set_caption('Joust')
        self.screen = pygame.display.get_surface()
        self.clear_surface = self.screen.copy()
        self.sprite_loader = Spriteloader()

        self.enemies = []
        self.god_mode = GodMode(self)
        self.hud = HUD(self)
        self.level = None
        self.players = []
        self.render_updates = {}
        self.running = False
        self.score = 0
        self.sound_mixer = SoundMixer()

    @property
    def lives(self):
        return self.players[0].lives

    def register_sprite(self, sprite):
        render_update = self.render_updates.setdefault(
            type(sprite),
            pygame.sprite.RenderUpdates()
        )
        render_update.add(sprite)

    def unregister_sprite(self, sprite):
        render_update = self.render_updates.get(type(sprite))
        if render_update is not None:
            render_update.remove(sprite)

    def start(self, level):
        self.level = level
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