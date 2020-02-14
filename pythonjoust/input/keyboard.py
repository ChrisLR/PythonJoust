import pygame

from pythonjoust.input.keymap import ActionKey


class Keyboard(object):
    """
    This object receives keypresses and turn them into Game Actions
    """
    def __init__(self, mapping):
        self.pressed_keys = tuple()
        self.mapping = mapping

    def get_keymaps(self):
        return {value for key, value in self.mapping.items() if self.pressed_keys[key]}

    def handle_keyboard_keys(self, all_keys):
        self.pressed_keys = all_keys


class KeyboardMapping(object):
    def __init__(self, left, right, flap):
        self._mapping = {
            left: ActionKey.Left,
            right: ActionKey.Right,
            flap: ActionKey.Flap,
        }

    def get(self, symbol):
        return self._mapping.get(symbol)

    def items(self):
        return self._mapping.items()

    def handles_keypress(self, symbol):
        if symbol in self._mapping:
            return True
        return False

    @classmethod
    def default(cls):
        return cls(
            left=pygame.K_LEFT,
            right=pygame.K_RIGHT,
            flap=pygame.K_SPACE,
        )

    @classmethod
    def alternate(cls):
        return cls(
            left=pygame.K_a,
            right=pygame.K_d,
            flap=pygame.K_f,
        )
