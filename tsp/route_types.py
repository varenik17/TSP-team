from dataclasses import dataclass


@dataclass(frozen=True)
class Place:
    id: int
    name: str
    category: str
    visit_cost: float
    visit_time_hours: float