from datetime import datetime
import os


def simple_notes_app(filename):
    """
    Простое приложение для сохранения заметок

    Пользователь вводит текст, который сохраняется в файл.
    Для завершения нужно ввести 'готово'
    """
    if not filename.endswith('.txt'):
        filename += '.txt'

    print("\n" + "=" * 60)
    print(" ПРИЛОЖЕНИЕ 'ЗАМЕТКИ'")
    print("=" * 60)
    print(f"Файл для сохранения: {filename}")
    print("\nВводите заметки. Для завершения напишите 'готово'")
    print("=" * 60 + "\n")

    notes = []
    note_number = 1

    # Основной цикл ввода
    while True:
        user_input = input(f"Заметка #{note_number}: ").strip()

        # Проверка команды выхода
        if user_input.lower() in ['готово', 'exit', 'quit']:
            break

        # Пропускаем пустые строки
        if not user_input:
            print("  Заметка пуста. Попробуйте снова.\n")
            continue

        # Добавляем заметку с временной меткой
        timestamp = datetime.now().strftime('%H:%M:%S')
        note_with_time = f"[{timestamp}] {user_input}"
        notes.append(note_with_time)

        print(f" Заметка #{note_number} добавлена!\n")
        note_number += 1

    # Сохранение в файл
    print("\n⏳ Сохранение заметок в файл...")

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Заголовок файла
            f.write("╔" + "═" * 58 + "╗\n")
            f.write("║" + "   ФАЙЛ ЗАМЕТОК ".center(58) + "║\n")
            f.write("╚" + "═" * 58 + "╝\n\n")

            # Информация о файле
            f.write(f"Дата создания: {datetime.now().strftime('%d.%m.%Y в %H:%M:%S')}\n")
            f.write(f"Всего заметок: {len(notes)}\n")
            f.write("─" * 60 + "\n\n")

            # Сохраняем заметки
            if notes:
                for idx, note in enumerate(notes, 1):
                    f.write(f"{idx}. {note}\n")
            else:
                f.write("Заметок не добавлено.\n")

            f.write("\n" + "─" * 60 + "\n")
            f.write("Конец файла\n")

        # Выводим результат
        print(f"Файл '{filename}' успешно создан!\n")

        print("=" * 60)
        print("РЕЗУЛЬТАТЫ:")
        print("=" * 60)
        print(f" Заметок добавлено: {len(notes)}")
        print(f" Файл: {filename}")

        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            print(f"  Размер файла: {file_size} байт ({file_size / 1024:.2f} КБ)")

        print("=" * 60)
        print("\n Спасибо за использование приложения!\n")

    except Exception as e:
        print(f" Ошибка при сохранении файла: {e}")


def main():
    """Главная функция"""
    # Получаем название файла от пользователя
    while True:
        filename = input(
            " Введите название файла для сохранения заметок\n   (без расширения, будет добавлено .txt): ").strip()

        if not filename:
            print(" Название не может быть пустым!\n")
            continue

        break

    # Запускаем приложение
    simple_notes_app(filename)


if __name__ == "__main__":
    main()