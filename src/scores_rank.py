import config
import os  # 导入 os 模块，用于文件操作


def load_scores():
    """从文件读取分数，返回一个列表，每个元素是一个 (name, score) 元组."""
    scores = []
    try:
        with open(config.SCORE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                name, score = line.strip().split(":")
                scores.append((name, int(score)))
    except FileNotFoundError:
        open(config.SCORE_PATH, "w").close()
    return scores


def save_score(player_name, score):
    """保存分数到文件."""
    with open(config.SCORE_PATH, "a", encoding="utf-8") as f:
        f.write(f"{player_name}:{score}\n")


def get_max_score():
    try:
        scores = load_scores()
        if scores:  # 确保 scores 列表不为空
            # 使用 lambda 表达式获取最高分
            max_score = max(scores, key=lambda item: item[1])[1]
        else:
            max_score = -1  # 文件为空
    except FileNotFoundError:
        max_score = -1  # 文件不存在
    return max_score
