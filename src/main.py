import pygame
import sys
import time
from snake import Snake
from food import Food
from utils import show_text
from powerup import PowerUp
from player_info import get_player_name
import show_texts
import scores_rank
import config

# 全局定义
SCREEN_X = config.SCREEN_X
SCREEN_Y = config.SCREEN_Y


def main():
    pygame.init()
    screen_size = (SCREEN_X, SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(config.PROGRAM_NAME)
    icon = pygame.image.load(config.ICON_PATH)
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    scores = 0
    isdead = False

    elapsed_time = 0

    file_score = scores_rank.get_max_score()
    # 蛇/食物
    snake = Snake()
    food = Food(SCREEN_X, SCREEN_Y)
    power_up = PowerUp(food)  # 传入 Food 对象
    power_up.set(snake.body)  # 初始设置 PowerUp 位置
    last_direction_input = None  # 存储上次有效的方向输入
    start_time = time.time()

    player_name = get_player_name(screen)
    if not player_name:
        return  # 如果没有输入名字，退出游戏
    once_flag = True
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                LR = [pygame.K_LEFT, pygame.K_RIGHT]
                UD = [pygame.K_UP, pygame.K_DOWN]
                if event.key in LR + UD:
                    if snake.next_direction is None:  # 只记录第一次按键
                        snake.next_direction = event.key
                        last_direction_input = event.key  # 记录按键
                # 死后按space重新
                if event.key == pygame.K_SPACE and isdead:
                    return main()

        screen.fill((255, 255, 255))

        # 画蛇身 / 每一步+1分
        if not isdead:
            if snake.move():  # 如果蛇成功移动
                scores += 1

        for rect in snake.body:
            pygame.draw.rect(screen, (20, 220, 39), rect, 0)

        # 显示死亡文字
        isdead = snake.isdead(SCREEN_X, SCREEN_Y)
        if isdead:
            if once_flag:
                scores_rank.save_score(player_name, scores)
                once_flag = False
            show_texts.dead_texts(screen)
            show_texts.show_leaderboard(screen)

        # 食物处理 / 吃到+50分
        # 当食物rect与蛇头重合,吃掉 -> Snake增加一个Node
        if food.rect == snake.body[0]:
            scores += food.score_increase
            food.remove()
            snake.addnode()

        # 食物投递
        food.set()
        pygame.draw.rect(screen, (136, 0, 21), food.rect, 0)

        if not isdead:
            power_up.move(snake.body)  # 移动 PowerUp
        power_up.draw(screen)
        # 蛇吃到 PowerUp 的检测
        if power_up.rect == snake.body[0]:
            scores += power_up.score_increase
            snake.change_speed()
            power_up.set(snake.body)  # 重新设置 PowerUp 位置
            power_up.reset_move_time()
            speed_change_time = time.time()  # 记录速度改变的时间

        if (
            "speed_change_time" in locals()
            and time.time() - speed_change_time > config.SPEEDUP_INTERVAL
        ):
            snake.recover_speed()  # 恢复蛇的速度
            del speed_change_time  # 删除 speed_change_time 变量

        if not isdead:
            elapsed_time = time.time() - start_time
            direction_name = snake.get_direction_name(last_direction_input)

        max_score = scores
        if max_score < file_score:
            max_score = file_score
        show_texts.running_texts(
            screen, scores, max_score, player_name, elapsed_time, direction_name
        )

        pygame.display.update()
        clock.tick(config.FRAMERATE)


if __name__ == "__main__":
    main()
