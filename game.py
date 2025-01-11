import pygame
from pygame.locals import *
import sys
import random
import time

import config
import pygame_utils as pu

def read_file_lines(file_path):
    lines = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        # 各行の改行文字を取り除く
        lines = [line.strip() for line in lines]
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    except Exception as e:
        print(f"Error: {e}")
    
    return lines

def load_images():
    # load images
    background = pygame.image.load("./srcs/sashimida/background.png")
    rail = pygame.image.load("./srcs/sashimida/rail.png")
    frame = pygame.image.load("./srcs/sashimida/frame.png")
    sashimi_list = []
    for i in range(1, 9):
        sashimi_list.append(pygame.image.load(f"./srcs/sashimida/sashimi{i}.png"))
    frame_width, _ = frame.get_size()
    sashimi_width, sashimi_height = sashimi_list[0].get_size()
    ratio = config.WINDOW_WIDTH / frame_width

    # resize images
    background = pu.resize_by_ratio(background, ratio)
    rail = pu.resize_by_ratio(rail, ratio)
    frame = pu.resize_by_ratio(frame, ratio)
    for i in range(8):
        sashimi_list[i] = pygame.transform.scale(sashimi_list[i], (int(sashimi_width * ratio), int(sashimi_height * ratio)))
    
    return background, rail, frame, sashimi_list

def main(SURFACE, font):
    # font
    header_font = pygame.font.Font(config.HEADER_FONT_FILE, config.HEADER_FONT_SIZE)

    # images
    background, rail, frame, sashimi_list = load_images()
    sashimi = random.choice(sashimi_list)
    rail_width = rail.get_size()[0]
    sashimi_width = sashimi.get_size()[0]
    rail_x = 45
    sashimi_x = 45 - sashimi_width

    # sounds
    sound_typing_good = pygame.mixer.Sound("./srcs/sashimida/typing_good.wav")
    sounf_typing_bad = pygame.mixer.Sound("./srcs/sashimida/typing_bad.wav")
    sound_get_sashimi = pygame.mixer.Sound("./srcs/sashimida/get_sashimi.wav")

    # questions
    questions_list = read_file_lines("./srcs/questions.txt")
    question_init_flag = True
    question = None

    # time
    start_time = time.time()

    # score
    score = 0

    while True:
        SURFACE.blit(background, (45, 130))
        rail_x += config.RAIL_SPEED
        if rail_x > 45 + rail_width:
            rail_x = 45
        SURFACE.blit(rail, (rail_x, 300))
        SURFACE.blit(rail, (rail_x - rail_width, 300))

        # initialize question
        if question_init_flag:
            tmp = random.choice(questions_list)
            while question != None and tmp == question:
                tmp = random.choice(questions_list)
            question = tmp
            question = question.lower().replace(" ", "_")
            question_width = font.size(question)[0]
            question_pos_x = (config.WINDOW_WIDTH - question_width) // 2
            question_pos_y = 500
            typed_num = 0
            question_init_flag = False

        # event handling
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了させる
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # キー入力
            if event.type == KEYDOWN:
                # ESCキーならtitleに戻る
                if event.key == K_ESCAPE:
                    return -1
                else:
                    if pu.get_key_input(pygame, event) == question[typed_num]:
                        sound_typing_good.play()
                        score += 10
                        typed_num += 1
                    elif not pygame.key.get_mods() & KMOD_SHIFT:
                        sounf_typing_bad.play()
                    if typed_num == len(question):
                        sound_get_sashimi.play()
                        score += 50
                        question_init_flag = True
        
        # text rendering
        typed_text = question[:typed_num]
        remaining_text = question[typed_num:]
        typed_surface = font.render(typed_text, True, config.TYPED_COLOR)
        remaining_surface = font.render(remaining_text, True,config. REMAINING_COLOR)
        SURFACE.blit(typed_surface, [question_pos_x, question_pos_y])
        SURFACE.blit(remaining_surface, [question_pos_x + typed_surface.get_width(), question_pos_y])

        # sashimi surface
        sashimi_x += config.RAIL_SPEED
        if sashimi_x > 45 + rail_width + 10 or question_init_flag:
            question_init_flag = True
            tmp = random.choice(sashimi_list)
            while tmp == sashimi:
                tmp = random.choice(sashimi_list)
            sashimi = tmp
            sashimi_x = 45 - sashimi_width
        SURFACE.blit(sashimi, (sashimi_x, 230))
        
        # frame rendering
        SURFACE.blit(frame, (0, 0))

        # remaining time
        remaining_time = config.PLAY_TIME - int(time.time() - start_time)
        if remaining_time <= 0:
            return score
        remaining_time_text = header_font.render(f"残り{remaining_time:02}秒", True, config.BLACK)
        SURFACE.blit(remaining_time_text, [70, 25])

        # score
        score_text = header_font.render(f"小計{score}円", True, config.BLACK)
        SURFACE.blit(score_text, [config.WINDOW_WIDTH - score_text.get_width() - 70, 25])
        
        # refresh window
        pygame.display.update()
