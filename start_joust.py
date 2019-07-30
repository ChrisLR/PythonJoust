import pygame

from pythonjoust.levels import BasicLevel
from pythonjoust.joust import Game


if __name__ == '__main__':
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    game = Game()
    starting_level = BasicLevel(game)
    game.start(starting_level)
    pygame.quit()
