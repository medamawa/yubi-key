import cv2
from cv2 import aruco
import pygame
from pygame.locals import *
import sys
import random
import time

import config
from utils import finger_utils as fu
from utils import marker_utils as mu
from utils import pygame_utils as pu
from utils import dvorak_utils as du

def put_left_hand(SURFACE, font, left_hands_list, left_id):
    if left_id == 2 or left_id == 3:
        left_hand = left_hands_list[left_id]
        text = font.render(f"layer{left_id}", True, config.BLACK)
    else:
        left_hand = left_hands_list[0]
        text = font.render("layer1", True, config.BLACK)
    left_hand = pu.resize_by_ratio(left_hand, 0.4)

    pu.put_middle(SURFACE, left_hand, 560, x_offset=-90)
    pu.put_middle(SURFACE, text, 750, x_offset=-90)

def put_right_hand(SURFACE, font, right_hands_list, left_id, right_id):
    right_hand = right_hands_list[right_id]
    right_hand = pu.resize_by_ratio(right_hand, 0.4)

    char = fu.get_selecting_key(left_id, right_id)
    if char == " ":
        char = "_"
    elif char == "\n":
        char = "\\n"
    text = font.render(char, True, config.BLACK)

    pu.put_middle(SURFACE, right_hand, 560, x_offset=90)
    pu.put_middle(SURFACE, text, 750, x_offset=90)

def put_right_hands_list(SURFACE, font, right_hands_list, left_id):
    background_rect = pygame.Surface((390, 240), pygame.SRCALPHA)
    background_rect.fill((*config.WHITE, 128))
    pu.put_middle(SURFACE, background_rect, 550, x_offset=385)
    border_x = (config.WINDOW_WIDTH - 390) // 2 + 385
    pygame.draw.rect(SURFACE, config.BLACK, (border_x, 550, 390, 240), 2)
    

    for i in range (1, 6):
        right_hand = right_hands_list[i]
        right_hand = pu.resize_by_ratio(right_hand, 0.13)

        char = fu.get_selecting_key(left_id, i)
        if char == " ":
            char = "[space]"
        text = font.render(char, True, config.BLACK)

        pu.put_middle(SURFACE, right_hand, 560, x_offset=170 + 62 * i)
        pu.put_middle(SURFACE, text, 620, x_offset=173 + 62 * i)
    
    for i in range (6, 12):
        right_hand = right_hands_list[i]
        right_hand = pu.resize_by_ratio(right_hand, 0.13)

        char = fu.get_selecting_key(left_id, i)
        if char == " ":
            char = "_"
        elif char == "\n":
            char = "\\n"
        text = font.render(char, True, config.BLACK)

        pu.put_middle(SURFACE, right_hand, 680, x_offset=170 + 62 * (i - 5))
        pu.put_middle(SURFACE, text, 740, x_offset=173 + 62 * (i - 5))

def put_camera_frame(SURFACE, frame):
    pygame_frame = pu.convert_opencv_img_to_pygame(frame)
    pygame_frame = pu.resize_by_ratio(pygame_frame, 0.30)
    SURFACE.blit(pygame_frame, (100, 155))

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
    background = pygame.image.load("./srcs/sashimida/background_yubi.png")
    rail = pygame.image.load("./srcs/sashimida/rail.png")
    frame = pygame.image.load("./srcs/sashimida/frame.png")
    dvorak_image = pygame.image.load("./srcs/sashimida/dvorak.png")
    left_hands_file = [f'./srcs/hand_images/left{i}.png' for i in range(5)]
    right_hands_file = [f'./srcs/hand_images/right{i}.png' for i in range(12)]
    sashimi_list = []
    left_hands_list = []
    right_hands_list = []
    for i in range(1, 9):
        sashimi_list.append(pygame.image.load(f"./srcs/sashimida/sashimi{i}.png"))
    for file in left_hands_file:
        left_hands_list.append(pygame.image.load(file))
    for file in right_hands_file:
        right_hands_list.append(pygame.image.load(file).convert_alpha())
   
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
    
    return background, rail, frame, dvorak_image, sashimi_list, left_hands_list, right_hands_list

def main(SCREEN, font):
    # surface
    SCREEN = pygame.display.set_mode(config.BATTLE_WINDOW_SIZE)
    SURFACE_YUBI = pygame.Surface(config.WINDOW_SIZE)
    SURFACE_DVORAK = pygame.Surface(config.WINDOW_SIZE)

    # font
    header_font = pygame.font.Font(config.HEADER_FONT_FILE, config.HEADER_FONT_SIZE)

    # images
    background, rail, frame, dvorak_image, sashimi_list, left_hands_list, right_hands_list = load_images()
    sashimi_yubi = random.choice(sashimi_list)
    sashimi_dvorak = random.choice(sashimi_list)
    rail_width = rail.get_size()[0]
    sashimi_width = sashimi_yubi.get_size()[0]
    rail_x = 45
    sashimi_x_yubi = 45 - sashimi_width
    sashimi_x_dvorak = 45 - sashimi_width

    # sounds
    sound_typing_good = pygame.mixer.Sound("./srcs/sashimida/typing_good.wav")
    sounf_typing_bad = pygame.mixer.Sound("./srcs/sashimida/typing_bad.wav")
    sound_get_sashimi = pygame.mixer.Sound("./srcs/sashimida/get_sashimi.wav")
    sound_time_up = pygame.mixer.Sound("./srcs/sashimida/time_up.wav")
    sound_game_bgm = pygame.mixer.Sound("./srcs/sashimida/game_bgm.wav")

    # flags
    time_up_flag = False
    question_init_flag_yubi = True
    question_init_flag_dvorak = True
    yubi_miss_count = 0

    # questions
    questions_list = read_file_lines(config.QUESTIONS_FILE)
    question_yubi = None
    question_dvorak = None

    # score
    score_yubi = 0
    dishes_yubi = 0
    score_dvorak = 0
    dishes_dvorak = 0
    
	# key
    dvorak_key = None

    # initialize markers
    markers_info = mu.init_markers_info()

    # make aruco detector
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(dictionary, parameters)

    # camera setup
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    if not cap.isOpened():
        print("Webカメラが見つかりません")
        exit()

    # time
    start_time = time.time()
    if config.BGM_FLAG:
        sound_game_bgm.play(-1)

    while True:
        # get camera frame
        ret, cam_frame = cap.read()
        if not ret:
            break
        
		# extract ROI
        cam_frame = cam_frame[300:, :]

        # convert to gray
        gray = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2GRAY)

        # detect markers
        corners, ids, _ = detector.detectMarkers(gray)

        # マーカーを検出した場合
        if ids is not None:
            mu.get_markers_info(markers_info, corners, ids)
            for _, info in markers_info.items():
                if not info["detected"]:
                    continue
                center_x, center_y = info["center"]
                
                # 中心座標を描画(stateによって色を変える)0
                if (info["state"]):
                    cv2.circle(cam_frame, (center_x, center_y), 15, (0, 255, 0), -1)
                else:
                    cv2.circle(cam_frame, (center_x, center_y), 15, (0, 0, 255), -1)

        # flip frame
        cam_frame = cv2.flip(cam_frame, 1)

        # initialize question
        if question_init_flag_yubi:
            tmp = random.choice(questions_list)
            while question_yubi != None and tmp == question_yubi:
                tmp = random.choice(questions_list)
            question_yubi = tmp
            question_yubi = question_yubi.lower().replace(" ", "_")
            question_width_yubi = font.size(question_yubi)[0]
            question_pos_x_yubi = (config.WINDOW_WIDTH - question_width_yubi) // 2
            question_pos_y_yubi = 500
            typed_num_yubi = 0
            question_init_flag_yubi = False

        if question_init_flag_dvorak:
            tmp = random.choice(questions_list)
            while question_dvorak != None and tmp == question_dvorak:
                tmp = random.choice(questions_list)
            question_dvorak = tmp
            question_dvorak = question_dvorak.lower().replace(" ", "_")
            question_width_dvorak = font.size(question_dvorak)[0]
            question_pos_x_dvorak = (config.WINDOW_WIDTH - question_width_dvorak) // 2
            question_pos_y_dvorak = 500
            typed_num_dvorak = 0
            question_init_flag_dvorak = False

        # event handling
        for event in pygame.event.get():
            # 閉じるボタンが押されたら終了させる
            if event.type == QUIT:
                cap.release()
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
                    cap.release()
                    SCREEN = pygame.display.set_mode(config.WINDOW_SIZE)
                    return -1, -1, -1, -1
                else:
                    dvorak_key = du.get_dvorak_input(pygame, event)
                    if dvorak_key == question_dvorak[typed_num_dvorak]:
                        sound_typing_good.play()
                        score_dvorak += 10
                        typed_num_dvorak += 1
                    elif not pygame.key.get_mods() & KMOD_SHIFT:
                        sounf_typing_bad.play()
                    if typed_num_dvorak == len(question_dvorak):
                        sound_get_sashimi.play()
                        score_dvorak += 50
                        dishes_dvorak += 1
                        typed_num_dvorak = 0
                        question_init_flag_dvorak = True
        
		# yubi_key handling
        state_list = fu.get_state_list(markers_info)
        left_id = fu.get_left_id(state_list)
        right_id = fu.get_right_id(state_list)
        selecting = fu.get_selecting_key(left_id, right_id)
        
		# when yubi_key entered
        if not time_up_flag and not state_list[4] and markers_info[4]["state_history"][0]:
            if selecting == " " or selecting == "." or selecting == "\n":
                selecting = "_"
            if selecting == question_yubi[typed_num_yubi] or yubi_miss_count >= 1:
                sound_typing_good.play()
                score_yubi += 10
                typed_num_yubi += 1
                yubi_miss_count = 0
            else:
                yubi_miss_count += 1
                sounf_typing_bad.play()
            if typed_num_yubi == len(question_yubi):
                sound_get_sashimi.play()
                score_yubi += 50
                dishes_yubi += 1
                typed_num_yubi = 0
                question_init_flag_yubi = True
        
		# text rendering
        typed_text_yubi = question_yubi[:typed_num_yubi]
        remaining_text_yubi = question_yubi[typed_num_yubi:]
        typed_surface_yubi = font.render(typed_text_yubi, True, config.TYPED_COLOR)
        remaining_surface_yubi = font.render(remaining_text_yubi, True,config. REMAINING_COLOR)

        typed_text_dvorak = question_dvorak[:typed_num_dvorak]
        remaining_text_dvorak = question_dvorak[typed_num_dvorak:]
        typed_surface_dvorak = font.render(typed_text_dvorak, True, config.TYPED_COLOR)
        remaining_surface_dvorak = font.render(remaining_text_dvorak, True,config. REMAINING_COLOR)

        # remaining time
        remaining_time = config.PLAY_TIME - int(time.time() - start_time)
        if remaining_time <= 0:
            if not time_up_flag:
                sound_game_bgm.stop()
                sound_time_up.play()
                time_up_flag = True
            if remaining_time < -0.8:
                cap.release()
                return score_yubi, dishes_yubi, score_dvorak, dishes_dvorak
        remaining_time_text = header_font.render(f"残り{remaining_time:02}秒", True, config.BLACK)

        # score
        score_text_yubi = header_font.render(f"小計{score_yubi}円", True, config.BLACK)
        score_text_dvorak = header_font.render(f"小計{score_dvorak}円", True, config.BLACK)

		# rendering yubi_key surface
		# background
        SURFACE_YUBI.blit(background, (45, 130))
        put_camera_frame(SURFACE_YUBI, cam_frame)
        rail_x += config.BATTLE_RAIL_SPEED
        if rail_x > 45 + rail_width:
            rail_x = 45
        SURFACE_YUBI.blit(rail, (rail_x, 300))
        SURFACE_YUBI.blit(rail, (rail_x - rail_width, 300))
        
        # sashimi
        sashimi_x_yubi += config.BATTLE_RAIL_SPEED
        if sashimi_x_yubi > 45 + rail_width + 10 or question_init_flag_yubi:
            question_init_flag_yubi = True
            tmp = random.choice(sashimi_list)
            while tmp == sashimi_yubi:
                tmp = random.choice(sashimi_list)
            sashimi_yubi = tmp
            sashimi_x_yubi = 45 - sashimi_width
        SURFACE_YUBI.blit(sashimi_yubi, (sashimi_x_yubi, 230))
        
		# frame
        SURFACE_YUBI.blit(frame, (0, 0))
        
		# yubi_key
        ans_left_id, ans_right_id = fu.key_to_id(question_yubi[typed_num_yubi])
        put_left_hand(SURFACE_YUBI, font, left_hands_list, ans_left_id)
        put_right_hand(SURFACE_YUBI, font, right_hands_list, ans_left_id, ans_right_id)
        put_right_hands_list(SURFACE_YUBI, font, right_hands_list, ans_left_id)
        
		# text
        SURFACE_YUBI.blit(typed_surface_yubi, [question_pos_x_yubi, question_pos_y_yubi])
        SURFACE_YUBI.blit(remaining_surface_yubi, [question_pos_x_yubi + typed_surface_yubi.get_width(), question_pos_y_yubi])
        SURFACE_YUBI.blit(remaining_time_text, [70, 25])
        SURFACE_YUBI.blit(score_text_yubi, [config.WINDOW_WIDTH - score_text_yubi.get_width() - 70, 25])


		# rendering dvorak surface
		# background
        SURFACE_DVORAK.blit(background, (45, 130))
        SURFACE_DVORAK.blit(rail, (rail_x, 300))
        SURFACE_DVORAK.blit(rail, (rail_x - rail_width, 300))
        
		# sashimi
        sashimi_x_dvorak += config.BATTLE_RAIL_SPEED
        if sashimi_x_dvorak > 45 + rail_width + 10 or question_init_flag_dvorak:
            question_init_flag_dvorak = True
            tmp = random.choice(sashimi_list)
            while tmp == sashimi_dvorak:
                tmp = random.choice(sashimi_list)
            sashimi_dvorak = tmp
            sashimi_x_dvorak = 45 - sashimi_width
        SURFACE_DVORAK.blit(sashimi_dvorak, (sashimi_x_dvorak, 230))
        
		# frame
        SURFACE_DVORAK.blit(frame, (0, 0))
        
		# dvorak keyboard
        put_dvorak(SURFACE_DVORAK, dvorak_image, dvorak_key)
        
		# text
        SURFACE_DVORAK.blit(typed_surface_dvorak, [question_pos_x_dvorak, question_pos_y_dvorak])
        SURFACE_DVORAK.blit(remaining_surface_dvorak, [question_pos_x_dvorak + typed_surface_dvorak.get_width(), question_pos_y_dvorak])
        SURFACE_DVORAK.blit(remaining_time_text, [70, 25])
        SURFACE_DVORAK.blit(score_text_dvorak, [config.WINDOW_WIDTH - score_text_dvorak.get_width() - 70, 25])

        
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
