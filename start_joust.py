import pygame

from pythonjoust.levels import BasicLevel
from pythonjoust.game import Game
from pythonjoust import config


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    game_options = config.load_ini()
    game = Game(game_options)
    starting_level = BasicLevel(game)
    game.start(starting_level)
    pygame.quit()
