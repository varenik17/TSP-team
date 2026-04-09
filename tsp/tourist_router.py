from typing import List, Dict, Any

from .route_types import Place
from .selector import greedy_select_places
from .constraints import (
    route_total_time,
    route_cost,
    has_two_nonconsecutive_food_stops,
)
from .lk import LinKernighanSolver

 #управление всеми процессами ( селектор, Лин-Керниган, цикл в путь, ограничения, корректировки)

def reorder_with_fixed_start(route: List[int], start_index: int) -> List[int]:
    if start_index not in route:
        raise ValueError("Стартовая точка отсутствует в маршруте")
    pos = route.index(start_index)
    return route[pos:] + route[:pos]


def build_submatrix(dist: List[List[float]], indices: List[int]) -> List[List[float]]:
    return [[dist[i][j] for j in indices] for i in indices]


def remap_route(local_route: List[int], global_indices: List[int]) -> List[int]:
    return [global_indices[i] for i in local_route]


def cycle_to_path_keep_start(cycle: List[int], start_index: int) -> List[int]:
    ordered = reorder_with_fixed_start(cycle, start_index)
    return ordered


def trim_route_to_constraints(
    route: List[int],
    dist: List[List[float]],
    places: List[Place],
    speed_kmh: float,
    max_time_hours: float,
    max_budget: float,
    start_index: int,
) -> List[int]:
    result = route[:]
    while len(result) > 1:
        total_cost = route_cost(result, places, start_index)
        total_time = route_total_time(result, dist, places, speed_kmh, start_index)
        if total_cost <= max_budget and total_time <= max_time_hours:
            break
        result.pop()
    return result


def build_tourist_route(
    dist: List[List[float]],
    places: List[Place],
    start_index: int,
    max_time_hours: float,
    max_budget: float,
    speed_kmh: float = 5.0,
    lk_max_depth: int = 5,
    lk_candidate_count: int = 8,
) -> Dict[str, Any]:
    selected = greedy_select_places(
        dist=dist,
        places=places,
        start_index=start_index,
        max_time_hours=max_time_hours,
        max_budget=max_budget,
        speed_kmh=speed_kmh,
    )

    if len(selected) == 1:
        return {
            "route_indices": [start_index],
            "route_names": [places[start_index].name],
            "total_cost": 0.0,
            "total_time_hours": 0.0,
            "visited_count": 0,
            "food_rule_ok": False,
        }

    # Если точек мало, LK может быть не нужен
    if len(selected) < 4:
        route = selected[:]
    else:
        local_dist = build_submatrix(dist, selected)
        solver = LinKernighanSolver(
            dist=local_dist,
            max_depth=lk_max_depth,
            candidate_count=lk_candidate_count,
        )
        local_cycle, _ = solver.solve()
        global_cycle = remap_route(local_cycle, selected)
        route = cycle_to_path_keep_start(global_cycle, start_index)

    route = trim_route_to_constraints(
        route=route,
        dist=dist,
        places=places,
        speed_kmh=speed_kmh,
        max_time_hours=max_time_hours,
        max_budget=max_budget,
        start_index=start_index,
    )

    # Локальное исправление , если вдруг food-точки стоят подряд
    from .route_rules import try_separate_food_stops
    route = try_separate_food_stops(route, places, start_index)

    total_cost = route_cost(route, places, start_index)
    total_time = route_total_time(route, dist, places, speed_kmh, start_index)
    food_rule_ok = has_two_nonconsecutive_food_stops(route, places, start_index)

    return {
        "route_indices": route,
        "route_names": [places[i].name for i in route],
        "total_cost": total_cost,
        "total_time_hours": total_time,
        "visited_count": max(0, len(route) - 1),
        "food_rule_ok": food_rule_ok,
    }