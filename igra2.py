import random


def get_computer_choice():
    """Компьютер выбирает случайный ход"""
    choices = ['камень', 'ножницы', 'бумага', 'ящерица', 'спок']
    return random.choice(choices)


def determine_winner(player_choice, computer_choice):
    """
    Определяет победителя в игре "Камень, ножницы, бумага, ящерица, Спок"

    Правила:
    - Камень разбивает ножницы и давит ящерицу
    - Ножницы режут бумагу и обезглавливают ящерицу
    - Бумага обвивает камень и опровергает Спока
    - Ящерица ест бумагу и отравляет Спока
    - Спок ломает ножницы и испаряет камень

    Возвращает: 1 - игрок победил, -1 - компьютер победил, 0 - ничья
    """

    if player_choice == computer_choice:
        return 0

    # Каждый выбор бьет два других
    winning_moves = {
        'камень': ['ножницы', 'ящерица'],
        'ножницы': ['бумага', 'ящерица'],
        'бумага': ['камень', 'спок'],
        'ящерица': ['бумага', 'спок'],
        'спок': ['ножницы', 'камень']
    }

    if computer_choice in winning_moves[player_choice]:
        return 1
    else:
        return -1


def get_win_description(player_choice, computer_choice):
    """Выводит описание того, как игрок победил"""
    descriptions = {
        ('камень', 'ножницы'): "Камень разбивает ножницы!",
        ('камень', 'ящерица'): "Камень давит ящерицу!",
        ('ножницы', 'бумага'): "Ножницы режут бумагу!",
        ('ножницы', 'ящерица'): "Ножницы обезглавливают ящерицу!",
        ('бумага', 'камень'): "Бумага обвивает камень!",
        ('бумага', 'спок'): "Бумага опровергает Спока!",
        ('ящерица', 'бумага'): "Ящерица ест бумагу!",
        ('ящерица', 'спок'): "Ящерица отравляет Спока!",
        ('спок', 'ножницы'): "Спок ломает ножницы!",
        ('спок', 'камень'): "Спок испаряет камень!"
    }
    return descriptions.get((player_choice, computer_choice), "Вы победили!")


def play_round():
    """Проводит один раунд игры"""
    print("\n--- Новый раунд ---")

    valid_choices = ['камень', 'ножницы', 'бумага', 'ящерица', 'спок']

    # Ввод выбора игрока
    while True:
        player_choice = input("Ваш выбор (камень/ножницы/бумага/ящерица/спок): ").lower().strip()
        if player_choice in valid_choices:
            break
        print("Ошибка! Введите: камень, ножницы, бумага, ящерица или спок")

    computer_choice = get_computer_choice()

    print(f"Вы выбрали: {player_choice}")
    print(f"Компьютер выбрал: {computer_choice}")

    result = determine_winner(player_choice, computer_choice)

    if result == 0:
        print("Ничья!")
        return 0
    elif result == 1:
        print(get_win_description(player_choice, computer_choice))
        print("Вы победили этот раунд! ")
        return 1
    else:
        print(get_win_description(computer_choice, player_choice))
        print("Компьютер победил этот раунд.")
        return -1


def play_series():
    """Проводит серию игр до трех побед"""
    player_wins = 0
    computer_wins = 0

    print("\n" + "=" * 60)
    print(" Добро пожаловать в игру 'Камень, ножницы, бумага, ящерица, Спок'!")
    print("Первый, кто выиграет 3 раунда, выигрывает серию!")
    print("=" * 60)

    print("\n Правила:")
    print("  • Камень разбивает ножницы и давит ящерицу")
    print("  • Ножницы режут бумагу и обезглавливают ящерицу")
    print("  • Бумага обвивает камень и опровергает Спока")
    print("  • Ящерица ест бумагу и отравляет Спока")
    print("  • Спок ломает ножницы и испаряет камень")

    while player_wins < 3 and computer_wins < 3:
        result = play_round()

        if result == 1:
            player_wins += 1
        elif result == -1:
            computer_wins += 1

        print(f"\nСчёт: Вы {player_wins} - {computer_wins} Компьютер")

    print("\n" + "=" * 60)
    if player_wins == 3:
        print(" Поздравляем! Вы выиграли серию!")
    else:
        print(" Компьютер выиграл серию!")
    print("=" * 60)

    return player_wins == 3


def main():
    """Главная функция - управляет игровыми сеансами"""
    play_again = True

    while play_again:
        play_series()

        while True:
            response = input("\nХотите сыграть еще? (да/нет): ").lower().strip()
            if response in ['да', 'yes', 'y', 'д']:
                play_again = True
                break
            elif response in ['нет', 'no', 'n', 'н']:
                play_again = False
                break
            else:
                print("Пожалуйста, ответьте 'да' или 'нет'")

    print("\nСпасибо за игру! До встречи! ")


if __name__ == "__main__":
    main()