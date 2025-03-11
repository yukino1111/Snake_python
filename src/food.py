import pygame
import random

import config
BLOCK_SIZE = config.BLOCK_SIZE
class Food:
    def __init__(self, SCREEN_X, SCREEN_Y):
        self.rect = pygame.Rect(-BLOCK_SIZE, 0, BLOCK_SIZE, BLOCK_SIZE)
        self.score_increase = config.NORMAL_SCORE
        self.allposx = []
        self.allposy = []
        # 不靠墙太近 25 ~ SCREEN_X-25 之间
        for pos in range(BLOCK_SIZE, SCREEN_X - BLOCK_SIZE, BLOCK_SIZE):
            self.allposx.append(pos)
        for pos in range(BLOCK_SIZE, SCREEN_Y - BLOCK_SIZE, BLOCK_SIZE):
            self.allposy.append(pos)

    def remove(self):
        self.rect.x = -BLOCK_SIZE

    def set(self):
        if self.rect.x == -BLOCK_SIZE:
            self.rect.left = random.choice(self.allposx)
            self.rect.top = random.choice(self.allposy)
            # print(f"food pos: "+self.rect)
