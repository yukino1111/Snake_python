import pygame
import config

def show_text(
    screen,
    x_ratio,
    y_ratio,
    text,
    color,
    font_size_ratio=0.05,  # 字体大小相对于屏幕高度的比例
    bold=False,
    italic=False,
    antialias=True,
    x_align="center",  # 水平对齐方式：left, center, right
    y_align="center",  # 垂直对齐方式：top, center, bottom
    SCREEN_X=1200,
    SCREEN_Y=700,
):
    """
    在屏幕上显示文字，支持不同分辨率和对齐方式。

    Args:
        screen: pygame 的屏幕对象。
        x_ratio: 文字中心 X 坐标相对于屏幕宽度的比例。
        y_ratio: 文字中心 Y 坐标相对于屏幕高度的比例。
        text: 要显示的文字内容。
        color: 文字颜色。
        font_name: 字体文件路径。
        font_size_ratio: 字体大小相对于屏幕高度的比例。
        bold: 是否加粗。
        italic: 是否斜体。
        antialias: 是否抗锯齿。
        x_align: 水平对齐方式，可选值：left, center, right。
        y_align: 垂直对齐方式，可选值：top, center, bottom。
        SCREEN_X: 屏幕宽度。
        SCREEN_Y: 屏幕高度。
    """

    # 计算字体大小
    min_pos=min(SCREEN_X, SCREEN_Y)
    font_size = int(min_pos * font_size_ratio)

    # 创建字体对象
    font = pygame.font.Font(config.FONT_PATH, font_size)

    # 设置字体样式
    font.set_bold(bold)
    font.set_italic(italic)

    # 渲染文字
    text_surface = font.render(text, antialias, color)
    text_rect = text_surface.get_rect()

    # 计算文字位置
    x = int(SCREEN_X * x_ratio)
    y = int(SCREEN_Y * y_ratio)

    # 水平对齐
    if x_align == "center":
        x -= text_rect.width // 2
    elif x_align == "right":
        x -= text_rect.width

    # 垂直对齐
    if y_align == "center":
        y -= text_rect.height // 2
    elif y_align == "bottom":
        y -= text_rect.height

    # 绘制文字
    screen.blit(text_surface, (x, y))
