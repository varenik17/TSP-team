from typing import List
from .route_types import Place


FOOD_CATEGORIES = {"cafe", "restaurant"}

def travel_time_hours(distance_km: float, speed_kmh: float) -> float:
    return distance_km / speed_kmh


def route_travel_distance(route: List[int], dist: List[List[float]]) -> float:
    if len(route) < 2:
        return 0.0
    return sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))


def route_travel_time(route: List[int], dist: List[List[float]], speed_kmh: float) -> float:
    distance = route_travel_distance(route, dist)
    return travel_time_hours(distance, speed_kmh)


def route_visit_time(route: List[int], places: List[Place], start_index: int) -> float:
    total = 0.0
    for idx in route:
        if idx != start_index:
            total += places[idx].visit_time_hours
    return total


def route_cost(route: List[int], places: List[Place], start_index: int) -> float:
    total = 0.0
    for idx in route:
        if idx != start_index:
            total += places[idx].visit_cost
    return total


def route_total_time(
    route: List[int],
    dist: List[List[float]],
    places: List[Place],
    speed_kmh: float,
    start_index: int,
) -> float:
    return route_travel_time(route, dist, speed_kmh) + route_visit_time(route, places, start_index)


def is_feasible_route(
    route: List[int],
    dist: List[List[float]],
    places: List[Place],
    speed_kmh: float,
    max_time_hours: float,
    max_budget: float,
    start_index: int,
) -> bool:
    total_time = route_total_time(route, dist, places, speed_kmh, start_index)
    total_cost = route_cost(route, places, start_index)
    return total_time <= max_time_hours and total_cost <= max_budget



def is_food_place(place: Place) -> bool:
    return place.category in FOOD_CATEGORIES


def food_count(route: List[int], places: List[Place], start_index: int) -> int:
    count = 0
    for idx in route:
        if idx != start_index and is_food_place(places[idx]):
            count += 1
    return count


def has_two_nonconsecutive_food_stops(route: List[int], places: List[Place], start_index: int) -> bool:
    food_positions = []

    for pos, idx in enumerate(route):
        if idx != start_index and is_food_place(places[idx]):
            food_positions.append(pos)

    if len(food_positions) < 2:
        return False

    for i in range(len(food_positions)):
        for j in range(i + 1, len(food_positions)):
            if abs(food_positions[j] - food_positions[i]) > 1:
                return True

    return False