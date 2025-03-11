import pygame
import config
import heapq

BLOCK_SIZE = config.BLOCK_SIZE




# def is_safe(node, snake_body, screen_x, screen_y):
#     """
#     检查节点是否安全（不撞墙，不撞自己）。
#     """
#     if (
#         node[0] < 0
#         or node[0] >= screen_x
#         or node[1] < 0
#         or node[1] >= screen_y
#         or pygame.Rect(node[0], node[1], config.BLOCK_SIZE, config.BLOCK_SIZE)
#         in snake_body[1:]
#     ):
#         return False
#     return True


# def dfs(start, goal, snake_body, screen_x, screen_y, path=None, visited=None, depth=0, max_depth=100):
#     """
#     深度优先搜索算法。
#     """
#     if path is None:
#         path = [start]
#     if visited is None:
#         visited = set()

#     visited.add(start)

#     if start == goal:
#         return path

#     if depth > max_depth:
#         return None  # 达到最大搜索深度，停止搜索

#     # 探索邻居节点
#     for direction in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
#         neighbor = (start[0], start[1])
#         if direction == pygame.K_LEFT:
#             neighbor = (start[0] - config.BLOCK_SIZE, start[1])
#         elif direction == pygame.K_RIGHT:
#             neighbor = (start[0] + config.BLOCK_SIZE, start[1])
#         elif direction == pygame.K_UP:
#             neighbor = (start[0], start[1] - config.BLOCK_SIZE)
#         elif direction == pygame.K_DOWN:
#             neighbor = (start[0], start[1] + config.BLOCK_SIZE)

#         # 检查邻居节点是否安全
#         if not is_safe(neighbor, snake_body, screen_x, screen_y) or neighbor in visited:
#             continue

#         # 递归搜索
#         new_path = dfs(neighbor, goal, snake_body, screen_x, screen_y, path + [neighbor], visited, depth + 1, max_depth)
#         if new_path:
#             return new_path

#     return None  # 没有找到路径



# def get_direction_from_path(start, next_node):
#     """
#     根据路径中的两个节点，确定移动方向。
#     """
#     if next_node[0] < start[0]:
#         return pygame.K_LEFT
#     elif next_node[0] > start[0]:
#         return pygame.K_RIGHT
#     elif next_node[1] < start[1]:
#         return pygame.K_UP
#     elif next_node[1] > start[1]:
#         return pygame.K_DOWN
#     return None


# def find_path(self, food_position):
#     """
#     使用 DFS 算法寻找通往食物的安全路径。
#     Args:
#         food_position (pygame.math.Vector2): 食物的中心坐标。
#     Returns:
#         int: 下一步移动的最佳方向（pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN），
#                  如果没有安全路径则返回 None。
#     """
#     start = (self.body[0].x, self.body[0].y)
#     goal = (food_position.x, food_position.y)

#     path = dfs(start, goal, self.body, config.SCREEN_X, config.SCREEN_Y)

#     if path and len(path) > 1:
#         next_node = path[1]  # 获取路径中的下一个节点
#         best_direction = get_direction_from_path(start, next_node)
#         return best_direction

#     return None  # 没有找到路径


def find_path(self, food_position):
    """
    寻找通往食物的安全路径。
    Args:
        food_position (pygame.math.Vector2): 食物的中心坐标。
    Returns:
        int: 下一步移动的最佳方向（pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN），
                如果没有安全路径则返回 None。
    """
    head = self.body[0].copy()  # 复制蛇头，避免修改原始蛇身
    possible_directions = [
        pygame.K_LEFT,
        pygame.K_RIGHT,
        pygame.K_UP,
        pygame.K_DOWN,
    ]
    safe_directions = []
    # 1. 筛选安全的方向
    for direction in possible_directions:
        temp_head = head.copy()
        if direction == pygame.K_LEFT:
            temp_head.left -= BLOCK_SIZE
        elif direction == pygame.K_RIGHT:
            temp_head.left += BLOCK_SIZE
        elif direction == pygame.K_UP:
            temp_head.top -= BLOCK_SIZE
        elif direction == pygame.K_DOWN:
            temp_head.top += BLOCK_SIZE
        # 检查是否撞墙或撞自己
        if (
            temp_head.x < 0
            or temp_head.x >= config.SCREEN_X
            or temp_head.y < 0
            or temp_head.y >= config.SCREEN_Y
            or temp_head in self.body[1:]
        ):
            continue  # 如果不安全，跳过此方向
        safe_directions.append(direction)
    # 2. 在安全的方向中，选择离食物最近的方向
    best_direction = None
    min_distance = float("inf")  # 初始化为无穷大
    for direction in safe_directions:
        temp_head = head.copy()
        if direction == pygame.K_LEFT:
            temp_head.left -= BLOCK_SIZE
        elif direction == pygame.K_RIGHT:
            temp_head.left += BLOCK_SIZE
        elif direction == pygame.K_UP:
            temp_head.top -= BLOCK_SIZE
        elif direction == pygame.K_DOWN:
            temp_head.top += BLOCK_SIZE
        # 计算到食物的距离（曼哈顿距离）
        distance = abs(temp_head.x - food_position.x) + abs(
            temp_head.y - food_position.y
        )
        if distance < min_distance:
            min_distance = distance
            best_direction = direction
    return best_direction
