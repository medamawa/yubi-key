import pygame
from pygame.locals import *
import sys
import time

import config
from utils import pygame_utils as pu

def load_images():
    # load images
    frame = pygame.image.load("./srcs/sashimida/frame.png")
    door_left = pygame.image.load("./srcs/sashimida/door_left.png")
    door_right = pygame.image.load("./srcs/sashimida/door_right.png")
    frame_width, frame_height = frame.get_size()
    ratio = config.WINDOW_WIDTH / frame_width

    # resize images
    frame = pu.resize_by_ratio(frame, ratio)
    door_left = pu.resize_by_ratio(door_left, ratio)
    door_right = pu.resize_by_ratio(door_right, ratio)
    
    return frame, door_left, door_right

def main(SURFACE, score, dishes):
    # images
    frame, door_left, door_right = load_images()
    
	# sounds
    sound_door_close = pygame.mixer.Sound("./srcs/sashimida/door_close.wav")
    sound_result = pygame.mixer.Sound("./srcs/sashimida/result.wav")

	# font
    result_font = pygame.font.Font(config.HEADER_FONT_FILE, config.HEADER_FONT_SIZE)
    result_font_big = pygame.font.Font(config.HEADER_FONT_FILE, config.HEADER_FONT_SIZE + 20)
    end_button_font = pygame.font.Font(config.TITLE_BUTTON_FONT_FILE, config.TITLE_BUTTON_FONT_SIZE - 10)

	# button
    end_button = pu.Button(config.WINDOW_WIDTH / 2, 720, 160, 50, "お会計", text_color=config.GREEN)
    
	# score surface
    background_rect = pygame.Surface((600, 350), pygame.SRCALPHA)
    background_rect.fill((*config.WHITE, 128))
    result_text_1 = result_font.render(f"{dishes}皿食べて", True, config.BLACK)
    result_text_2 = result_font.render("合計", True, config.BLACK)
    result_text_3 = result_font_big.render(f"{score}円", True, config.BLACK)

	# flags
    result_sound_flag = False
    effect_end_flag = False

	# door variables
    door_left_x = 0 - door_left.get_size()[0]
    door_right_x = config.WINDOW_WIDTH
    door_speed = 80
    
	# door close sound
    sound_door_close.play()
    
	# time
    start_time = time.time()

    while True:
        door_left_x += door_speed
        if door_left_x > 0:
            door_left_x = 0
        door_right_x -= door_speed
        if door_right_x < config.WINDOW_WIDTH - door_right.get_size()[0]:
            door_right_x = config.WINDOW_WIDTH - door_right.get_size()[0]
            door_speed = 0
        SURFACE.blit(door_left, (door_left_x, 0))
        SURFACE.blit(door_right, (door_right_x, 0))
        SURFACE.blit(frame, (0, 0))
        
		# event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key in (pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LSHIFT, pygame.K_RSHIFT):
                    continue
                else:
                    if effect_end_flag:
                        return
            if end_button.is_clicked(event):
                pygame.quit()
                sys.exit()
        
		# get time
        time_passed = time.time() - start_time
        
		# score
        if time_passed > 0.15:
            pu.put_middle(SURFACE, background_rect, 220)
            end_button.draw(SURFACE, end_button_font)
        if time_passed > 0.45:
            if not result_sound_flag:
                sound_result.play()
                result_sound_flag = True
            pu.put_middle(SURFACE, result_text_1, 250)
        if time_passed > 1.05:
            pu.put_middle(SURFACE, result_text_2, 340)
        if time_passed > 1.55:
            pu.put_middle(SURFACE, result_text_3, 440)
            if not effect_end_flag:
                effect_end_flag = True
        
        
        # refresh window
        SURFACE.blit(frame, (0, 0))
        pygame.display.update()