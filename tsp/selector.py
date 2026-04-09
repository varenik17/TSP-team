from typing import List, Optional

from .route_types import Place
from .constraints import (
    is_feasible_route,
    is_food_place,
    food_count,
)

#чем меньше значение - тем лучше кандидат
#учитываю расстояние, время пребывания, стоимость
def candidate_value(
    last_idx: int,
    candidate_idx: int,
    dist: List[List[float]],
    places: List[Place],
) -> float:

    travel = dist[last_idx][candidate_idx]
    visit_time = places[candidate_idx].visit_time_hours
    visit_cost = places[candidate_idx].visit_cost

    return travel + visit_time + 0.3 * visit_cost


def pick_best_candidate(
    current_route: List[int],
    candidates: List[int],
    dist: List[List[float]],
    places: List[Place],
    start_index: int,
    max_time_hours: float,
    max_budget: float,
    speed_kmh: float,
) -> Optional[int]:
    last = current_route[-1]
    best = None
    best_value = float("inf")

    for candidate in candidates:
        trial_route = current_route + [candidate]

        if not is_feasible_route(
            route=trial_route,
            dist=dist,
            places=places,
            speed_kmh=speed_kmh,
            max_time_hours=max_time_hours,
            max_budget=max_budget,
            start_index=start_index,
        ):
            continue

        value = candidate_value(last, candidate, dist, places)
        if value < best_value:
            best_value = value
            best = candidate

    return best


# допустимый маршрут (фикс старта, 2 еды, добираем остальное)
def greedy_select_places(
    dist: List[List[float]],
    places: List[Place],
    start_index: int,
    max_time_hours: float,
    max_budget: float,
    speed_kmh: float,
) -> List[int]:
    route = [start_index]
    all_candidates = [i for i in range(len(places)) if i != start_index]

    food_candidates = [i for i in all_candidates if is_food_place(places[i])]
    other_candidates = [i for i in all_candidates if not is_food_place(places[i])]

    # стараемся включить 2 food-точки
    while food_count(route, places, start_index) < 2:
        best_food = pick_best_candidate(
            current_route=route,
            candidates=food_candidates,
            dist=dist,
            places=places,
            start_index=start_index,
            max_time_hours=max_time_hours,
            max_budget=max_budget,
            speed_kmh=speed_kmh,
        )

        if best_food is None:
            break

        route.append(best_food)
        food_candidates.remove(best_food)
        if best_food in other_candidates:
            other_candidates.remove(best_food)

    # добираем все остальные допустимые точки
    remaining = [i for i in all_candidates if i not in route]

    while True:
        best = pick_best_candidate(
            current_route=route,
            candidates=remaining,
            dist=dist,
            places=places,
            start_index=start_index,
            max_time_hours=max_time_hours,
            max_budget=max_budget,
            speed_kmh=speed_kmh,
        )

        if best is None:
            break

        route.append(best)
        remaining.remove(best)

    return route