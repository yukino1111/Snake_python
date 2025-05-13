import pygame
import sys
import time
from snake import Snake
from food import Food
from powerup import PowerUp
import scores_rank
import config
from interface import (
    MainMenu,
    DeathMenu,
    PauseMenu,
    Interface,
    NameInputMenu,
    LeaderboardMenu,
    AboutMenu,
    QuitMenu,
)  # 导入界面类

# 全局定义
SCREEN_X = config.SCREEN_X
SCREEN_Y = config.SCREEN_Y


# 游戏状态管理类
class GameState:
    def __init__(self):
        # 分数和状态
        self.scores = 0
        self.isdead = False
        self.cheat_flag = 0
        self.file_score = 0

        # 游戏对象
        self.snake = None
        self.food = None
        self.power_up = None  # 多态: PowerUp与Food将展示不同的行为

        # 时间相关
        self.start_time = 0
        self.elapsed_time = 0
        self.pause_start_time = -1
        self.pause_finish_time = -1
        self.total_pause_time = -1
        self.speed_change_time = -1

        # 控制标志
        self.last_direction_input = None
        self.once_flag = True
        self.paused = False

    def reset(self):
        """重置游戏状态"""
        # 分数和状态重置
        self.scores = 0
        self.isdead = False
        self.cheat_flag = 0
        self.file_score = scores_rank.get_max_score()

        # 重新创建游戏对象
        self.snake = Snake()
        self.food = Food(SCREEN_X, SCREEN_Y)  # 基类实例
        self.power_up = PowerUp(SCREEN_X, SCREEN_Y)  # 多态: 派生类实例，可替代基类位置
        self.power_up.set(self.snake.body)  # 多态: 调用重写的set方法，参数不同于Food类

        # 时间相关重置
        self.start_time = time.time()
        self.elapsed_time = 0
        self.pause_start_time = -1
        self.pause_finish_time = -1
        self.total_pause_time = -1
        self.speed_change_time = -1

        # 控制标志重置
        self.last_direction_input = None
        self.once_flag = True
        self.paused = False


def main():
    pygame.init()
    screen_size = (SCREEN_X, SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(config.PROGRAM_NAME)
    icon = pygame.image.load(config.ICON_PATH)
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    clock.tick(config.FRAMERATE)

    # 创建各种菜单
    main_menu = MainMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    death_menu = DeathMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    pause_menu = PauseMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    interface = Interface(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    name_input_menu = NameInputMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    leaderboard_menu = LeaderboardMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    about_menu = AboutMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    quit_menu = QuitMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)

    player_name = ""  # 默认玩家名字
    ProgramRunning = True
    game_state = GameState()  # 创建游戏状态管理器

    while ProgramRunning:
        menu_choice = main_menu.run()
        # print(menu_choice)
        if menu_choice == "start":
            # 获取玩家名字
            name_choice = name_input_menu.run()
            if name_choice == "" or name_choice == None:
                continue  # 返回主菜单
            else:
                player_name = name_choice

            game_state.reset()  # 初始化游戏状态

            running = True
            while running:  # 游戏主循环
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        ProgramRunning = False
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # 按下 Esc 键
                            game_state.paused = True
                            clock.tick(1)  # 降低帧率，减少 CPU 占用
                            game_state.pause_start_time = time.time()
                            pause_choice = pause_menu.run()  # 显示暂停菜单

                            if pause_choice == "continue":
                                game_state.paused = False  # 继续游戏
                                game_state.pause_finish_time = time.time()
                                game_state.total_pause_time = (
                                    game_state.pause_finish_time
                                    - game_state.pause_start_time
                                )
                                game_state.start_time += game_state.total_pause_time
                                game_state.speed_change_time += (
                                    game_state.total_pause_time
                                )
                                game_state.power_up.reset_move_time(
                                    game_state.total_pause_time
                                )
                                clock.tick(config.FRAMERATE)  # 恢复正常帧率
                            elif pause_choice == "restart":
                                game_state.reset()  # 重新初始化游戏
                                continue
                            elif pause_choice == "mainmenu":
                                running = False
                                break
                            elif pause_choice == "quit":
                                quit_choice = quit_menu.run()
                                if quit_choice == "continue":
                                    game_state.paused = False  # 返回暂停菜单
                                    clock.tick(config.FRAMERATE)
                                    game_state.pause_finish_time = time.time()
                                    game_state.total_pause_time = (
                                        game_state.pause_finish_time
                                        - game_state.pause_start_time
                                    )
                                    game_state.start_time += game_state.total_pause_time
                                    game_state.speed_change_time += (
                                        game_state.total_pause_time
                                    )
                                    game_state.power_up.reset_move_time(
                                        game_state.total_pause_time
                                    )
                                else:
                                    running = False
                                    ProgramRunning = False
                                    break
                        if not game_state.paused:  # 只有在未暂停时才处理方向键和作弊键
                            LR = [pygame.K_LEFT, pygame.K_RIGHT]
                            UD = [pygame.K_UP, pygame.K_DOWN]
                            if event.key in LR + UD:
                                if game_state.snake.next_direction is None:
                                    game_state.snake.next_direction = event.key
                                    game_state.last_direction_input = event.key
                            if event.key == pygame.K_k:
                                game_state.cheat_flag = 1 - game_state.cheat_flag
                if running == False:
                    break

                screen.fill((240, 240, 240))
                if not game_state.paused:
                    if game_state.cheat_flag == 1:
                        food_position = pygame.math.Vector2(
                            game_state.power_up.rect.center
                        )
                        if game_state.snake.move(food_position):
                            game_state.scores += 1
                    else:
                        if game_state.snake.move():
                            game_state.scores += 1

                    for rect in game_state.snake.body:
                        pygame.draw.rect(screen, (20, 220, 39), rect, 0)

                    game_state.isdead = game_state.snake.isdead(SCREEN_X, SCREEN_Y)

                    if game_state.food.rect == game_state.snake.body[0]:
                        game_state.scores += (
                            game_state.food.score_increase
                        )  # 多态: 使用各自的score_increase属性
                        game_state.food.remove()
                        game_state.snake.addnode(0)

                    game_state.food.set()  # 多态: Food类的set不需要参数
                    pygame.draw.rect(
                        screen, (136, 0, 21), game_state.food.rect, 0
                    )  # 显式绘制

                    if not game_state.isdead:
                        game_state.power_up.move(
                            game_state.snake.body
                        )  # 多态: PowerUp特有的方法
                    game_state.power_up.draw(
                        screen
                    )  # 多态: PowerUp使用自己的draw方法，颜色不同

                    if game_state.power_up.rect == game_state.snake.body[0]:
                        game_state.scores += (
                            game_state.power_up.score_increase
                        )  # 多态: 不同的得分增加
                        game_state.snake.addnode(0)
                        game_state.snake.change_speed()
                        game_state.power_up.set(game_state.snake.body)  # 多态: 参数不同
                        game_state.power_up.reset_move_time()  # 多态: PowerUp特有方法
                        game_state.speed_change_time = time.time()

                    if (
                        time.time() - game_state.speed_change_time
                        > config.SPEEDUP_INTERVAL
                        and game_state.speed_change_time != -1
                    ):
                        game_state.snake.recover_speed()
                        game_state.speed_change_time = -1

                    if not game_state.isdead:
                        game_state.elapsed_time = time.time() - game_state.start_time
                        direction_name = game_state.snake.get_direction_name(
                            game_state.last_direction_input
                        )

                    interface.show_running_info(
                        game_state.scores,
                        game_state.file_score,
                        player_name,
                        game_state.elapsed_time,
                        direction_name,
                    )  # 使用Interface显示信息
                    if game_state.isdead:
                        if not running:
                            break  # 退出游戏
                        if game_state.once_flag:
                            scores_rank.save_score(player_name, game_state.scores)
                            game_state.once_flag = False
                        death_choice = death_menu.run(game_state.scores)

                        if death_choice == "restart":
                            game_state.reset()
                            continue  # 重新开始游戏
                        elif death_choice == "leaderboard":
                            scores = scores_rank.get_leaderboard()
                            leaderboard_menu.run(scores)
                            break
                        elif death_choice == "mainmenu":
                            break  # 返回主菜单
                        elif death_choice == "quit":
                            quit_choice = quit_menu.run()
                            if quit_choice == "continue":
                                continue  # 返回死亡菜单
                            else:
                                running = False
                                ProgramRunning = False
                                break
                    pygame.display.update()
            if ProgramRunning == False:
                break
            # 游戏结束，显示死亡菜单

        elif menu_choice == "leaderboard":
            scores = scores_rank.get_leaderboard()
            leaderboard_choice = leaderboard_menu.run(scores)
            if leaderboard_choice == "mainmenu":
                continue  # 返回主菜单
        elif menu_choice == "about":
            about_choice = about_menu.run()
            if about_choice == "mainmenu":
                continue  # 返回主菜单
        elif menu_choice == "quit":
            quit_choice = quit_menu.run()
            if quit_choice == "continue":
                continue  # 返回主菜单
            else:
                break  # 退出游戏

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
