import pygame
from pygame.locals import *
import sys

import config
import game
import title

def main():
    # initialization
    pygame.init()
    SURFACE = pygame.display.set_mode(config.WINDOW_SIZE)
    pygame.display.set_caption(config.TITLE)
    font = pygame.font.Font(config.FONT_FILE, config.FONT_SIZE)

    # main loop
    while True:
        title.main(SURFACE, font)
        game.main(SURFACE, font)

if __name__ == '__main__':
    main()