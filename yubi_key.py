import cv2
from cv2 import aruco
import pygame
from pygame.locals import *
import sys
import time

import config
from utils import finger_utils as fu
from utils import marker_utils as mu
from utils import pygame_utils as pu

def put_left_hand(SURFACE, font, left_hands_list, left_id):
    if left_id == 2 or left_id == 3:
        left_hand = left_hands_list[left_id]
        text = font.render(f"layer{left_id}", True, config.BLACK)
    else:
        left_hand = left_hands_list[0]
        text = font.render("layer1", True, config.BLACK)
    left_hand = pu.resize_by_ratio(left_hand, 0.5)

    pu.put_middle(SURFACE, left_hand, 520, x_offset=-110)
    pu.put_middle(SURFACE, text, 770, x_offset=-110)

def put_right_hand(SURFACE, font, right_hands_list, left_id, right_id):
    right_hand = right_hands_list[right_id]
    right_hand = pu.resize_by_ratio(right_hand, 0.5)

    char = fu.get_selecting_key(left_id, right_id)
    if char == " ":
        char = "_"
    elif char == "\n":
        char = "\\n"
    text = font.render(char, True, config.BLACK)

    pu.put_middle(SURFACE, right_hand, 520, x_offset=110)
    pu.put_middle(SURFACE, text, 770, x_offset=110)

def put_right_hands_list(SURFACE, font, right_hands_list, left_id):
    for i in range (1, 6):
        right_hand = right_hands_list[i]
        right_hand = pu.resize_by_ratio(right_hand, 0.15)

        char = fu.get_selecting_key(left_id, i)
        if char == " ":
            char = "[space]"
        text = font.render(char, True, config.BLACK)

        pu.put_middle(SURFACE, right_hand, 530, x_offset=190 + 62 * i)
        pu.put_middle(SURFACE, text, 600, x_offset=193 + 62 * i)
    
    for i in range (6, 12):
        right_hand = right_hands_list[i]
        right_hand = pu.resize_by_ratio(right_hand, 0.15)

        char = fu.get_selecting_key(left_id, i)
        if char == " ":
            char = "_"
        elif char == "\n":
            char = "\\n"
        text = font.render(char, True, config.BLACK)

        pu.put_middle(SURFACE, right_hand, 660, x_offset=190 + 62 * (i - 5))
        pu.put_middle(SURFACE, text, 730, x_offset=193 + 62 * (i - 5))

def put_output(SURFACE, font, sub_font, output):
    sub_text = sub_font.render("output", True, config.BLACK)
    pu.put_middle(SURFACE, sub_text, 520, x_offset=-400)

    # 14文字ごとに改行
    words = output.split()
    texts_list = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + (1 if current_line else 0) <= 14:
            current_line += (" " if current_line else "") + word
        else:
            texts_list.append(current_line)
            current_line = word

    # 最後の行を追加
    if current_line:
        if output[-1] == " ":
            texts_list.append(current_line + " _")
        else:
            texts_list.append(current_line + "_")
    
    if len(texts_list) > 5:
        text = font.render("...", True, config.BLACK)
        pu.put_middle(SURFACE, text, 545, x_offset=-400)

        for i in range(-5, 0):
            text = font.render(texts_list[i], True, config.BLACK)
            pu.put_middle(SURFACE, text, 545 + 40 * (i + 6), x_offset=-400)
    else:
        for i in range(len(texts_list)):
            text = font.render(texts_list[i], True, config.BLACK)
            pu.put_middle(SURFACE, text, 565 + 40 * i, x_offset=-400)

def put_key_table(SURFACE, sub_font):
    for i in range(1, 4):
        for j in range(1, 6):
            char = fu.get_selecting_key(i, j)
            text = sub_font.render(char, True, config.BLACK)
            pu.put_middle(SURFACE, text, 100 + 100 * i, x_offset=410 + 32 * j)
        
        for j in range(6, 12):
            char = fu.get_selecting_key(i, j)
            if char == " ":
                char = "_"
            elif char == "\n":
                char = "\\n"
            text = sub_font.render(char, True, config.BLACK)
            pu.put_middle(SURFACE, text, 135 + 100 * i, x_offset=410 + 32 * (j - 5))

def yubi_key_surface(SURFACE, font, sub_font, pygame_frame, cap, markers_info, output, left_hands_list, right_hands_list):
	SURFACE.fill(config.WHITE)
	
	# put frame (camera)
	pygame_frame = pu.resize_by_ratio(pygame_frame, 0.65)
	pu.put_middle(SURFACE, pygame_frame, 30)
    
	state_list = fu.get_state_list(markers_info)
	left_id = fu.get_left_id(state_list)
	right_id = fu.get_right_id(state_list)
	
	put_left_hand(SURFACE, font, left_hands_list, left_id)
	put_right_hand(SURFACE, font, right_hands_list, left_id, right_id)
	put_right_hands_list(SURFACE, font, right_hands_list, left_id)
	put_output(SURFACE, font, sub_font, output)
	put_key_table(SURFACE, sub_font)
    
	# event handling
	for event in pygame.event.get():
		# 閉じるボタンが押されたら終了させる
		if event.type == QUIT:
			cap.release()
			pygame.quit()
			sys.exit()

		# キー入力
		if event.type == KEYDOWN:
			# ESCキーならtitleに戻る
			if event.key == K_ESCAPE:
				cap.release()
				pygame.quit()
				sys.exit()
	
	# refresh window
	pygame.display.flip()

def load_images():
	left_hands_file = [f'./srcs/hand_images/left{i}.png' for i in range(5)]
	right_hands_file = [f'./srcs/hand_images/right{i}.png' for i in range(12)]
	left_hands_list = []
	right_hands_list = []
	for file in left_hands_file:
		left_hands_list.append(pygame.image.load(file))
	for file in right_hands_file:
		right_hands_list.append(pygame.image.load(file))

	return left_hands_list, right_hands_list


def main():
    # pygame setup
    pygame.init()
    SURFACE = pygame.display.set_mode(config.WINDOW_SIZE)
    pygame.display.set_caption(config.YUBI_KEY_TITLE)
    font = pygame.font.Font(config.FONT_FILE, config.FONT_SIZE)
    sub_font = pygame.font.Font(config.FONT_FILE, config.SUB_FONT_SIZE)
    
	# images
    left_hands_list, right_hands_list = load_images()

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

    # yubi_key output
    output = ""

    while True:
        time_start = time.perf_counter()

        # get frame
        ret, frame = cap.read()
        if not ret:
            break

        # convert to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect markers
        corners, ids, _ = detector.detectMarkers(gray)

        # マーカーを検出した場合
        if ids is not None:
            mu.get_markers_info(markers_info, corners, ids)
            for marker_id, info in markers_info.items():
                if not info["detected"]:
                    continue
                center_x, center_y = info["center"]
                size = info["size"]
                
                # 中心座標を描画(stateによって色を変える)0
                if (info["state"]):
                    cv2.circle(frame, (center_x, center_y), 15, (0, 255, 0), -1)
                else:
                    cv2.circle(frame, (center_x, center_y), 15, (0, 0, 255), -1)

        # flip frame
        frame = cv2.flip(frame, 1)

        # get output
        output, _ = fu.get_output(markers_info, output)

        # fps
        time_end = time.perf_counter()
        fps = 1.0 / (time_end - time_start)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # convert frame into pygame image
        pygame_frame = pu.convert_opencv_img_to_pygame(frame)
        
        yubi_key_surface(SURFACE, font, sub_font, pygame_frame, cap, markers_info, output, left_hands_list, right_hands_list)

    # リソースを解放
    cap.release()

if __name__ == '__main__':
    main()
