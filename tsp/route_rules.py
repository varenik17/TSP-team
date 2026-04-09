from typing import List, Optional

from .route_types import Place
from .constraints import is_food_place, has_two_nonconsecutive_food_stops


def food_positions(route: List[int], places: List[Place], start_index: int) -> List[int]:
    positions = []
    for pos, idx in enumerate(route):
        if idx != start_index and is_food_place(places[idx]):
            positions.append(pos)
    return positions

# если еда идет подряд, то пытаемся переставить между точками любую другую не еду
def try_separate_food_stops(route: List[int], places: List[Place], start_index: int) -> List[int]:
    if has_two_nonconsecutive_food_stops(route, places, start_index):
        return route[:]

    result = route[:]
    n = len(result)

    for i in range(1, n - 1):
        if is_food_place(places[result[i]]) and is_food_place(places[result[i + 1]]):
            # ищем не-food точку дальше по маршруту
            for j in range(i + 2, n):
                if not is_food_place(places[result[j]]):
                    result[i + 1], result[j] = result[j], result[i + 1]
                    if has_two_nonconsecutive_food_stops(result, places, start_index):
                        return result
                    # откатываемся
                    result[i + 1], result[j] = result[j], result[i + 1]

            # ищем не-food точку раньше по маршруту (не старт)
            for j in range(1, i):
                if not is_food_place(places[result[j]]):
                    result[i], result[j] = result[j], result[i]
                    if has_two_nonconsecutive_food_stops(result, places, start_index):
                        return result
                    result[i], result[j] = result[j], result[i]

    return route[:]