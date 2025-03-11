import pygame
import time
import config
import cheat

MOVE_INTERVAL = config.MOVE_INTERVAL
SPEED_FACTOR = config.SPEED_FACTOR

BLOCK_SIZE = config.BLOCK_SIZE

class Snake(object):
    # 初始化各种需要的属性 [开始时默认向右/身体块x5]
    def __init__(self):
        self.dirction = pygame.K_RIGHT
        self.body = []
        for x in range(5):
            self.addnode()
        self.last_move_time = 0  # 上次移动的时间
        self.move_interval = (
            MOVE_INTERVAL  # 移动间隔，单位秒 (调整这个值来控制蛇的速度)
        )
        self.next_direction = None  # 存储下一次移动的方向

    # 无论何时 都在前端增加蛇块
    def addnode(self):
        left, top = (0, 0)
        if self.body:
            left, top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left, top, BLOCK_SIZE, BLOCK_SIZE)
        if self.dirction == pygame.K_LEFT:
            node.left -= BLOCK_SIZE
        elif self.dirction == pygame.K_RIGHT:
            node.left += BLOCK_SIZE
        elif self.dirction == pygame.K_UP:
            node.top -= BLOCK_SIZE
        elif self.dirction == pygame.K_DOWN:
            node.top += BLOCK_SIZE
        self.body.insert(0, node)
        # print(f"snake pos: " + node)

    # 删除最后一个块
    def delnode(self):
        self.body.pop()

    # 死亡判断
    def isdead(self, SCREEN_X, SCREEN_Y):
        # 撞墙
        if self.body[0].x not in range(SCREEN_X):
            return True
        if self.body[0].y not in range(SCREEN_Y):
            return True
        # 撞自己
        if self.body[0] in self.body[1:]:
            return True
        return False

    # 移动！
    def move(self, food_position=None):
        current_time = time.time()
        if current_time - self.last_move_time >= self.move_interval:
            # 1. 确定移动方向
            new_direction = None

            # 如果有待定的方向，则使用它
            if self.next_direction is not None:
                new_direction = self.next_direction
                self.next_direction = None  # 清空待定方向
            # 如果启用了作弊模式，则计算最佳方向
            elif food_position:
                new_direction = cheat.find_path(self,food_position)

            # 2. 移动蛇
            if new_direction:
                self.changedirection(new_direction)  # 改变蛇的方向
            self.addnode()  # 增加蛇的节点
            self.delnode()  # 删除蛇的节点

            # 3. 更新时间
            self.last_move_time = current_time
            return True  # 移动成功
        return False  # 移动失败

    # 改变方向 但是左右、上下不能被逆向改变
    def changedirection(self, curkey):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if curkey in LR + UD:
            if (curkey in LR) and (self.dirction in LR):
                return
            if (curkey in UD) and (self.dirction in UD):
                return
            self.dirction = curkey

    def get_direction_name(self, direction):
        if direction == pygame.K_LEFT:
            return "←"
        elif direction == pygame.K_RIGHT:
            return "→"
        elif direction == pygame.K_UP:
            return "↑"
        elif direction == pygame.K_DOWN:
            return "↓"
        else:
            return "None"

    def change_speed(self):
        self.move_interval /= SPEED_FACTOR

    def recover_speed(self):
        self.move_interval = MOVE_INTERVAL
