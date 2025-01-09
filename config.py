import pygame

# sashimida

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

# title

SASHIMI_MARGIN = 350
TITLE_RAIL_SPEED = 1

# button

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=BLACK, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, screen):
        # マウス座標を取得
        mouse_pos = pygame.mouse.get_pos()

        # ボタンの色を切り替え
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        # ボタンのテキストを描画
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # マウスクリックイベントかつボタン領域内かを確認
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
