import cv2
from cv2 import aruco
import pygame
from pygame.locals import *
import sys
import random
import time

import finger_utils as fu
import marker_utils as mu
import pygame_utils as pu
import config

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
        right_hands_list.append(pygame.image.load(file))
   
    frame_width, _ = frame.get_size()
    sashimi_width, sashimi_height = sashimi_list[0].get_size()
    ratio = config.WINDOW_WIDTH / frame_width

    # resize images
    background = pu.resize_by_ratio(background, ratio)
    rail = pu.resize_by_ratio(rail, ratio)
    frame = pu.resize_by_ratio(frame, ratio)
    for i in range(8):
        sashimi_list[i] = pygame.transform.scale(sashimi_list[i], (int(sashimi_width * ratio), int(sashimi_height * ratio)))
    
    return background, rail, frame, sashimi_list, left_hands_list, right_hands_list

def main(SURFACE, font):
    # font
    header_font = pygame.font.Font(config.HEADER_FONT_FILE, config.HEADER_FONT_SIZE)

    # images
    background, rail, frame, sashimi_list, left_hands_list, right_hands_list = load_images()
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

    # flags
    time_up_flag = False
    question_init_flag = True

    # questions
    questions_list = read_file_lines("./srcs/questions.txt")
    question = None

    # score
    score = 0
    dishes = 0

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
        

        
		# rendering background
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
                    return -1, -1
        
		# yubi_key handling
        state_list = fu.get_state_list(markers_info)
        left_id = fu.get_left_id(state_list)
        right_id = fu.get_right_id(state_list)
        selecting = fu.get_selecting_key(left_id, right_id)
        
		# when yubi_key entered
        if not time_up_flag and not state_list[4] and markers_info[4]["state_history"][0] and not markers_info[1]["state_history"][0]:
            if selecting == " " or selecting == "." or selecting == "\n":
                selecting = "_"
            if selecting == question[typed_num]:
                sound_typing_good.play()
                typed_num += 1
            else:
                sounf_typing_bad.play()
            if typed_num == len(question):
                sound_get_sashimi.play()
                question_init_flag = True
        
		# text rendering
        typed_text = question[:typed_num]
        remaining_text = question[typed_num:]
        typed_surface = font.render(typed_text, True, config.TYPED_COLOR)
        remaining_surface = font.render(remaining_text, True,config. REMAINING_COLOR)
        SURFACE.blit(typed_surface, [question_pos_x, question_pos_y])
        SURFACE.blit(remaining_surface, [question_pos_x + typed_surface.get_width(), question_pos_y])
        
		# yubi_key surface
        put_left_hand(SURFACE, font, left_hands_list, left_id)
        put_right_hand(SURFACE, font, right_hands_list, left_id, right_id)
        put_right_hands_list(SURFACE, font, right_hands_list, left_id)
        put_camera_frame(SURFACE, cam_frame)

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
