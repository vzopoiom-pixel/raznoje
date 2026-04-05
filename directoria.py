import os
from pathlib import Path


def build_tree(directory, prefix="", is_last=True, max_depth=10, current_depth=0):
    """
    Рекурсивно строит древовидную структуру директорий и файлов

    Args:
        directory: путь к директории
        prefix: префикс для отступа
        is_last: является ли это последним элементом в списке
        max_depth: максимальная глубина рекурсии
        current_depth: текущая глубина
    """

    if current_depth >= max_depth:
        return

    try:
        items = sorted(os.listdir(directory))
    except PermissionError:
        print(f"{prefix} Доступ запрещен")
        return

    # директории и файлы
    dirs = [item for item in items if os.path.isdir(os.path.join(directory, item))]
    files = [item for item in items if os.path.isfile(os.path.join(directory, item))]

    all_items = dirs + files

    for index, item in enumerate(all_items):
        item_path = os.path.join(directory, item)
        is_last_item = (index == len(all_items) - 1)

        #  символы для рисования дерева
        current_prefix = "└── " if is_last_item else "├── "
        next_prefix = prefix + ("    " if is_last_item else "│   ")

        if os.path.isdir(item_path):
            print(f"{prefix}{current_prefix} {item}/")
            build_tree(item_path, next_prefix, is_last_item, max_depth, current_depth + 1)
        else:
            size = os.path.getsize(item_path)
            print(f"{prefix}{current_prefix} {item} ({size} байт)")


def display_tree(root_path):
    """Выводит древовидную структуру для заданного пути"""
    path = Path(root_path)

    if not path.exists():
        print(f"Ошибка: Путь '{root_path}' не существует!")
        return

    if not path.is_dir():
        print(f"Ошибка: '{root_path}' не является директорией!")
        return

    print(f"\n{'=' * 60}")
    print(f"Структура директории: {root_path}")
    print(f"{'=' * 60}\n")
    print(f" {path.name}/")

    build_tree(str(path))


def count_items(directory, max_depth=10, current_depth=0):
    """Подсчитывает количество файлов и директорий"""
    if current_depth >= max_depth:
        return {'dirs': 0, 'files': 0}

    try:
        items = os.listdir(directory)
    except PermissionError:
        return {'dirs': 0, 'files': 0}

    dirs = 0
    files = 0

    for item in items:
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            dirs += 1
            sub_count = count_items(item_path, max_depth, current_depth + 1)
            dirs += sub_count['dirs']
            files += sub_count['files']
        else:
            files += 1

    return {'dirs': dirs, 'files': files}


def main():


    while True:
        print("\n" + "-" * 60)
        user_input = input("Введите путь к директории (или 'выход' для выхода): ").strip()

        if user_input.lower() in ['выход', 'exit', 'quit']:
            print("\nДо свидания!")
            break

        if not user_input:
            print(" Ошибка: путь не может быть пустым!")
            continue

        display_tree(user_input)

        # Выводим статистику
        if os.path.exists(user_input) and os.path.isdir(user_input):
            stats = count_items(user_input)
            print(f"\n Статистика:")
            print(f"   Директорий: {stats['dirs']}")
            print(f"   Файлов: {stats['files']}")


if __name__ == "__main__":
    main()