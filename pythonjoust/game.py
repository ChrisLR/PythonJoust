# Original Joust Code by S Paget

import random

import pygame

from pythonjoust.input import ActionKey, initialize_joysticks, keymap, Keyboard, KeyboardMapping, Joystick, JoystickMapping
from pythonjoust.actors import Player, listing
from pythonjoust.hud import HUD
from pythonjoust.soundmixer import SilentMixer
from pythonjoust.spriteloader import Spriteloader


class GodMode(pygame.sprite.Sprite):
    render_priority = 1

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
    def __init__(self, options):
        self.options = options
        self.window = pygame.display.set_mode((900, 650))
        pygame.display.set_caption('Joust')
        self.screen = pygame.display.get_surface()
        self.clear_surface = self.screen.copy()
        self.sprite_loader = Spriteloader(self)

        self.enemies = []
        self.god_mode = GodMode(self)
        self.hud = HUD(self)
        self.level = None
        self.players = []
        self.render_updates = {}
        self.running = False
        self.sound_mixer = SilentMixer()
        # self.sound_mixer = SoundMixer()
        self.previous_global_actions = set()
        self.joysticks = [
            Joystick(joystick, JoystickMapping.default())
            for joystick in initialize_joysticks()
        ]
        self.keyboards = [
            Keyboard(KeyboardMapping.default()),
            Keyboard(KeyboardMapping.alternate())
        ]

        # TODO This needs to be option based, not hardcoded
        all_inputs = []
        all_inputs.extend(self.joysticks)
        all_inputs.extend(self.keyboards)
        self.available_inputs = (i for i in all_inputs)

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

    def get_render_updates(self):
        sorted_list = sorted(
            self.render_updates.items(),
            key=lambda element: element[0].render_priority,
            reverse=True
        )
        return [render_update for key, render_update in sorted_list]

    def start(self, level):
        self.level = level
        self.add_player()
        level.prepare()
        pygame.display.update()
        self._run()

    def add_player(self):
        controller_input = next(self.available_inputs, None)
        if controller_input is None:
            # DEBUG!
            # controller_input = self.keyboards[0]
            return

        player_spawn_point = self.level.get_player_spawn()
        player = Player(
            self, *player_spawn_point,
            controller_input=controller_input,
            player_number=len(self.players) + 1
        )
        self.players.append(player)
        self.register_sprite(player)

    def spawn_random_egg(self):
        spawn_point = random.choice(self.level.enemy_spawn_points)
        egg = listing.get("Egg")(self, *spawn_point)
        egg.x_speed = random.randint(-25, 25)
        self.level.eggs.append(egg)
        self.register_sprite(egg)

    def _run(self):
        self.running = True
        while self.running:
            current_time = pygame.time.get_ticks()
            self.level.update(current_time)
            self._handle_input(current_time)
            draw_rects = []
            render_updates = self.get_render_updates()
            for render_update in render_updates:
                render_update.update(current_time)
                draw_rect = render_update.draw(self.screen)
                if draw_rect is not None:
                    draw_rects.extend(draw_rect)

            self.level.draw(self.screen)
            self.hud.draw()
            draw_rects.extend(self.level.lava_rectangles)
            pygame.display.update(draw_rects)

            for render_update in render_updates:
                render_update.clear(self.screen, self.clear_surface)

    def _handle_input(self, current_time):
        all_keys = pygame.key.get_pressed()
        pygame.event.clear()
        global_actions = {
            action for key, action in keymap.global_keys.items()
            if all_keys[key]
        }
        # If they have pressed Escape, close down Pygame
        if ActionKey.GameExit in global_actions:
            self.running = False

        add_player = ActionKey.AddPlayer
        if add_player in global_actions and add_player not in self.previous_global_actions:
            self.add_player()

        spawn_egg = ActionKey.SpawnEgg
        if spawn_egg in global_actions and spawn_egg not in self.previous_global_actions:
            self.spawn_random_egg()

        # check for God mode toggle
        if ActionKey.GodMode in global_actions:
            self.god_mode.toggle(current_time)

        for player in self.players:
            player.handle_input(all_keys)

        # TODO This can be improved
        self.previous_global_actions = global_actions
