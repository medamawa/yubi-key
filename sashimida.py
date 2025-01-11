import pygame
from pygame.locals import *
import sys

import config
import game
import game_yubi
import title

def main():
    # initialization
    pygame.init()
    SURFACE = pygame.display.set_mode(config.WINDOW_SIZE)
    pygame.display.set_caption(config.TITLE)
    font = pygame.font.Font(config.FONT_FILE, config.FONT_SIZE)
    score = 0

    # main loop
    while True:
        mode = title.main(SURFACE)
        if mode == 1:
            score = game.main(SURFACE, font)
        elif mode == 2:
            score = game_yubi.main(SURFACE, font)

if __name__ == '__main__':
    main()