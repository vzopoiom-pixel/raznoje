import turtle
import math

#  ДАННЫЕ: 5 ближайших звёзд
stars = [
    {"name": "Проксима Центавра", "distance_ly": 4.24},
    {"name": "Альфа Центавра A", "distance_ly": 4.37},
    {"name": "Звезда Барнарда", "distance_ly": 5.96},
    {"name": "Вольф 359", "distance_ly": 7.79},
    {"name": "Лаланд 21185", "distance_ly": 8.29},
]

LIGHT_SPEED_KMH = 1_080_000_000  # скорость света в км/ч
KM_IN_LY = 9_461_000_000_000  # км в одном световом году


def calculate_travel(speed_kmh):
    """Считает время до каждой звезды и выводит рекомендации"""
    print("\n КОСМИЧЕСКИЙ РЕЙНДЖЕР — НАВИГАЦИОННЫЙ ОТЧЁТ")
    print("=" * 55)

    needs_upgrade = False
    required_speeds = []

    for star in stars:
        distance_km = star["distance_ly"] * KM_IN_LY
        time_hours = distance_km / speed_kmh
        time_years = time_hours / 8760  # часов в году

        print(f"\n {star['name']}")
        print(f"   Расстояние : {star['distance_ly']} св. лет")
        print(f"   Время пути : {time_years:.1f} лет  ({time_hours:,.0f} ч)")

        if time_years > 10:
            needs_upgrade = True
            # Скорость, нужная чтобы добраться за меньше чем за 10 лет
            needed = distance_km / (10 * 8760)
            required_speeds.append((star["name"], needed))
            print(f" Более 10 лет! Рекомендуется улучшить корабль.")
        else:
            print(f" Вы доберётесь менее чем за 10 лет!")

    # РЕКОМЕНДАЦИЯ
    if needs_upgrade:
        print("\n" + "=" * 55)
        print(" РЕКОМЕНДАЦИЯ ПО УЛУЧШЕНИЮ КОРАБЛЯ:")
        max_needed = max(speed for _, speed in required_speeds)
        print(f"   Минимальная скорость для всех звезд < 10 лет:")
        print(f"   ➡  {max_needed:,.0f} км/ч")
        print(f"   (это {max_needed / LIGHT_SPEED_KMH * 100:.4f}% скорости света)")
        for name, speed in required_speeds:
            print(f"\n   • {name}: нужно ≥ {speed:,.0f} км/ч")
    else:
        print("\n Ваш корабль достаточно быстр для всех звёзд!")


#ГЛАВНАЯ ПРОГРАММА
print(" Добро пожаловать, космический рейнджер!")
speed_input = float(input("Введите скорость вашего корабля (км/ч): "))
calculate_travel(speed_input)

