import pygame
from pygame.locals import *
import sys
import random

# configuration
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 832
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
TITLE = "sashimida"
FONT_FILE = "./srcs/NikkyouSans.ttf"
FONT_SIZE = 40
RAIL_SPEED = 2

WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
TYPED_COLOR = (238, 120, 0)
REMAINING_COLOR = (255, 255, 255)

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

def get_key_input(pygame, event):
    shift_mapping = {
    '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
    '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
    '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|',
    ';': ':', "'": '"', ',': '<', '.': '>', '/': '?'
    }

    if event.key == K_SPACE:
        return '_'

    if pygame.key.get_mods() & KMOD_SHIFT:
        if pygame.key.name(event.key) in shift_mapping:
            return shift_mapping[pygame.key.name(event.key)]
    return pygame.key.name(event.key)

def load_images():
    # load images
    background = pygame.image.load("./srcs/sashimida/background.png")
    rail = pygame.image.load("./srcs/sashimida/rail.png")
    frame = pygame.image.load("./srcs/sashimida/frame.png")
    sashimi_list = []
    for i in range(1, 9):
        sashimi_list.append(pygame.image.load(f"./srcs/sashimida/sashimi{i}.png"))
    bg_width, bg_height = background.get_size()
    rail_width, rail_height = rail.get_size()
    frame_width, frame_height = frame.get_size()
    sashimi_width, sashimi_height = sashimi_list[0].get_size()
    ratio = WINDOW_WIDTH / frame_width

    # resize images
    background = pygame.transform.scale(background, (int(bg_width * ratio), int(bg_height * ratio)))
    rail = pygame.transform.scale(rail, (int(rail_width * ratio), int(rail_height * ratio)))
    frame = pygame.transform.scale(frame, (int(frame_width * ratio), int(frame_height * ratio)))
    for i in range(8):
        sashimi_list[i] = pygame.transform.scale(sashimi_list[i], (int(sashimi_width * ratio), int(sashimi_height * ratio)))
    
    return background, rail, frame, sashimi_list

def main():
    # initialization
    pygame.init()
    SURFACE = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(TITLE)
    font = pygame.font.Font(FONT_FILE, FONT_SIZE)

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

    # main loop
    while True:
        # SURFACE.fill(GRAY)
        SURFACE.blit(background, (45, 130))
        rail_x += RAIL_SPEED
        if rail_x > 45 + rail_width:
            rail_x = 45
        SURFACE.blit(rail, (rail_x, 300))
        SURFACE.blit(rail, (rail_x - rail_width, 300))

        # initialize question
        if question_init_flag:
            question = random.choice(questions_list)
            question = question.lower().replace(" ", "_")
            question_width = font.size(question)[0]
            question_pos_x = (WINDOW_WIDTH - question_width) // 2
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
                # ESCキーなら終了
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    if get_key_input(pygame, event) == question[typed_num]:
                        sound_typing_good.play()
                        typed_num += 1
                    elif not pygame.key.get_mods() & KMOD_SHIFT:
                        sounf_typing_bad.play()
                    if typed_num == len(question):
                        sound_get_sashimi.play()
                        question_init_flag = True
            
        typed_text = question[:typed_num]
        remaining_text = question[typed_num:]
        typed_surface = font.render(typed_text, True, TYPED_COLOR)
        remaining_surface = font.render(remaining_text, True, REMAINING_COLOR)
        SURFACE.blit(typed_surface, [question_pos_x, question_pos_y])
        SURFACE.blit(remaining_surface, [question_pos_x + typed_surface.get_width(), question_pos_y])

        # sashimi
        sashimi_x += RAIL_SPEED
        if sashimi_x > 45 + rail_width + 10 or question_init_flag:
            question_init_flag = True
            tmp = random.choice(sashimi_list)
            while tmp == sashimi:
                tmp = random.choice(sashimi_list)
            sashimi = tmp
            sashimi_x = 45 - sashimi_width
        SURFACE.blit(sashimi, (sashimi_x, 230))
        
        # refresh window
        SURFACE.blit(frame, (0, 0))
        pygame.display.update()

if __name__ == '__main__':
    main()