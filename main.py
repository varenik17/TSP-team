from tsp import Place, build_tourist_route


def main() -> None:
    places = [
        Place(0, "Старт: отель", "start", 0.0, 0.0),
        Place(1, "Музей истории", "museum", 0.0, 1.0),
        Place(2, "Кафе Чак-Чак", "cafe", 500.0, 1.0),
        Place(3, "Памятник паровозу", "attraction", 0.0, 0.25),
        Place(4, "Ресторан Казани", "restaurant", 1200.0, 1.2),
        Place(5, "Центр развития Казани", "historic_site", 400.0, 1.0),
        Place(6, "Зеленый парк", "park", 0.0, 1.0),
    ]

    dist = [
        [0.0, 1.2, 1.0, 0.5, 2.0, 2.3, 1.5],
        [1.2, 0.0, 0.6, 1.0, 1.5, 1.8, 1.0],
        [1.0, 0.6, 0.0, 1.1, 1.4, 2.0, 1.3],
        [0.5, 1.0, 1.1, 0.0, 2.1, 2.4, 1.6],
        [2.0, 1.5, 1.4, 2.1, 0.0, 1.0, 1.3],
        [2.3, 1.8, 2.0, 2.4, 1.0, 0.0, 0.9],
        [1.5, 1.0, 1.3, 1.6, 1.3, 0.9, 0.0],
    ]

    result = build_tourist_route(
        dist=dist,
        places=places,
        start_index=0,
        max_time_hours=5.0,
        max_budget=5000.0,
        speed_kmh=5.0,
    )

    print("Итоговый маршрут:", result["route_names"])
    print("Итоговая стоимость:", round(result["total_cost"], 2))
    print("Итоговое время:", round(result["total_time_hours"], 2))
    print("Правило еды выполнено:", result["food_rule_ok"])


if __name__ == "__main__":
    main()