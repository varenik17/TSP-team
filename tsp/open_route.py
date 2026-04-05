from typing import List, Tuple

from .helpers import path_length


def cycle_to_open_path(cycle: List[int], dist: List[List[float]], start_node: int) -> Tuple[List[int], float]:
    """
    Разрезает цикл в одном ребре так, чтобы:
    - маршрут начинался со start_node
    - путь был как можно короче
    """
    n = len(cycle)
    if n == 0:
        return [], 0.0
    if n == 1:
        return cycle[:], 0.0

    start_pos = cycle.index(start_node)
    rotated = cycle[start_pos:] + cycle[:start_pos]

    best_path = None
    best_len = float("inf")

    for cut in range(1, n):
        path1 = rotated[:]
        removed_edge_1 = dist[path1[cut - 1]][path1[cut]]

        open_len_1 = sum(dist[path1[i]][path1[i + 1]] for i in range(n - 1)) - removed_edge_1
        if open_len_1 < best_len:
            best_len = open_len_1
            best_path = path1

        reversed_cycle = [rotated[0]] + list(reversed(rotated[1:]))
        removed_edge_2 = dist[reversed_cycle[cut - 1]][reversed_cycle[cut]]
        open_len_2 = sum(dist[reversed_cycle[i]][reversed_cycle[i + 1]] for i in range(n - 1)) - removed_edge_2
        if open_len_2 < best_len:
            best_len = open_len_2
            best_path = reversed_cycle

    return best_path, best_len