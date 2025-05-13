import pygame
import random

import config

BLOCK_SIZE = config.BLOCK_SIZE


class Food:
    def __init__(self, SCREEN_X, SCREEN_Y):  # 父类构造函数，被PowerUp继承
        self.rect = pygame.Rect(-BLOCK_SIZE, 0, BLOCK_SIZE, BLOCK_SIZE)
        self.score_increase = config.NORMAL_SCORE  # 将被PowerUp类特化
        self.allposx = []
        self.allposy = []
        # 不靠墙太近 25 ~ SCREEN_X-25 之间
        for pos in range(BLOCK_SIZE, SCREEN_X - BLOCK_SIZE, BLOCK_SIZE):
            self.allposx.append(pos)  # 创建网格系统，被子类共享
        for pos in range(BLOCK_SIZE, SCREEN_Y - BLOCK_SIZE, BLOCK_SIZE):
            self.allposy.append(pos)  # 创建网格系统，被子类共享

    def remove(self):
        self.rect.x = -BLOCK_SIZE

    def set(self):  # 父类方法，在PowerUp中被重写以展示多态性
        if self.rect.x == -BLOCK_SIZE:
            self.rect.left = random.choice(self.allposx)
            self.rect.top = random.choice(self.allposy)
            # print(f"food pos: "+self.rect)
