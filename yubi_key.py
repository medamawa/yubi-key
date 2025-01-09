import cv2
from cv2 import aruco
import pygame
from pygame.locals import *
import sys
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
    left_hand = pu.resize_by_ratio(left_hand, 0.5)
    pu.put_middle(SURFACE, left_hand, 500, x_offset=-120)
    pu.put_middle(SURFACE, text, 750, x_offset=-120)


def put_right_hand(SURFACE, font, right_hands_list, right_id):
    right_hand = right_hands_list[right_id]
    right_hand = pu.resize_by_ratio(right_hand, 0.5)
    pu.put_middle(SURFACE, right_hand, 500, x_offset=120)
    

def yubi_key_surface(SURFACE, font, pygame_frame, cap, markers_info, selecting, output, left_hands_list, right_hands_list):
	SURFACE.fill(config.WHITE)
	
	# put frame (camera)
	pygame_frame = pu.resize_by_ratio(pygame_frame, 0.6)
	pu.put_middle(SURFACE, pygame_frame, 40)
    
	state_list = fu.get_state_list(markers_info)
	left_id = fu.get_left_id(state_list)
	right_id = fu.get_right_id(state_list)
	
	put_left_hand(SURFACE, font, left_hands_list, left_id)
	put_right_hand(SURFACE, font, right_hands_list, right_id)
    
	
	# event handling
	for event in pygame.event.get():
		# 閉じるボタンが押されたら終了させる
		if event.type == QUIT:
			cap.release()
			cv2.destroyAllWindows()
			pygame.quit()
			sys.exit()

		# キー入力
		if event.type == KEYDOWN:
			# ESCキーならtitleに戻る
			if event.key == K_ESCAPE:
				cap.release()
				cv2.destroyAllWindows()
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

        tmp, selecting = fu.get_output(markers_info, output)
        if tmp != "":
            output = tmp
        cv2.putText(frame, f"output: {output}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, f"selecting: {selecting}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # fps
        time_end = time.perf_counter()
        fps = 1.0 / (time_end - time_start)
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # convert frame into pygame image
        pygame_frame = pu.convert_opencv_img_to_pygame(frame)
        
        yubi_key_surface(SURFACE, font, pygame_frame, cap, markers_info, selecting, output, left_hands_list, right_hands_list)

    # リソースを解放
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
