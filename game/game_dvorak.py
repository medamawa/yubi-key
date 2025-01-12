import pygame
from pygame.locals import *
import sys
import random
import time

import config
from utils import pygame_utils as pu
from utils import dvorak_utils as du

def put_dvorak(SURFACE, dvorak_image, key):
    pu.put_middle(SURFACE, dvorak_image, 600)

    if key == '_':
        key = ' '

    id, shift = du.get_dvorak_id(key)

    origin_x = (config.WINDOW_WIDTH - dvorak_image.get_width()) // 2 + 17
    origin_y = 613
    width = 27
    margin = 6

    if id == None:
        return
    if id <= 11:
        x = origin_x + width * id + margin * id
        y = origin_y
        pygame.draw.rect(SURFACE, (255, 0, 0), (x, y, width, width), width=2)
    elif id <= 22:
        x = origin_x + width * (id - 12 + 0.6) + margin * (id - 12)
        y = origin_y + width + margin + 1
        pygame.draw.rect(SURFACE, (255, 0, 0), (x, y, width, width), width=2)
    elif id <= 33:
        x = origin_x + width * (id - 23 + 1.2) + 1 + margin * (id - 23)
        y = origin_y + width * 2 + margin * 2 + 1
        pygame.draw.rect(SURFACE, (255, 0, 0), (x, y, width, width), width=2)
    elif id <= 43:
        x = origin_x + width * (id - 34 + 1.8) + 1 + margin * (id - 34)
        y = origin_y + width * 3 + margin * 3 + 1
        pygame.draw.rect(SURFACE, (255, 0, 0), (x, y, width, width), width=2)

    if shift:
        x = origin_x
        y = origin_y + width * 3 + margin * 3 + 1
        pygame.draw.rect(SURFACE, (255, 0, 0), (x, y, width * 1.6, width), width=2)

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
    dvorak_image = pygame.image.load("./srcs/sashimida/dvorak.png")
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
    dvorak_image = pu.resize_by_ratio(dvorak_image, ratio)
    for i in range(8):
        sashimi_list[i] = pygame.transform.scale(sashimi_list[i], (int(sashimi_width * ratio), int(sashimi_height * ratio)))
    
    return background, rail, frame, dvorak_image, sashimi_list

def main(SURFACE, font):
    # font
    header_font = pygame.font.Font(config.HEADER_FONT_FILE, config.HEADER_FONT_SIZE)

    # images
    background, rail, frame, dvorak_image, sashimi_list = load_images()
    sashimi = random.choice(sashimi_list)
    rail_width = rail.get_size()[0]
    sashimi_width = sashimi.get_size()[0]
    rail_x = 45
    sashimi_x = 45 - sashimi_width

    # sounds
    sound_typing_good = pygame.mixer.Sound("./srcs/sashimida/typing_good.wav")
    sounf_typing_bad = pygame.mixer.Sound("./srcs/sashimida/typing_bad.wav")
    sound_get_sashimi = pygame.mixer.Sound("./srcs/sashimida/get_sashimi.wav")
    sound_time_up = pygame.mixer.Sound("./srcs/sashimida/time_up.wav")
    sound_game_bgm = pygame.mixer.Sound("./srcs/sashimida/game_bgm.wav")
    sound_game_bgm.play(-1)

    # flags
    time_up_flag = False
    question_init_flag = True

    # questions
    questions_list = read_file_lines(config.QUESTIONS_FILE)
    question = None

    # time
    start_time = time.time()

    # score
    score = 0
    dishes = 0

    # key
    key = None

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
            
            # time up flag
            if time_up_flag:
                continue
            
            # キー入力
            if event.type == KEYDOWN:
                # ESCキーならtitleに戻る
                if event.key == K_ESCAPE:
                    sound_game_bgm.stop()
                    return -1, -1
                else:
                    key = du.get_dvorak_input(pygame, event)
                    if key == question[typed_num]:
                        sound_typing_good.play()
                        score += 10
                        typed_num += 1
                    elif not pygame.key.get_mods() & KMOD_SHIFT:
                        sounf_typing_bad.play()
                    if typed_num == len(question):
                        sound_get_sashimi.play()
                        score += 50
                        dishes += 1
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

        # dvorak keyboard
        put_dvorak(SURFACE, dvorak_image, key)
        
        # frame rendering
        SURFACE.blit(frame, (0, 0))

        # remaining time
        remaining_time = config.PLAY_TIME - int(time.time() - start_time)
        if remaining_time <= 0:
            if not time_up_flag:
                sound_game_bgm.stop()
                sound_time_up.play()
                time_up_flag = True
            if remaining_time < -0.8:
                return score, dishes
        remaining_time_text = header_font.render(f"残り{remaining_time:02}秒", True, config.BLACK)
        SURFACE.blit(remaining_time_text, [70, 25])

        # score
        score_text = header_font.render(f"小計{score}円", True, config.BLACK)
        SURFACE.blit(score_text, [config.WINDOW_WIDTH - score_text.get_width() - 70, 25])
        
        # refresh window
        pygame.display.update()
