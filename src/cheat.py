import pygame
import config
import heapq
from collections import deque  # 使用双端队列实现 BFS


BLOCK_SIZE = config.BLOCK_SIZE


# def find_path(self, food_position):
#     """
#     寻找通往食物的安全路径。
#     Args:
#         food_position (pygame.math.Vector2): 食物的中心坐标。
#     Returns:
#         int: 下一步移动的最佳方向（pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN），
#                 如果没有安全路径则返回 None。
#     """
#     head = self.body[0].copy()  # 复制蛇头，避免修改原始蛇身
#     possible_directions = [
#         pygame.K_LEFT,
#         pygame.K_RIGHT,
#         pygame.K_UP,
#         pygame.K_DOWN,
#     ]
#     safe_directions = []
#     # 1. 筛选安全的方向
#     for direction in possible_directions:
#         temp_head = head.copy()
#         if direction == pygame.K_LEFT:
#             temp_head.left -= BLOCK_SIZE
#         elif direction == pygame.K_RIGHT:
#             temp_head.left += BLOCK_SIZE
#         elif direction == pygame.K_UP:
#             temp_head.top -= BLOCK_SIZE
#         elif direction == pygame.K_DOWN:
#             temp_head.top += BLOCK_SIZE
#         # 检查是否撞墙或撞自己
#         if (
#             temp_head.x < 0
#             or temp_head.x >= config.SCREEN_X
#             or temp_head.y < 0
#             or temp_head.y >= config.SCREEN_Y
#             or temp_head in self.body[1:]
#         ):
#             continue  # 如果不安全，跳过此方向
#         safe_directions.append(direction)
#     # 2. 在安全的方向中，选择离食物最近的方向
#     best_direction = None
#     min_distance = float("inf")  # 初始化为无穷大
#     for direction in safe_directions:
#         temp_head = head.copy()
#         if direction == pygame.K_LEFT:
#             temp_head.left -= BLOCK_SIZE
#         elif direction == pygame.K_RIGHT:
#             temp_head.left += BLOCK_SIZE
#         elif direction == pygame.K_UP:
#             temp_head.top -= BLOCK_SIZE
#         elif direction == pygame.K_DOWN:
#             temp_head.top += BLOCK_SIZE
#         # 计算到食物的距离（曼哈顿距离）
#         distance = abs(temp_head.x - food_position.x) + abs(
#             temp_head.y - food_position.y
#         )
#         if distance < min_distance:
#             min_distance = distance
#             best_direction = direction
#     return best_direction



def _get_direction_from_path(start_node, next_node):
    """根据路径中的两个节点，确定移动方向。"""
    if next_node[0] < start_node[0]:
        return pygame.K_LEFT
    elif next_node[0] > start_node[0]:
        return pygame.K_RIGHT
    elif next_node[1] < start_node[1]:
        return pygame.K_UP
    elif next_node[1] > start_node[1]:
        return pygame.K_DOWN
    return None


def _bfs_search(start_node, goal_node, obstacles, screen_x, screen_y):
    """通用的 BFS 搜索函数"""
    queue = deque([(start_node, [])])
    visited = {start_node}
    while queue:
        current_node, path = queue.popleft()
        if current_node == goal_node:
            return path + [current_node]  # 返回包含起点和终点的完整路径
        # 探索邻居节点
        for dx, dy in [
            (-BLOCK_SIZE, 0),
            (BLOCK_SIZE, 0),
            (0, -BLOCK_SIZE),
            (0, BLOCK_SIZE),
        ]:
            neighbor_node = (current_node[0] + dx, current_node[1] + dy)
            if (
                0 <= neighbor_node[0] < screen_x
                and 0 <= neighbor_node[1] < screen_y
                and neighbor_node not in visited
                and neighbor_node not in obstacles
            ):
                visited.add(neighbor_node)
                new_path = path + [current_node]  # 将当前节点加入路径
                queue.append((neighbor_node, new_path))
    return None  # 未找到路径


def find_path(self, food_position):
    """
    使用 BFS 寻找食物路径，如果找不到则尝试追尾。
    Args:
        food_position (pygame.math.Vector2): 食物的中心坐标。
    Returns:
        int: 下一步移动的最佳方向，或 None。
    """
    start_node = (self.body[0].left, self.body[0].top)
    # 确保目标坐标与网格对齐
    goal_node = (
        food_position.x - food_position.x % BLOCK_SIZE,
        food_position.y - food_position.y % BLOCK_SIZE,
    )
    # 障碍物：蛇身（不包括头）
    obstacles_food = {(segment.left, segment.top) for segment in self.body[1:]}
    # 1. 尝试寻找食物路径
    path_to_food = _bfs_search(
        start_node, goal_node, obstacles_food, config.SCREEN_X, config.SCREEN_Y
    )
    if path_to_food and len(path_to_food) > 1:
        # print("BFS: Path to food found")
        next_node = path_to_food[1]  # 路径包含起点，所以取第二个点
        return _get_direction_from_path(start_node, next_node)
    # 2. 如果找不到食物路径，尝试追尾 (生存策略)
    # print("BFS: Path to food not found, attempting tail following.")
    tail_node = (self.body[-1].left, self.body[-1].top)
    # 追尾时的障碍物：蛇身（不包括头和尾巴）
    obstacles_tail = {(segment.left, segment.top) for segment in self.body[1:-1]}
    path_to_tail = _bfs_search(
        start_node, tail_node, obstacles_tail, config.SCREEN_X, config.SCREEN_Y
    )
    if path_to_tail and len(path_to_tail) > 1:
        # print("BFS: Path to tail found")
        next_node = path_to_tail[1]
        # 再次检查这一步是否安全（因为障碍物不同了）
        temp_head_check = self.body[0].copy()
        if _get_direction_from_path(start_node, next_node) == pygame.K_LEFT:
            temp_head_check.left -= BLOCK_SIZE
        elif _get_direction_from_path(start_node, next_node) == pygame.K_RIGHT:
            temp_head_check.left += BLOCK_SIZE
        elif _get_direction_from_path(start_node, next_node) == pygame.K_UP:
            temp_head_check.top -= BLOCK_SIZE
        elif _get_direction_from_path(start_node, next_node) == pygame.K_DOWN:
            temp_head_check.top += BLOCK_SIZE
        if temp_head_check not in self.body[1:]:  # 确保不会撞到非尾巴部分
            return _get_direction_from_path(start_node, next_node)
        # else:
        #     print("BFS: Tail following path step unsafe, falling back.")
    # 3. 如果连追尾路径都找不到，或者追尾路径第一步不安全，则随机选择一个安全方向
    # print("BFS: Path to tail not found or unsafe, falling back to random safe move.")
    safe_directions_fallback = []
    head = self.body[0].copy()
    for direction in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
        temp_head = head.copy()
        if direction == pygame.K_LEFT:
            temp_head.left -= BLOCK_SIZE
        elif direction == pygame.K_RIGHT:
            temp_head.left += BLOCK_SIZE
        elif direction == pygame.K_UP:
            temp_head.top -= BLOCK_SIZE
        elif direction == pygame.K_DOWN:
            temp_head.top += BLOCK_SIZE
        if (
            0 <= temp_head.left < config.SCREEN_X
            and 0 <= temp_head.top < config.SCREEN_Y
            and temp_head not in self.body[1:]
        ):  # 检查是否撞到身体（除头外）
            safe_directions_fallback.append(direction)
    if safe_directions_fallback:
        import random

        # print(f"BFS: Fallback safe directions: {safe_directions_fallback}")
        return random.choice(safe_directions_fallback)
    # print("BFS: No safe moves available!")
    return None  # 实在没有安全方向了
