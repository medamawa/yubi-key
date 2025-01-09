import pygame

import config

class Button:
    def __init__(self, x, y, width, height, text, color=config.WHITE, hover_color=config.GRAY, text_color=config.BLACK, outline_color=config.BROWN, outline_width=5, alpha=150):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        self.alpha = alpha
        
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.hover_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        self.surface.fill((*color, alpha))
        self.hover_surface.fill((*color, 240))

        self.hover_flag = False

    def draw(self, SURFACE, font):
        # sounds
        sound_hover = pygame.mixer.Sound("./srcs/sashimida/hover.wav")

        # マウス座標を取得
        mouse_pos = pygame.mouse.get_pos()

        # ボタンの色を切り替え
        if self.rect.collidepoint(mouse_pos):
            SURFACE.blit(self.hover_surface, self.rect)
            if not self.hover_flag:
                sound_hover.play()
                self.hover_flag = True
        else:
            SURFACE.blit(self.surface, self.rect)
            self.hover_flag = False
        
        pygame.draw.rect(SURFACE, self.outline_color, self.rect, self.outline_width)


        # ボタンのテキストを描画
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        SURFACE.blit(text_surface, text_rect)

    def is_clicked(self, event):
        # マウスクリックイベントかつボタン領域内かを確認
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
