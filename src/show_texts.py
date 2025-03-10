from utils import show_text
import pygame
import scores_rank
import config

SCREEN_X = config.SCREEN_X
SCREEN_Y = config.SCREEN_Y


def dead_texts(screen):
    show_text(
        screen,
        0.5,  # 居中
        0.4,  # 顶部 30% 的位置
        "YOU DEAD!",
        (227, 29, 18),
        font_size_ratio=0.16,  # 字体大小为屏幕高度的 10%
        # bold=True,
        x_align="center",
        y_align="center",
        SCREEN_X=SCREEN_X,
        SCREEN_Y=SCREEN_Y,
    )
    show_text(
        screen,
        0.5,  # 居中
        0.6,  # 顶部 50% 的位置
        "press space to try again...",
        (0, 0, 22),
        font_size_ratio=0.04,  # 字体大小为屏幕高度的 3%
        x_align="center",
        y_align="center",
        SCREEN_X=SCREEN_X,
        SCREEN_Y=SCREEN_Y,
    )


def show_leaderboard(screen):
    """显示排行榜."""
    scores = scores_rank.load_scores()
    # 使用 lambda 表达式对分数进行排序
    sorted_scores = sorted(scores, key=lambda item: item[1], reverse=True)
    top_5_scores = sorted_scores[:5]

    # 屏幕左上角起始位置
    # x_pos = 0.1 * SCREEN_X  # 屏幕宽度的 10%
    # y_pos = 0.1 * SCREEN_Y  # 屏幕高度的 10%
    # line_height = 0.05 * SCREEN_Y  # 每行的高度

    show_text(
        screen,
        0.1,
        0.1,
        "排行榜",
        (0, 0, 0),
        font_size_ratio=0.05,
        x_align="left",
        y_align="top",
        SCREEN_X=SCREEN_X,
        SCREEN_Y=SCREEN_Y,
    )

    # 使用 enumerate 和 zip 显示排行榜
    for i, (rank, (name, score)) in enumerate(
        zip(range(1, len(top_5_scores) + 1), top_5_scores)
    ):
        text = f"{rank}. {name}: {score}"
        # y = y_pos + i * line_height  # 计算每行的 y 坐标
        show_text(
            screen,
            0.1,
            0.125 + (i + 1) * 0.04,
            text,
            (0, 0, 0),
            font_size_ratio=0.03,
            x_align="left",
            y_align="top",
            SCREEN_X=SCREEN_X,
            SCREEN_Y=SCREEN_Y,
        )

    # pygame.display.update()


def running_texts(screen, scores, player_name, elapsed_time, direction_name):
    show_text(
        screen,
        0.1,  # 左侧 10% 的位置
        0.725,  # 底部 27.5% 的位置
        f"Max Score: {scores}",
        (223, 223, 223),
        font_size_ratio=0.05,  # 字体大小为屏幕高度的 3.75%
        x_align="left",
        y_align="center",
        SCREEN_X=SCREEN_X,
        SCREEN_Y=SCREEN_Y,
    )
    show_text(
        screen,
        0.1,  # 左侧 10% 的位置
        0.8,  # 底部 20% 的位置
        f"{player_name}的Score: " + str(scores),
        (223, 223, 223),
        font_size_ratio=0.05,  # 字体大小为屏幕高度的 3.75%
        x_align="left",
        y_align="center",
        SCREEN_X=SCREEN_X,
        SCREEN_Y=SCREEN_Y,
    )
    show_text(
        screen,
        0.1,  # 左侧 10% 的位置
        0.875,  # 底部 12.5% 的位置
        "时间: " + str(int(elapsed_time)),
        (223, 223, 223),
        font_size_ratio=0.05,  # 字体大小为屏幕高度的 3.75%
        x_align="left",
        y_align="center",
        SCREEN_X=SCREEN_X,
        SCREEN_Y=SCREEN_Y,
    )

    show_text(
        screen,
        0.95,  # 右侧 20% 的位置
        0.1,  # 顶部 10% 的位置
        "按键记录: " + direction_name,
        (0, 0, 0),
        font_size_ratio=0.05,  # 字体大小为屏幕高度的 2.5%
        x_align="right",
        y_align="center",
        SCREEN_X=SCREEN_X,
        SCREEN_Y=SCREEN_Y,
    )
