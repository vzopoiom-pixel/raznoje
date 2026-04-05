import os
from pathlib import Path


def get_file_info(file_path):
    """Получает информацию о файле"""
    try:
        stat_info = os.stat(file_path)
        size = stat_info.st_size
        return {
            'type': 'Файл',
            'size': size,
            'size_kb': size / 1024,
            'exists': True
        }
    except Exception as e:
        return {'type': 'Файл', 'error': str(e)}


def get_dir_info(dir_path):
    """Получает информацию о директории"""
    try:
        items = os.listdir(dir_path)
        return {
            'type': 'Директория',
            'count': len(items),
            'exists': True,
            'items': items
        }
    except Exception as e:
        return {'type': 'Директория', 'error': str(e)}


def display_path_info(path_str):
    """Выводит информацию о пути (файл или директория)"""
    path = Path(path_str)

    print(f"\n{'=' * 60}")
    print(f"Информация о пути: {path}")
    print(f"{'=' * 60}")

    if not path.exists():
        print(f" Ошибка: Путь не существует!")
        return

    if path.is_file():
        info = get_file_info(path)
        print(f"Тип: {info['type']}")
        print(f"Размер: {info['size']} байт ({info['size_kb']:.2f} КБ)")

    elif path.is_dir():
        info = get_dir_info(path)
        print(f"Тип: {info['type']}")
        print(f"Количество элементов: {info['count']}")
        print(f"\n Содержимое директории:")

        for item in sorted(info['items']):
            item_path = path / item
            if item_path.is_dir():
                print(f"{item}/ (директория)")
            else:
                size = os.path.getsize(item_path)
                print(f" {item} ({size} байт)")


def main():

    while True:
        print("\n" + "-" * 60)
        user_input = input("Введите путь к файлу или директории (или 'выход' для выхода): ").strip()

        if user_input.lower() in ['выход', 'exit', 'quit']:
            print("\nДо свидания!")
            break

        if not user_input:
            print(" Ошибка: путь не может быть пустым!")
            continue

        display_path_info(user_input)


if __name__ == "__main__":
    main()