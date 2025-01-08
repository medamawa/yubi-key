import pygame
from pygame.locals import *
import sys
import datetime

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

def main():
    # initialization
    pygame.init()
    SURFACE = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(TITLE)
    font = pygame.font.Font(FONT_FILE, FONT_SIZE)
    rail_x = 45

    # load images
    background = pygame.image.load("./srcs/sashimida/background.png")
    rail = pygame.image.load("./srcs/sashimida/rail.png")
    frame = pygame.image.load("./srcs/sashimida/frame.png")
    bg_width, bg_height = background.get_size()
    rail_width, rail_height = rail.get_size()
    frame_width, frame_height = frame.get_size()
    ratio = WINDOW_WIDTH / frame_width

    # resize images
    background = pygame.transform.scale(background, (int(bg_width * ratio), int(bg_height * ratio)))
    rail = pygame.transform.scale(rail, (int(rail_width * ratio), int(rail_height * ratio)))
    frame = pygame.transform.scale(frame, (int(frame_width * ratio), int(frame_height * ratio)))


    questions_list = read_file_lines("./srcs/questions.txt")
    question_init_flag = True

    # main loop
    while True:
        # SURFACE.fill(GRAY)
        SURFACE.blit(background, (45, 130))
        rail_x += RAIL_SPEED
        if rail_x > 45 + rail_width * ratio:
            rail_x = 45
        SURFACE.blit(rail, (rail_x, 300))
        SURFACE.blit(rail, (rail_x - rail_width * ratio, 300))
        SURFACE.blit(frame, (0, 0))

        # initialize question
        if question_init_flag:
            question = questions_list.pop(0)
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
                        typed_num += 1
                    if typed_num == len(question):
                        question_init_flag = True
            
        typed_text = question[:typed_num]
        remaining_text = question[typed_num:]
        typed_surface = font.render(typed_text, True, TYPED_COLOR)
        remaining_surface = font.render(remaining_text, True, REMAINING_COLOR)
        SURFACE.blit(typed_surface, [question_pos_x, question_pos_y])
        SURFACE.blit(remaining_surface, [question_pos_x + typed_surface.get_width(), question_pos_y])
        
        # date = font.render(question, True, (100, 0, 100))
        # 時刻 = font.render(datetime.datetime.now().strftime("%H:%M:%S"), True, (0, 0, 100))
        # SURFACE.blit(date, [80, 90])
        # SURFACE.blit(時刻, [100, 150])
        
        # 画面更新
        pygame.display.update()

if __name__ == '__main__':
    main()