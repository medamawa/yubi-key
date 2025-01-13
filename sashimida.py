import pygame
from pygame.locals import *
import sys

import config
from game import game
from game import game_yubi
from game import game_dvorak
from game import game_battle
from game import title
from game import result
from game import result_battle

def main():
    # initialization
    pygame.init()
    SURFACE = pygame.display.set_mode(config.WINDOW_SIZE)
    pygame.display.set_caption(config.TITLE)
    font = pygame.font.Font(config.FONT_FILE, config.FONT_SIZE)
    score = 0
    dishes = 0

    # main loop
    while True:
        mode = title.main(SURFACE)
        if mode == 1:
            score, dishes = game.main(SURFACE, font)
        elif mode == 2:
            score, dishes = game_yubi.main(SURFACE, font)
        elif mode == 3:
            score, dishes = game_dvorak.main(SURFACE, font)
        elif mode == 4:
            score_yubi, dishes_yubi, score_dvorak, dishes_dvorak = game_battle.main(SURFACE, font)
            if score_yubi == -1:
                continue
            result_battle.main(SURFACE, score_yubi, dishes_yubi, score_dvorak, dishes_dvorak)
            continue
        if score == -1:
            continue
        result.main(SURFACE, score, dishes)
        

if __name__ == '__main__':
    main()