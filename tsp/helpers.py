import math
from typing import List, Tuple, Set, Optional

Edge = Tuple[int, int]


def norm_edge(a: int, b: int) -> Edge:
    return (a, b) if a < b else (b, a)


def tour_to_edges(tour: List[int]) -> Set[Edge]:
    n = len(tour)
    return {norm_edge(tour[i], tour[(i + 1) % n]) for i in range(n)}


def adjacency_list(n: int, edges: Set[Edge]) -> List[List[int]]:
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def single_tour_check(n: int, edges: Set[Edge]) -> bool:
    if len(edges) != n:
        return False

    adj = adjacency_list(n, edges)
    if any(len(adj[v]) != 2 for v in range(n)):
        return False

    seen = set()
    stack = [0]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        stack.extend(adj[v])

    return len(seen) == n


def edges_to_tour(n: int, edges: Set[Edge]) -> Optional[List[int]]:
    if not single_tour_check(n, edges):
        return None

    adj = adjacency_list(n, edges)
    tour = [0]
    prev = -1
    curr = 0

    while True:
        nxt_candidates = [u for u in adj[curr] if u != prev]
        if not nxt_candidates:
            return None
        nxt = nxt_candidates[0]

        if nxt == 0:
            break

        tour.append(nxt)
        prev, curr = curr, nxt

        if len(tour) > n:
            return None

    return tour if len(tour) == n else None


def nearest_neighbor_tour(dist: List[List[float]], start: int = 0) -> List[int]:
    n = len(dist)
    unvisited = set(range(n))
    unvisited.remove(start)

    tour = [start]
    current = start

    while unvisited:
        nxt = min(unvisited, key=lambda x: dist[current][x])
        tour.append(nxt)
        unvisited.remove(nxt)
        current = nxt

    return tour


def tour_length(tour: List[int], dist: List[List[float]]) -> float:
    n = len(tour)
    return sum(dist[tour[i]][tour[(i + 1) % n]] for i in range(n))


def path_length(path: List[int], dist: List[List[float]]) -> float:
    if len(path) < 2:
        return 0.0
    return sum(dist[path[i]][path[i + 1]] for i in range(len(path) - 1))


def build_distance_matrix(points: List[Tuple[float, float]]) -> List[List[float]]:
    n = len(points)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            d = math.hypot(x1 - x2, y1 - y2)
            dist[i][j] = d
            dist[j][i] = d
    return dist