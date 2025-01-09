import pygame
from pygame.locals import *
import sys

import config
import pygame_utils as pg_utils

def load_images():
    # load images
    background = pygame.image.load("./srcs/sashimida/title_background.png")
    rail = pygame.image.load("./srcs/sashimida/rail.png")
    frame = pygame.image.load("./srcs/sashimida/frame.png")
    sashimi_list = []
    for i in range(1, 9):
        sashimi_list.append(pygame.image.load(f"./srcs/sashimida/sashimi{i}.png"))
    bg_width, bg_height = background.get_size()
    rail_width, rail_height = rail.get_size()
    frame_width, frame_height = frame.get_size()
    sashimi_width, sashimi_height = sashimi_list[0].get_size()
    ratio = config.WINDOW_WIDTH / frame_width

    # resize images
    background = pygame.transform.scale(background, (int(bg_width * ratio), int(bg_height * ratio)))
    rail = pygame.transform.scale(rail, (int(rail_width * ratio), int(rail_height * ratio)))
    frame = pygame.transform.scale(frame, (int(frame_width * ratio), int(frame_height * ratio)))
    for i in range(8):
        sashimi_list[i] = pygame.transform.scale(sashimi_list[i], (int(sashimi_width * ratio), int(sashimi_height * ratio)))
    
    return background, rail, frame, sashimi_list

def main(SURFACE):
    # images
    background, rail, frame, sashimi_list = load_images()
    rail_width = rail.get_size()[0]
    sashimi_width = sashimi_list[0].get_size()[0]
    rail_x = 45
    sashimi_x_list = [45 - sashimi_width + i * config.SASHIMI_MARGIN for i in range(len(sashimi_list))]

	# font
    start_button_font = pygame.font.Font(config.TITLE_BUTTON_FONT_FILE, config.TITLE_BUTTON_FONT_SIZE)
    end_button_font = pygame.font.Font(config.TITLE_BUTTON_FONT_FILE, config.TITLE_BUTTON_FONT_SIZE - 10)

	# button
    start_button = pg_utils.Button(config.WINDOW_WIDTH / 2, 580, 240, 60, "スタート", text_color=config.RED)
    end_button = pg_utils.Button(config.WINDOW_WIDTH / 2, 650, 160, 50, "お会計", text_color=config.GREEN)

    while True:
        SURFACE.blit(background, (45, 130))
        rail_x += config.TITLE_RAIL_SPEED
        if rail_x > 45 + rail_width:
            rail_x = 45
        SURFACE.blit(rail, (rail_x, 580))
        SURFACE.blit(rail, (rail_x - rail_width, 580))
        
		# sashimi
        sashimi_x_list = [x + config.TITLE_RAIL_SPEED for x in sashimi_x_list]
        for i, sashimi_x in enumerate(sashimi_x_list):
            if sashimi_x > 45 + rail_width + 10:
                sashimi_x_list[i] -= config.SASHIMI_MARGIN * len(sashimi_list)
        for i, sashimi in enumerate(sashimi_list):
            if sashimi_x_list[i] > 45 - sashimi_width and sashimi_x_list[i] < 45 + rail_width:
                SURFACE.blit(sashimi, (sashimi_x_list[i], 510))
        
		# button
        start_button.draw(SURFACE, start_button_font)
        end_button.draw(SURFACE, end_button_font)
        
		# event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                return
            if start_button.is_clicked(event):
                return
            if end_button.is_clicked(event):
                pygame.quit()
                sys.exit()
        
        # refresh window
        SURFACE.blit(frame, (0, 0))
        pygame.display.update()