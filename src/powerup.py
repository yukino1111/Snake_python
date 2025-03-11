import pygame
import random
import time

import config
BLOCK_SIZE = config.BLOCK_SIZE
class PowerUp:
    def __init__(self, food):  # 传入 Food 对象
        self.food = food
        self.rect = pygame.Rect(-BLOCK_SIZE, 0, BLOCK_SIZE, BLOCK_SIZE)  # 初始位置在屏幕外
        self.last_move_time = 0
        self.move_interval = config.POWERUP_MOVE_INTERVAL
        self.score_increase = config.POWERUP_SCORE

    def set(self, snake_body):
        # 确保 PowerUp 不与蛇身重叠，并且使用 Food 的生成位置
        while True:
            self.rect.left = random.choice(self.food.allposx)
            self.rect.top = random.choice(self.food.allposy)
            if self.rect not in snake_body:
                break

    def move(self, snake_body):
        current_time = time.time()
        if current_time - self.last_move_time > self.move_interval:
            self.set(snake_body)  # 移动 PowerUp
            self.last_move_time = current_time

    def reset_move_time(self,total_pause_time=-1):
        if total_pause_time != -1:
            self.last_move_time += total_pause_time
        else:
            self.last_move_time = time.time()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), self.rect, 0)  # 黄色
