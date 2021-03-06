from enum import IntEnum

import pygame


class ActionKey(IntEnum):
    GameExit = 0
    GodMode = 1
    Left = 2
    Right = 3
    Flap = 4
    AddPlayer = 5
    SpawnEgg = 6


global_keys = {
    pygame.K_ESCAPE: ActionKey.GameExit,
    pygame.K_g: ActionKey.GodMode,
    pygame.K_F2: ActionKey.AddPlayer,
    pygame.K_F3: ActionKey.SpawnEgg,
}


player_one = {
    pygame.K_LEFT: ActionKey.Left,
    pygame.K_RIGHT: ActionKey.Right,
    pygame.K_SPACE: ActionKey.Flap,
}

player_two = {
    pygame.K_a: ActionKey.Left,
    pygame.K_d: ActionKey.Right,
    pygame.K_f: ActionKey.Flap,
}
