import random


#  Правда или Действие


truths = [
    "Что самое неловкое, что с тобой случалось?",
    "Какой твой самый большой страх?",
    "Что ты делаешь, когда думаешь, что никто не смотрит?",
    "Какой поступок ты больше всего хотел бы не совершать?",
    "Что тебя раздражает в людях?",
]

dares = [
    "Спой куплет любой песни как можно громче!",
    "Сделай 10 приседаний прямо сейчас.",
    "Изобрази животное на выбор других игроков.",
    "Говори шёпотом следующие 2 минуты.",
    "Станцуй без музыки 30 секунд.",
]


def game_truth_or_dare():
    print("\n правда или действие ")
    while True:
        choice = input("\nВыберите: (1) Правда  (2) Действие  (0) Выход: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            print(" Правда:", random.choice(truths))
        elif choice == "2":
            print(" Действие:", random.choice(dares))
        else:
            print("Некорректный выбор — повторяем вопрос!")
            continue

        result = input("Выполнил(а)? (да/нет): ").strip().lower()
        if result != "да":
            print("⚠️  Не выполнено — вопрос повторяется!")
            if choice == "1":
                print("❓ Правда:", random.choice(truths))
            else:
                print("🔥 Действие:", random.choice(dares))



# суперы ну второе задание


heroes = [
    "Человек-паук", "Железный человек", "Тор", "Чёрная вдова",
    "Капитан Америка", "Халк", "Доктор Стрэндж", "Ванда",
    "Человек-муравей", "Чёрная пантера", "Бэтмен", "Супермен",
    "Чудо-женщина", "Флэш", "Аквамен",
]


def game_superheroes():
    print("\n выборы ролей")
    players = []

    while True:
        name = input("Введите имя игрока (или Enter для завершения): ").strip()
        if name == "":
            break
        if len(players) >= len(heroes):
            print(f"Максимум {len(heroes)} игроков!")
            break
        players.append(name)

    if not players:
        print("Игроков нет!")
        return

    assigned = random.sample(heroes, len(players))

    print("\n--- Результаты ---")
    for player, hero in zip(players, assigned):
        print(f"  {player}  →  {hero}")



# меню и выбор действий


def main():
    while True:
        print("\nМенюшка")
        print("1. Правда или Действие")
        print("2. Супергерои")
        print("0. Выход")
        choice = input("Выбор: ").strip()

        if choice == "1":
            game_truth_or_dare()
        elif choice == "2":
            game_superheroes()
        elif choice == "0":
            print("Пока!")
            break
        else:
            print("Неверный выбор, попробуй снова.")


main()