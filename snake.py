import pygame
import sys
import random
import time

# 全局定义
SCREEN_X = 1200
SCREEN_Y = 700


# 蛇类
# 点以25为单位
class Snake(object):
    # 初始化各种需要的属性 [开始时默认向右/身体块x5]
    def __init__(self):
        self.dirction = pygame.K_RIGHT
        self.body = []
        for x in range(5):
            self.addnode()
        self.last_move_time = 0  # 上次移动的时间
        self.move_interval = 0.1  # 移动间隔，单位秒 (调整这个值来控制蛇的速度)
        self.next_direction = None  # 存储下一次移动的方向

    # 无论何时 都在前端增加蛇块
    def addnode(self):
        left, top = (0, 0)
        if self.body:
            left, top = (self.body[0].left, self.body[0].top)
        node = pygame.Rect(left, top, 25, 25)
        if self.dirction == pygame.K_LEFT:
            node.left -= 25
        elif self.dirction == pygame.K_RIGHT:
            node.left += 25
        elif self.dirction == pygame.K_UP:
            node.top -= 25
        elif self.dirction == pygame.K_DOWN:
            node.top += 25
        self.body.insert(0, node)

    # 删除最后一个块
    def delnode(self):
        self.body.pop()

    # 死亡判断
    def isdead(self):
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
    def move(self):
        current_time = time.time()
        if current_time - self.last_move_time >= self.move_interval:
            # 如果有待定的方向，则使用它
            if self.next_direction is not None:
                self.changedirection(self.next_direction)
                self.next_direction = None  # 清空待定方向

            self.addnode()
            self.delnode()
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


# 食物类
# 方法： 放置/移除
# 点以25为单位
class Food:
    def __init__(self):
        self.rect = pygame.Rect(-25, 0, 25, 25)
        self.allposx = []
        self.allposy = []
        # 不靠墙太近 25 ~ SCREEN_X-25 之间
        for pos in range(25, SCREEN_X - 25, 25):
            self.allposx.append(pos)
        for pos in range(25, SCREEN_Y - 25, 25):
            self.allposy.append(pos)

    def remove(self):
        self.rect.x = -25

    def set(self):
        if self.rect.x == -25:
            self.rect.left = random.choice(self.allposx)
            self.rect.top = random.choice(self.allposy)
            # print(self.rect)


def show_text(
    screen,
    pos_x_ratio,
    pos_y_ratio,
    text,
    color,
    font_bold=False,
    font_size=60,
    font_italic=False,
    centered_y=False,
):
    # 获取系统字体，并设置文字大小
    # cur_font = pygame.font.SysFont("宋体", font_size)
    cur_font = pygame.font.Font("PingFang-Medium.ttf", font_size)

    # 设置是否加粗属性
    cur_font.set_bold(font_bold)
    # 设置是否斜体属性
    cur_font.set_italic(font_italic)
    # 设置文字内容
    text_fmt = cur_font.render(text, 1, color)
    text_rect = text_fmt.get_rect()  # 获取文本的矩形区域
    # 绘制文字
    # screen.blit(text_fmt, pos)
    pos_x = int(SCREEN_X * pos_x_ratio)
    pos_y = int(SCREEN_Y * pos_y_ratio)

    if centered_y:
        pos_x = pos_x - text_rect.width // 2

    screen.blit(text_fmt, (pos_x, pos_y))


def get_direction_name(direction):
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


def main():
    pygame.init()
    screen_size = (SCREEN_X, SCREEN_Y)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Snake")
    icon = pygame.image.load("icon.jpg")  # 替换为你的图标文件路径
    pygame.display.set_icon(icon)  # 设置窗口图标
    clock = pygame.time.Clock()
    scores = 0
    isdead = False

    elapsed_time = 0

    # 蛇/食物
    snake = Snake()
    food = Food()
    last_direction_input = None  # 存储上次有效的方向输入
    start_time = time.time()

    while True:
        for event in pygame.event.get():
            # fps = clock.get_fps()  # 获取当前帧数
            # print(f"FPS: {fps}")  # 打印帧数

            # pygame.display.flip()  # 更新屏幕

            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()  # 不加这一行，idle中窗口无法退出
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
            # scores += random.randint(1001, 10000)
            if snake.move():  # 如果蛇成功移动
                scores += 1
        for rect in snake.body:
            pygame.draw.rect(screen, (20, 220, 39), rect, 0)

        # 显示死亡文字
        isdead = snake.isdead()
        if isdead:
            show_text(
                screen,
                1 / 2,  # 居中
                2 / 7,
                "YOU DEAD!",
                (227, 29, 18),
                False,
                100,
                False,
                True,
            )
            show_text(
                screen,
                1 / 2,  # 居中
                4 / 7,
                "press space to try again...",
                (0, 0, 22),
                False,
                30,
                False,
                True,
            )

        # 食物处理 / 吃到+50分
        # 当食物rect与蛇头重合,吃掉 -> Snake增加一个Node
        if food.rect == snake.body[0]:
            scores += 50
            food.remove()
            snake.addnode()

        # 食物投递
        food.set()
        pygame.draw.rect(screen, (136, 0, 21), food.rect, 0)

        # 显示分数文字
        show_text(
            screen,
            1 / 10,
            29 / 40,
            "Scores: " + str(scores),
            (223, 223, 223),
            font_size=45,
        )
        show_text(
            screen,
            1 / 10,
            32 / 40,
            "ming的Scores: " + str(scores),
            (223, 223, 223),
            font_size=45,
        )
        if not isdead:
            elapsed_time = time.time() - start_time
        show_text(
            screen,
            1 / 10,
            35 / 40,
            "时间: " + str(int(elapsed_time)),
            (223, 223, 223),
            font_size=45,
        )

        # 显示上次方向输入
        direction_name = get_direction_name(last_direction_input)
        show_text(
            screen,
            8 / 10,
            1 / 10,
            "按键记录: " + direction_name,
            (0, 0, 0),
            font_size=30,
        )

        pygame.display.update()
        clock.tick(80)  # 限制帧数为60 FPS


if __name__ == "__main__":
    main()
