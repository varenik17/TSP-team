import random
from typing import List, Tuple, Set, Optional
from tsp import *

Edge = Tuple[int, int]

# реализация LKH для симметричной матрицы расстояний (из статьи)
class LinKernighanSolver:

    def __init__(
            self,
            dist: List[List[float]],
            max_depth: int = 5,
            candidate_count: int = 8,
            random_seed: Optional[int] = None,
    ) -> None:
        self.dist = dist
        self.n = len(dist)
        self.max_depth = max_depth
        self.candidate_count = candidate_count
        self.random = random.Random(random_seed)

        self.candidates = self._build_candidates()

    # выбираем заранее ближайших соседей для вершин
    def _build_candidates(self) -> List[List[int]]:
        candidates = []
        for i in range(self.n):
            order = sorted(
                (j for j in range(self.n) if j != i),
                key=lambda j: self.dist[i][j]
            )
            candidates.append(order[:self.candidate_count])
        return candidates

    # улучшение тура по итерациям
    def solve(self, initial_tour: Optional[List[int]] = None) -> Tuple[List[int], float]:
        if self.n < 4:
            raise ValueError("Используйте для LKH n >= 4")

        if initial_tour is None:
            start = self.random.randrange(self.n)
            tour = nearest_neighbor_tour(self.dist, start=start)
        else:
            if sorted(initial_tour) != list(range(self.n)):
                raise ValueError("initial_tour должен быть перестановкой")
            tour = initial_tour[:]

        improved = True
        while improved:
            improved = False

            t1_order = tour[:]
            self.random.shuffle(t1_order)

            for t1 in t1_order:
                new_tour = self._try_improve_from_t1(tour, t1)
                if new_tour is not None:
                    if tour_length(new_tour, self.dist) + 1e-12 < tour_length(tour, self.dist):
                        tour = new_tour
                        improved = True
                        break

        return tour, tour_length(tour, self.dist)

    # шаги из алгоритма статьи
    def _try_improve_from_t1(self, tour: List[int], t1: int) -> Optional[List[int]]:
        base_edges = tour_to_edges(tour)
        neighbors = self._tour_neighbors(tour)

        for t2 in neighbors[t1]:
            x1 = norm_edge(t1, t2)

            removed = {x1}
            added = set()

            used_x = {x1}
            used_y = set()

            for t3 in self.candidates[t2]:
                y1 = norm_edge(t2, t3)

                if t3 == t1:
                    continue
                if y1 in base_edges:
                    continue

                g1 = self.dist[t1][t2] - self.dist[t2][t3]
                if g1 <= 0:
                    continue

                added.add(y1)
                used_y.add(y1)

                result = self._search(
                    base_tour=tour,
                    base_edges=base_edges,
                    t1=t1,
                    last_vertex=t3,
                    gain=g1,
                    removed=removed.copy(),
                    added=added.copy(),
                    used_x=used_x.copy(),
                    used_y=used_y.copy(),
                    depth=1,
                )
                if result is not None:
                    return result

                added.remove(y1)
                used_y.remove(y1)

        return None

    def _search(
            self,
            base_tour: List[int],
            base_edges: Set[Edge],
            t1: int,
            last_vertex: int,
            gain: float,
            removed: Set[Edge],
            added: Set[Edge],
            used_x: Set[Edge],
            used_y: Set[Edge],
            depth: int,
    ) -> Optional[List[int]]:

        current_edges = (base_edges - removed) | added
        neighbors = self._edge_neighbors(current_edges)

        for t_next in neighbors[last_vertex]:
            xi = norm_edge(last_vertex, t_next)

            if xi in used_y:
                continue

            removed2 = removed | {xi}
            used_x2 = used_x | {xi}

            closing_edge = norm_edge(t_next, t1)

            if t_next != t1 and closing_edge not in current_edges:
                candidate_edges = (base_edges - removed2) | added | {closing_edge}

                if single_tour_check(self.n, candidate_edges):
                    candidate_tour = edges_to_tour(self.n, candidate_edges)
                    if candidate_tour is not None:
                        old_len = tour_length(base_tour, self.dist)
                        new_len = tour_length(candidate_tour, self.dist)
                        if new_len + 1e-12 < old_len:
                            return candidate_tour

            if depth >= self.max_depth:
                continue

            for t_new in self.candidates[t_next]:
                yi = norm_edge(t_next, t_new)

                if t_new == t1:
                    continue
                if yi in current_edges:
                    continue
                if yi in used_x2:
                    continue

                new_gain = gain + self.dist[xi[0]][xi[1]] - self.dist[yi[0]][yi[1]]
                if new_gain <= 0:
                    continue

                added2 = added | {yi}
                used_y2 = used_y | {yi}

                result = self._search(
                    base_tour=base_tour,
                    base_edges=base_edges,
                    t1=t1,
                    last_vertex=t_new,
                    gain=new_gain,
                    removed=removed2,
                    added=added2,
                    used_x=used_x2,
                    used_y=used_y2,
                    depth=depth + 1,
                )
                if result is not None:
                    return result

        return None

    # соседи в текущем туре
    def _tour_neighbors(self, tour: List[int]) -> List[List[int]]:
        n = len(tour)
        pos = [0] * n
        for i, v in enumerate(tour):
            pos[v] = i

        neighbors = [[] for _ in range(n)]
        for v in range(n):
            i = pos[v]
            neighbors[v] = [
                tour[(i - 1) % n],
                tour[(i + 1) % n],
            ]
        return neighbors

    # соседи по ребрам
    def _edge_neighbors(self, edges: Set[Edge]) -> List[List[int]]:
        return adjacency_list(self.n, edges)



