import pygame
import sys
import config
from utils import show_text

SCREEN_X = config.SCREEN_X
SCREEN_Y = config.SCREEN_Y


def get_player_name(screen):
    """获取玩家名字."""
    input_box_width = SCREEN_X // 2  # 输入框宽度
    input_box_height = 50  # 输入框高度
    input_box_x = (SCREEN_X - input_box_width) // 2  # 居中计算 x 坐标
    input_box_y = SCREEN_Y // 3  # 顶部 1/3 位置
    input_box = pygame.Rect(input_box_x, input_box_y, input_box_width, input_box_height)
    color_inactive = pygame.Color("lightskyblue3")
    color_active = pygame.Color("dodgerblue2")
    color = color_inactive
    active = True
    text = ""
    font = pygame.font.Font(config.FONT_PATH, 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((255, 255, 255))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        input_box.x = (SCREEN_X - width) // 2  # 动态调整输入框位置
        # Blit the text.
        text_x = input_box.x + (input_box.width - txt_surface.get_width()) // 2
        text_y = input_box.y + (input_box.height - txt_surface.get_height()) // 2
        screen.blit(txt_surface, (text_x, text_y))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)

        show_text(
            screen,
            0.5,  # 居中
            0.2,  # 顶部 20% 的位置
            "请输入你的名字:",
            (0, 0, 0),
            font_size_ratio=0.1,
            x_align="center",
            y_align="center",
            SCREEN_X=SCREEN_X,
            SCREEN_Y=SCREEN_Y,
        )

        pygame.display.flip()
        pygame.time.Clock().tick(config.FRAMERATE)
