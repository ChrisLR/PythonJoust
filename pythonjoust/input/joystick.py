import pygame
from pygame import joystick

from pythonjoust.input.keymap import ActionKey


class Joystick(object):
    """
    This object turns Joystick Motions/Buttons into Game Actions
    """
    THRESHOLD = 0.2
    MAX_SPEED_PER_TICK = 20

    def __init__(self, joystick, mapping):
        self.joystick = joystick
        self.joystick.init()
        self.mapping = mapping

    def get_keymaps(self):
        joystick = self.joystick
        joystick_x = self.joystick.get_axis(0)
        num_buttons = joystick.get_numbuttons()
        pressed_buttons = [i for i in range(num_buttons) if joystick.get_button(i)]
        keymaps = self.mapping.get(joystick_x, pressed_buttons)

        return keymaps

    def handle_keyboard_keys(self, all_keys):
        pass


class JoystickMapping(object):
    def __init__(self, flap):
        self._mapping = {
            flap: ActionKey.Flap,
        }

    def get(self, joystick_x, buttons_pressed):
        maps = {self._mapping.get(button) for button in buttons_pressed}
        if joystick_x >= 0.5:
            maps.add(ActionKey.Right)
        elif joystick_x < -0.5:
            maps.add(ActionKey.Left)

        return maps

    @classmethod
    def default(cls):
        return cls(
            flap=0,
        )


def initialize_joysticks():
    joystick.init()
    return [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
