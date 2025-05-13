import pygame
import random
import time
import food
import config

BLOCK_SIZE = config.BLOCK_SIZE


class PowerUp(food.Food):  # 继承: PowerUp继承自Food类，获得其基本属性和方法
    def __init__(self, SCREEN_X, SCREEN_Y):  # 直接传递屏幕尺寸，与Food一致
        super().__init__(
            SCREEN_X, SCREEN_Y
        )  # 继承: 调用父类Food的构造函数，继承屏幕网格系统
        self.rect = pygame.Rect(
            -BLOCK_SIZE, 0, BLOCK_SIZE, BLOCK_SIZE
        )  # 初始位置在屏幕外
        self.last_move_time = 0
        self.move_interval = config.POWERUP_MOVE_INTERVAL
        self.score_increase = config.POWERUP_SCORE  # 多态: 不同于Food类的得分值

    def set(self, snake_body):  # 多态: 重写父类的set方法，添加额外参数和检查
        # 确保 PowerUp 不与蛇身重叠，使用继承的 allposx 和 allposy
        while True:
            self.rect.left = random.choice(self.allposx)  # 继承: 使用从Food类继承的属性
            self.rect.top = random.choice(self.allposy)
            if self.rect not in snake_body:
                break

    def move(self, snake_body):  # 多态: PowerUp独有的方法，扩展了父类功能
        current_time = time.time()
        if current_time - self.last_move_time > self.move_interval:
            self.set(snake_body)  # 移动 PowerUp
            self.last_move_time = current_time

    def reset_move_time(self, total_pause_time=-1):  # 多态: PowerUp特有的方法
        if total_pause_time != -1:
            self.last_move_time += total_pause_time
        else:
            self.last_move_time = time.time()

    def draw(self, screen):  # 多态: 重写父类的隐式draw方法，使用不同的颜色
        pygame.draw.rect(screen, (255, 255, 0), self.rect, 0)  # 黄色，与Food的红色不同
