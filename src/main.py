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


def main():
    pygame.init()
    screen_size = (SCREEN_X, SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(config.PROGRAM_NAME)
    icon = pygame.image.load(config.ICON_PATH)
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    clock.tick(config.FRAMERATE)
    main_menu = MainMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    death_menu = DeathMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    pause_menu = PauseMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)  # 创建暂停菜单
    interface = Interface(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)  # 创建Interface对象
    name_input_menu = NameInputMenu(
        SCREEN_X, SCREEN_Y, config.PROGRAM_NAME
    )  # 创建名字输入菜单
    leaderboard_menu = LeaderboardMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    about_menu = AboutMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)
    quit_menu = QuitMenu(SCREEN_X, SCREEN_Y, config.PROGRAM_NAME)

    player_name = ""  # 默认玩家名字
    file_score = 0  # 默认最高分
    ProgramRunning = True

    while ProgramRunning:
        menu_choice = main_menu.run()
        # print(menu_choice)
        if menu_choice == "start":
            # 获取玩家名字
            name_choice = name_input_menu.run()
            if name_choice == "" or name_choice == None:
                # name_choice == ""
                continue  # 返回主菜单
            else:
                player_name = name_choice
            scores = 0
            isdead = False
            elapsed_time = 0
            cheat_flag = 0
            file_score = scores_rank.get_max_score()  # 获取最高分
            snake = Snake()  # 在这里定义 snake 变量
            food = Food(SCREEN_X, SCREEN_Y)
            power_up = PowerUp(food)
            power_up.set(snake.body)
            last_direction_input = None
            start_time = time.time()
            once_flag = True
            paused = False
            pause_start_time = -1
            pause_finish_time = -1
            total_pause_time = -1
            speed_change_time = -1

            def init_game():
                nonlocal scores, isdead, elapsed_time, cheat_flag, food, snake, power_up, last_direction_input, start_time, once_flag, paused, pause_start_time, pause_finish_time, total_pause_time, speed_change_time
                scores = 0
                isdead = False
                elapsed_time = 0
                cheat_flag = 0
                file_score = scores_rank.get_max_score()  # 获取最高分
                snake = Snake()
                food = Food(SCREEN_X, SCREEN_Y)
                power_up = PowerUp(food)
                power_up.set(snake.body)
                last_direction_input = None
                start_time = time.time()
                once_flag = True
                paused = False
                pause_start_time = -1
                pause_finish_time = -1
                total_pause_time = -1
                speed_change_time = -1

            init_game()  # 初始化游戏
            running = True
            while running:  # 游戏主循环
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        ProgramRunning = False
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:  # 按下 Esc 键
                            paused = True
                            clock.tick(1)  # 降低帧率，减少 CPU 占用
                            pause_start_time = time.time()
                            pause_choice = pause_menu.run()  # 显示暂停菜单

                            if pause_choice == "continue":
                                paused = False  # 继续游戏
                                pause_finish_time = time.time()
                                total_pause_time = pause_finish_time - pause_start_time
                                start_time += total_pause_time
                                speed_change_time += total_pause_time
                                power_up.reset_move_time(total_pause_time)
                                clock.tick(config.FRAMERATE)  # 降低帧率，减少 CPU 占用
                            elif pause_choice == "restart":
                                init_game()  # 重新初始化游戏
                                continue
                            elif pause_choice == "mainmenu":
                                # isdead = True  # 强制结束游戏循环，返回主菜单
                                running = False
                                break
                            elif pause_choice == "quit":
                                quit_choice = quit_menu.run()
                                if quit_choice == "continue":
                                    paused = False  # 返回暂停菜单
                                    clock.tick(
                                        config.FRAMERATE
                                    )  # 降低帧率，减少 CPU 占用
                                    pause_finish_time = time.time()
                                    total_pause_time = (
                                        pause_finish_time - pause_start_time
                                    )
                                    start_time += total_pause_time
                                    speed_change_time += total_pause_time
                                    power_up.reset_move_time(total_pause_time)
                                    # continue
                                else:
                                    running = False
                                    ProgramRunning = False
                                    break
                        if not paused:  # 只有在未暂停时才处理方向键和作弊键
                            LR = [pygame.K_LEFT, pygame.K_RIGHT]
                            UD = [pygame.K_UP, pygame.K_DOWN]
                            if event.key in LR + UD:
                                if snake.next_direction is None:
                                    snake.next_direction = event.key
                                    last_direction_input = event.key
                            if event.key == pygame.K_k:
                                cheat_flag = 1 - cheat_flag
                if running == False:
                    break
                # if paused:  # 如果游戏暂停
                #     continue  # 跳过游戏逻辑，进入下一轮循环

                screen.fill((240, 240, 240))
                if not paused:
                    if cheat_flag == 1:
                        food_position = pygame.math.Vector2(power_up.rect.center)
                        if snake.move(food_position):
                            scores += 1
                    else:
                        if snake.move():
                            scores += 1

                    for rect in snake.body:
                        pygame.draw.rect(screen, (20, 220, 39), rect, 0)

                    isdead = snake.isdead(SCREEN_X, SCREEN_Y)

                    if food.rect == snake.body[0]:
                        scores += food.score_increase
                        food.remove()
                        snake.addnode(0)

                    food.set()
                    pygame.draw.rect(screen, (136, 0, 21), food.rect, 0)

                    if not isdead:
                        power_up.move(snake.body)
                    power_up.draw(screen)

                    if power_up.rect == snake.body[0]:
                        scores += power_up.score_increase
                        snake.addnode(0)
                        snake.change_speed()
                        power_up.set(snake.body)
                        power_up.reset_move_time()
                        speed_change_time = time.time()

                    if (
                        time.time() - speed_change_time > config.SPEEDUP_INTERVAL
                        and speed_change_time != -1
                    ):
                        snake.recover_speed()
                        speed_change_time = -1

                    if not isdead:
                        elapsed_time = time.time() - start_time
                        direction_name = snake.get_direction_name(last_direction_input)

                    interface.show_running_info(
                        scores, file_score, player_name, elapsed_time, direction_name
                    )  # 使用Interface显示信息
                    if isdead:
                        if not running:
                            break  # 退出游戏
                        if once_flag:
                            scores_rank.save_score(player_name, scores)
                            once_flag = False
                        death_choice = death_menu.run(scores)

                        if death_choice == "restart":
                            init_game()
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
