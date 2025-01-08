import pygame
from pygame.locals import *
import sys
import datetime

# pygame初期化
pygame.init()
SURFACE = pygame.display.set_mode((1280, 720))    # サイズを指定して画面を作成
pygame.display.set_caption("sashimida")    # タイトル文字を指定
font = pygame.font.Font("NikkyouSans.ttf", 60)               # フォントの設定(60px)

# メイン関数
def main():
    # 表示更新ループ
    while True:
        SURFACE.fill((0,100,0))          # 背景（壁）を緑色で塗りつぶす
        日付 = font.render(str(datetime.date.today()), True, (100, 0, 100))
        時刻 = font.render(datetime.datetime.now().strftime("%H:%M:%S"), True, (0, 0, 100))
        SURFACE.blit(日付, [80, 90])    # 文字列の位置を指定
        SURFACE.blit(時刻, [100, 150])    # 文字列の位置を指定
        pygame.display.update()            # 画面更新
        # イベントを処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()       # Pygameの終了（画面を閉じる）
                sys.exit()          # プログラムの終了

if __name__ == '__main__':
    main()