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

def main(SCREEN, score_yubi, dishes_yubi, score_dvorak, dishes_dvorak):
    # surface
    SURFACE_YUBI = pygame.Surface(config.WINDOW_SIZE)
    SURFACE_DVORAK = pygame.Surface(config.WINDOW_SIZE)
	
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
    result_text_1_yubi = result_font.render(f"{dishes_yubi}皿食べて", True, config.BLACK)
    result_text_2_yubi = result_font.render("合計", True, config.BLACK)
    result_text_3_yubi = result_font_big.render(f"{score_yubi}円", True, config.BLACK)
    result_text_1_dvorak = result_font.render(f"{dishes_dvorak}皿食べて", True, config.BLACK)
    result_text_2_dvorak = result_font.render("合計", True, config.BLACK)
    result_text_3_dvorak = result_font_big.render(f"{score_dvorak}円", True, config.BLACK)

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
        SURFACE_YUBI.blit(door_left, (door_left_x, 0))
        SURFACE_YUBI.blit(door_right, (door_right_x, 0))
        SURFACE_YUBI.blit(frame, (0, 0))
        SURFACE_DVORAK.blit(door_left, (door_left_x, 0))
        SURFACE_DVORAK.blit(door_right, (door_right_x, 0))
        SURFACE_DVORAK.blit(frame, (0, 0))
        
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
                        SCREEN = pygame.display.set_mode(config.WINDOW_SIZE)
                        return
            if end_button.is_clicked(event):
                pygame.quit()
                sys.exit()
        
		# get time
        time_passed = time.time() - start_time
        
		# score
        if time_passed > 0.15:
            pu.put_middle(SURFACE_YUBI, background_rect, 220)
            end_button.draw(SURFACE_YUBI, end_button_font)
            pu.put_middle(SURFACE_DVORAK, background_rect, 220)
            end_button.draw(SURFACE_DVORAK, end_button_font)
        if time_passed > 0.45:
            if not result_sound_flag:
                sound_result.play()
                result_sound_flag = True
            pu.put_middle(SURFACE_YUBI, result_text_1_yubi, 250)
            pu.put_middle(SURFACE_DVORAK, result_text_1_dvorak, 250)
        if time_passed > 1.05:
            pu.put_middle(SURFACE_YUBI, result_text_2_yubi, 340)
            pu.put_middle(SURFACE_DVORAK, result_text_2_dvorak, 340)
        if time_passed > 1.55:
            pu.put_middle(SURFACE_YUBI, result_text_3_yubi, 440)
            pu.put_middle(SURFACE_DVORAK, result_text_3_dvorak, 440)
            if not effect_end_flag:
                effect_end_flag = True
        
        
        # refresh window
        new_width = config.BATTLE_WINDOW_WIDTH / 2
        new_height = new_width * config.WINDOW_HEIGHT / config.WINDOW_WIDTH
        offset_y = (config.BATTLE_WINDOW_HEIGHT - new_height) // 2
        SURFACE_YUBI_SCALED = pygame.transform.scale(SURFACE_YUBI, (new_width, new_height))
        SURFACE_DVORAK_SCALED = pygame.transform.scale(SURFACE_DVORAK, (new_width, new_height))
        SCREEN.fill(config.WHITE)
        SCREEN.blit(SURFACE_YUBI_SCALED, (0, offset_y))
        SCREEN.blit(SURFACE_DVORAK_SCALED, (config.BATTLE_WINDOW_WIDTH / 2, offset_y))
        pygame.display.update()