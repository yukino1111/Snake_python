import pygame
import sys
import config
import os


class Interface:
    def __init__(self, screen_width, screen_height, caption):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(caption)
        self.font = pygame.font.Font(config.FONT_PATH, 30)  # 缩小字体
        self.text_color = (0, 0, 0)  # 默认文本颜色为黑色
        self.bg_color = (240, 240, 240)  # 默认背景颜色
        self.running = True  # 游戏是否运行

    def draw_text(
        self,
        text,
        color,
        x,
        y,
        x_align="center",
        y_align="center",
        font_size_ratio=0.05,
        bold=False,
    ):
        """绘制文本，支持相对位置和字体大小"""
        font_size = int(self.screen_height * font_size_ratio)
        font = pygame.font.Font(config.FONT_PATH, font_size)
        font.set_bold(bold)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if x_align == "left":
            text_rect.left = int(x * self.screen_width)
        elif x_align == "right":
            text_rect.right = int(x * self.screen_width)
        else:
            text_rect.centerx = int(x * self.screen_width)

        if y_align == "top":
            text_rect.top = int(y * self.screen_height)
        elif y_align == "bottom":
            text_rect.bottom = int(y * self.screen_height)
        else:
            text_rect.centery = int(y * self.screen_height)

        self.screen.blit(text_surface, text_rect)

    def draw_button_text(self, text, color, x, y, font_size_ratio=0.04):
        """绘制按钮文本，支持相对位置和字体大小"""
        font_size = int(self.screen_height * font_size_ratio)
        font = pygame.font.Font(config.FONT_PATH, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(x), int(y))  # 按钮文本居中显示
        self.screen.blit(text_surface, text_rect)

    def draw_button(self, text, color, x, y, width, height, font_size_ratio=0.04):
        button_rect = pygame.Rect(x - width / 2, y - height / 2, width, height)
        # 绘制阴影
        shadow_color = (100, 100, 100)  # 灰色阴影
        shadow_offset = 3  # 阴影偏移量
        shadow_rect = pygame.Rect(
            button_rect.x + shadow_offset,
            button_rect.y + shadow_offset,
            button_rect.width,
            button_rect.height,
        )
        pygame.draw.rect(self.screen, shadow_color, shadow_rect)

        pygame.draw.rect(self.screen, color, button_rect)
        button_center_x = x
        button_center_y = y
        self.draw_button_text(
            text,
            (0, 0, 0),
            button_center_x,
            button_center_y,
            font_size_ratio=font_size_ratio,
        )  # 按钮文字为黑色
        return button_rect

    def show_running_info(
        self, scores, max_score, player_name, elapsed_time, direction_name
    ):
        """显示游戏运行时的信息"""
        font_size_ratio = 0.05  # 字体大小为屏幕高度的 5%
        real_score = scores if scores > max_score else max_score
        text_color = (50, 50, 50)  # 加深颜色，使用深灰色
        self.draw_text(
            f"Max Score: {real_score}",
            text_color,
            0.1,  # 左侧 10% 的位置
            0.85,  # 底部 90% 的位置
            x_align="left",
            y_align="bottom",
            font_size_ratio=font_size_ratio,
        )
        self.draw_text(
            f"{player_name}的Score: {scores}",
            text_color,
            0.1,  # 左侧 10% 的位置
            0.9,  # 底部 93.5% 的位置
            x_align="left",
            y_align="bottom",
            font_size_ratio=font_size_ratio,
        )
        self.draw_text(
            f"时间: {int(elapsed_time)}",
            text_color,
            0.1,  # 左侧 10% 的位置
            0.95,  # 底部 97% 的位置
            x_align="left",
            y_align="bottom",
            font_size_ratio=font_size_ratio,
        )

        # 右侧信息
        self.draw_text(
            f"按键记录: {direction_name}",
            self.text_color,  # 黑色
            0.95,  # 右侧 5% 的位置
            0.1,  # 顶部 10% 的位置
            x_align="right",
            y_align="center",
            font_size_ratio=font_size_ratio,
        )

    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            # print(str(event))
            if event.type == pygame.WINDOWCLOSE:
                self.running = False
                pygame.quit()
                sys.exit()
                # print("quit")
                return "quit"
            return event  # 返回事件


class NameInputMenu(Interface):
    def __init__(self, screen_width, screen_height, caption):
        super().__init__(screen_width, screen_height, caption)
        self.input_text = ""
        self.active = True  # 是否激活输入框
        self.confirm_button_rect = None
        self.back_button_rect = None

    def run(self):
        self.input_text = ""
        self.active = True
        while self.active and self.running:
            self.screen.fill(self.bg_color)  # 浅灰色背景
            # 绘制提示文本
            self.draw_text(
                "请输入你的名字:", self.text_color, 0.5, 0.3, font_size_ratio=0.06
            )

            # 绘制输入框
            input_rect = pygame.Rect(
                self.screen_width / 2 - 150, self.screen_height / 2 - 25, 300, 50
            )
            pygame.draw.rect(self.screen, (255, 255, 255), input_rect, 0)  # 白色背景
            pygame.draw.rect(self.screen, self.text_color, input_rect, 2)  # 黑色边框

            # 绘制输入文本
            self.draw_text(
                self.input_text, self.text_color, 0.5, 0.5, font_size_ratio=0.04
            )

            # 绘制按钮
            button_width = 100
            button_height = 40
            button_color = (70, 130, 180)  # 钢青色

            self.confirm_button_rect = self.draw_button(
                "确定",
                button_color,
                self.screen_width / 2 + 75,
                self.screen_height / 2 + 100,
                button_width,
                button_height,
                font_size_ratio=0.03,
            )
            self.back_button_rect = self.draw_button(
                "返回",
                button_color,
                self.screen_width / 2 - 75,
                self.screen_height / 2 + 100,
                button_width,
                button_height,
                font_size_ratio=0.03,
            )

            event = self.handle_events()
            if event and event.type == pygame.MOUSEBUTTONDOWN:
                if self.confirm_button_rect.collidepoint(event.pos):
                    self.active = False  # 结束输入
                    return self.input_text
                if self.back_button_rect.collidepoint(event.pos):
                    self.active = False
                    return ""  # 返回主菜单

            if event and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.active = False  # 结束输入
                    return self.input_text
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

            pygame.display.flip()
        return None  # 如果没有输入名字，返回None


class MainMenu(Interface):
    def __init__(self, screen_width, screen_height, caption):
        super().__init__(screen_width, screen_height, caption)
        self.start_button_rect = None
        self.leaderboard_button_rect = None
        self.about_button_rect = None
        self.quit_button_rect = None

    def run(self):
        while self.running:
            self.screen.fill(self.bg_color)  # 浅灰色背景

            # 绘制标题
            self.draw_text(
                "贪吃蛇",  # 游戏标题
                self.text_color,
                0.5,  # 居中显示
                0.15,  # 顶部 15% 的位置
                font_size_ratio=0.1,  # 字体大小为屏幕高度的 10%
            )

            # 绘制按钮
            button_width = 250
            button_height = 60
            button_color = (52, 152, 219)  # 亮蓝色

            button_y_start = self.screen_height / 2 - 100  # 调整起始位置
            button_spacing = 70  # 调整按钮间距

            self.start_button_rect = self.draw_button(
                "开始游戏",
                button_color,
                self.screen_width / 2,
                button_y_start,
                button_width,
                button_height,
            )
            self.leaderboard_button_rect = self.draw_button(
                "排行榜",
                button_color,
                self.screen_width / 2,
                button_y_start + button_spacing,
                button_width,
                button_height,
            )
            self.about_button_rect = self.draw_button(
                "关于",
                button_color,
                self.screen_width / 2,
                button_y_start + 2 * button_spacing,
                button_width,
                button_height,
            )
            self.quit_button_rect = self.draw_button(
                "退出游戏",
                button_color,
                self.screen_width / 2,
                button_y_start + 3 * button_spacing,
                button_width,
                button_height,
            )

            event = self.handle_events()
            if event == "quit":
                print("quit1")
                return "quit"
            # if event and event.type == pygame.QUIT:
            #     return "quit"  # 退出游戏
            if event and event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    return "start"  # 开始游戏
                if self.leaderboard_button_rect.collidepoint(event.pos):
                    return "leaderboard"  # 排行榜
                if self.about_button_rect.collidepoint(event.pos):
                    return "about"  # 关于
                if self.quit_button_rect.collidepoint(event.pos):
                    return "quit"  # 退出游戏

            pygame.display.flip()


class LeaderboardMenu(Interface):
    def __init__(self, screen_width, screen_height, caption):
        super().__init__(screen_width, screen_height, caption)
        self.back_button_rect = None

    def run(self, scores):
        for i, (name, score) in enumerate(scores[:10]):  # 显示前10名
            zipped_data = [(name, score)]
        score_values1 = map(lambda item: item[1], scores)
        while self.running:
            self.screen.fill(self.bg_color)

            # 显示排行榜标题
            self.draw_text("排行榜", self.text_color, 0.5, 0.15, font_size_ratio=0.08)
            # 显示排行榜数据
            y_offset = 0.3  # 初始偏移量
            for i, (name, score) in enumerate(scores[:10]):  # 显示前10名

                text = f"第{i + 1}名 {name}: {score}"
                self.draw_text(
                    text,
                    self.text_color,
                    0.5,
                    y_offset + i * 0.05,
                    font_size_ratio=0.04,
                )

            # 绘制返回按钮
            button_width = 150
            button_height = 50
            button_color = (100, 149, 237)  # 矢车菊蓝

            self.back_button_rect = self.draw_button(
                "返回",
                button_color,
                self.screen_width / 2,
                self.screen_height * 0.9,
                button_width,
                button_height,
                font_size_ratio=0.03,
            )

            event = self.handle_events()
            if event and event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect.collidepoint(event.pos):
                    return "mainmenu"  # 返回主菜单

            pygame.display.flip()
        print(zipped_data)
        print(max(score_values1))


class AboutMenu(Interface):
    def __init__(self, screen_width, screen_height, caption):
        super().__init__(screen_width, screen_height, caption)
        self.back_button_rect = None

    def run(self):
        while self.running:
            self.screen.fill(self.bg_color)

            # 读取关于信息
            about_text = self.read_about_text()

            # 显示关于信息
            y_offset = 0.2
            line_spacing = 0.04
            for i, line in enumerate(about_text):
                self.draw_text(
                    line,
                    self.text_color,
                    0.5,
                    y_offset + i * line_spacing,
                    font_size_ratio=0.03,
                )

            # 绘制返回按钮
            button_width = 150
            button_height = 50
            button_color = (100, 149, 237)  # 矢车菊蓝

            self.back_button_rect = self.draw_button(
                "返回",
                button_color,
                self.screen_width / 2,
                self.screen_height * 0.9,
                button_width,
                button_height,
                font_size_ratio=0.03,
            )

            event = self.handle_events()
            if event and event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect.collidepoint(event.pos):
                    return "mainmenu"  # 返回主菜单

            pygame.display.flip()

    def read_about_text(self):
        """读取 about.md 文件内容"""
        try:
            with open(config.MD_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()
            return [line.strip() for line in lines]
        except FileNotFoundError:
            return ["about.md 文件未找到"]
        except Exception as e:
            return [f"读取 about.md 文件时发生错误: {e}"]


class PauseMenu(Interface):
    def __init__(self, screen_width, screen_height, caption):
        super().__init__(screen_width, screen_height, caption)
        self.continue_button_rect = None
        self.restart_button_rect = None
        self.mainmenu_button_rect = None
        self.quit_button_rect = None

    def run(self):
        while self.running:
            self.screen.fill(self.bg_color)  # 浅灰色背景

            # 绘制按钮
            button_width = 250
            button_height = 60
            button_color = (149, 165, 166)  # 灰色

            button_y_start = self.screen_height / 2 - 100  # 调整起始位置
            button_spacing = 70  # 调整按钮间距

            self.draw_text(
                "游戏暂停",
                self.text_color,  # 黑色
                self.screen_width / 2,
                button_y_start - button_spacing,  # 调整位置
            )
            self.continue_button_rect = self.draw_button(
                "继续游戏",
                button_color,
                self.screen_width / 2,
                button_y_start,
                button_width,
                button_height,
            )
            self.restart_button_rect = self.draw_button(
                "重新开始",
                button_color,
                self.screen_width / 2,
                button_y_start + button_spacing,
                button_width,
                button_height,
            )
            self.mainmenu_button_rect = self.draw_button(
                "返回主菜单",
                button_color,
                self.screen_width / 2,
                button_y_start + 2 * button_spacing,
                button_width,
                button_height,
            )
            self.quit_button_rect = self.draw_button(
                "退出游戏",
                button_color,
                self.screen_width / 2,
                button_y_start + 3 * button_spacing,
                button_width,
                button_height,
            )

            event = self.handle_events()
            if event and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "continue"
            if event and event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button_rect.collidepoint(event.pos):
                    return "continue"  # 继续游戏
                if self.restart_button_rect.collidepoint(event.pos):
                    return "restart"  # 重新开始
                if self.mainmenu_button_rect.collidepoint(event.pos):
                    return "mainmenu"  # 返回主菜单
                if self.quit_button_rect.collidepoint(event.pos):
                    return "quit"  # 退出游戏

            pygame.display.flip()


class DeathMenu(Interface):
    def __init__(self, screen_width, screen_height, caption):
        super().__init__(screen_width, screen_height, caption)
        self.restart_button_rect = None
        self.mainmenu_button_rect = None
        self.quit_button_rect = None

    def run(self, score):
        print
        while self.running:
            self.screen.fill(self.bg_color)  # 浅灰色背景

            # 绘制按钮
            button_width = 250
            button_height = 60
            button_color = (231, 76, 60)  # 砖红色

            button_y_start = self.screen_height / 2 - 50  # 调整起始位置
            button_spacing = 70  # 调整按钮间距

            self.draw_text(
                "你死了!",
                (231, 76, 60),  # 砖红色
                0.5,  # 居中显示
                0.2,  # 调整位置
                font_size_ratio=0.08,  # 调整字体大小
                bold=True,
            )
            self.draw_text(
                f"你的分数是: {score}",
                self.text_color,  # 使用默认文本颜色
                0.5,  # 居中显示
                0.3,  # 调整位置
                font_size_ratio=0.05,  # 调整字体大小
            )
            self.restart_button_rect = self.draw_button(
                "重新开始",
                button_color,
                self.screen_width / 2,
                button_y_start,
                button_width,
                button_height,
            )
            self.leaderboard_button_rect = self.draw_button(
                "查看排行榜",
                button_color,
                self.screen_width / 2,
                button_y_start + button_spacing,
                button_width,
                button_height,
            )
            self.mainmenu_button_rect = self.draw_button(
                "返回主菜单",
                button_color,
                self.screen_width / 2,
                button_y_start + 2 * button_spacing,
                button_width,
                button_height,
            )
            self.quit_button_rect = self.draw_button(
                "退出游戏",
                button_color,
                self.screen_width / 2,
                button_y_start + 3 * button_spacing,
                button_width,
                button_height,
            )

            event = self.handle_events()
            if event and event.type == pygame.MOUSEBUTTONDOWN:
                if self.restart_button_rect.collidepoint(event.pos):
                    return "restart"  # 重新开始
                if self.leaderboard_button_rect.collidepoint(event.pos):
                    return "leaderboard"  # 查看排行榜
                if self.mainmenu_button_rect.collidepoint(event.pos):
                    return "mainmenu"  # 返回主菜单
                if self.quit_button_rect.collidepoint(event.pos):
                    return "quit"  # 退出游戏

            pygame.display.flip()


class QuitMenu(Interface):
    def __init__(self, screen_width, screen_height, caption):
        super().__init__(screen_width, screen_height, caption)
        self.yes_button_rect = None
        self.no_button_rect = None

    def run(self):
        while self.running:
            self.screen.fill(self.bg_color)
            # 绘制退出提示
            self.draw_text(
                "退出游戏？", self.text_color, 0.5, 0.4, font_size_ratio=0.06
            )

            # 绘制按钮
            button_width = 100
            button_height = 40
            button_color = (192, 192, 192)  # 银色

            self.yes_button_rect = self.draw_button(
                "是",
                button_color,
                self.screen_width / 2 - 75,
                self.screen_height / 2 + 100,
                button_width,
                button_height,
                font_size_ratio=0.03,
            )
            self.no_button_rect = self.draw_button(
                "否",
                button_color,
                self.screen_width / 2 + 75,
                self.screen_height / 2 + 100,
                button_width,
                button_height,
                font_size_ratio=0.03,
            )

            event = self.handle_events()
            if event and event.type == pygame.MOUSEBUTTONDOWN:
                if self.yes_button_rect.collidepoint(event.pos):
                    return "quit"
                if self.no_button_rect.collidepoint(event.pos):
                    return "continue"  # 返回上一层菜单

            pygame.display.flip()
