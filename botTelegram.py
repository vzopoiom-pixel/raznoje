# ниже пишкм все нам нужные библеотеки до 8 строчки
import logging
import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler что это все только в краткости



#===============================================================================================================
#Эти компоненты являются частью библиотеки python-telegram-bot для создания ботов на Python. Вот краткий обзор: 
#python-telegram-bot docs
#python-telegram-bot docs
#Основные компоненты

#import os — это загрузка встроенного модуля для работы с операционной системой.
#InlineKeyboardButton: Создает отдельную кнопку, которая прикрепляется прямо к сообщению.
#InlineKeyboardMarkup: Собирает кнопки в сетку (клавиатуру) для отправки.
#pplication: Основной класс для запуска бота и управления его жизненным циклом.
#CommandHandler: Реагирует на команды пользователя (например, /start).
#MessageHandler: Обрабатывает обычные текстовые сообщения или другие типы данных.
#filters: Набор условий для фильтрации сообщений (например, только текст, только фото).
#ContextTypes: Позволяет передавать контекст (данные) между функциями бота.
#CallbackQueryHandler: Обрабатывает нажатия на inline-кнопки (чтобы бот понял, что пользователь нажал).
#===============================================================================================================

#logging.basicConfig : это базовая функция позволяющия реагировать на команды пользователя и настраивает модули

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ниже у нас важная деталь бота а именно его токен
BOT_TOKEN = "8648822743:AAHRQk12BQuqOn7r9yXumbdRya4OC0uSJvk"
# это табличка текстовая
NOTES_FILE = "notes.json"


# то что создает и вызывает функцию
def load_notes():
    try:
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {}


def save_notes(notes):
    try:
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка сохранения: {e}")


# бот запускается при команде /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(
            "Привет! 👋\n\n"
            "Команды:\n"
            "/add текст - добавить заметку\n"
            "/list - показать заметки (с кнопками удаления!)\n"
            "/delete номер - удалить по номеру\n"
            "/help - справка"
        )
    except Exception as e:  # выдает ошибку если не правильно
        logger.error(f"Ошибка в start: {e}")


# главные функции для бота которые  водить юзер
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text(
            "📋 СПРАВКА:\n\n"
            "/add [текст] - Добавить заметку\n"
            "/list - Показать все заметки с кнопками удаления 🗑️\n"
            "/delete [номер] - Удалить заметку по номеру\n"
            "/clear - Удалить все заметки сразу"
        )
    except Exception as e:
        logger.error(f"Ошибка в help: {e}")


async def add_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = str(update.effective_user.id)

        if not context.args:
            await update.message.reply_text("Использование: /add [текст]")
            return

        text = " ".join(context.args)
        notes = load_notes()

        if user_id not in notes:
            notes[user_id] = []

        notes[user_id].append({
            "text": text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        save_notes(notes)
        await update.message.reply_text(f"✅ Заметка добавлена:\n📝 {text}")

    except Exception as e:
        logger.error(f"Ошибка в add: {e}")
        await update.message.reply_text(f"❌ Ошибка: {e}")


async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = str(update.effective_user.id)
        notes = load_notes()
        user_notes = notes.get(user_id, [])

        if not user_notes:
            await update.message.reply_text("📭 Заметок нет!")
            return

        # Отправляем каждую заметку отдельно с кнопкой удаления
        for i, note in enumerate(user_notes):
            # Создаем кнопку удаления
            keyboard = [
                [InlineKeyboardButton("🗑️ Удалить", callback_data=f"delete_{i}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            message_text = f"📌 Заметка #{i + 1}\n\n📝 {note['text']}\n⏰ {note['date']}"

            await update.message.reply_text(
                message_text,
                reply_markup=reply_markup
            )
    # отвечает за ошибку
    except Exception as e:
        logger.error(f"Ошибка в list: {e}")
        await update.message.reply_text(f"❌ Ошибка: {e}")


async def delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка нажатия кнопки удаления"""
    try:
        query = update.callback_query
        user_id = str(query.from_user.id)

        # Получаем индекс заметки из callback_data
        idx = int(query.data.split("_")[1])

        notes = load_notes()
        user_notes = notes.get(user_id, [])

        # если нету заметки
        if idx < 0 or idx >= len(user_notes):
            await query.answer("❌ Заметка не найдена!", show_alert=True)
            return

        # Удаляем заметку
        deleted_text = user_notes[idx]["text"]
        user_notes.pop(idx)
        notes[user_id] = user_notes
        save_notes(notes)

        # Отвечаем пользователю
        await query.answer()
        await query.edit_message_text(
            text=f"🗑️ УДАЛЕНО!\n\nБыла заметка:\n📝 {deleted_text}"
        )

    except Exception as e:
        logger.error(f"Ошибка в delete_callback: {e}")
        await query.answer(f"❌ Ошибка: {e}", show_alert=True)


async def delete_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Удаление по номеру через команду"""
    try:
        user_id = str(update.effective_user.id)

        if not context.args:
            await update.message.reply_text("Использование: /delete [номер]")
            return

        try:
            idx = int(context.args[0]) - 1
        except:
            await update.message.reply_text("Введи номер цифрой!")
            return

        notes = load_notes()
        user_notes = notes.get(user_id, [])

        if idx < 0 or idx >= len(user_notes):
            await update.message.reply_text("❌ Неверный номер!")
            return

        deleted = user_notes[idx]["text"]
        user_notes.pop(idx)
        notes[user_id] = user_notes
        save_notes(notes)

        await update.message.reply_text(f"🗑️ Удалено:\n📝 {deleted}")

    except Exception as e:
        logger.error(f"Ошибка в delete: {e}")
        await update.message.reply_text(f"❌ Ошибка: {e}")


# удаляет все заметки созадные пользователем
async def clear_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Удаление всех заметок с подтверждением"""
    try:
        user_id = str(update.effective_user.id)
        notes = load_notes()

        if user_id not in notes or len(notes[user_id]) == 0:
            await update.message.reply_text("📭 Заметок нет!")
            return

        count = len(notes[user_id])

        # Создаем кнопки подтверждения при удалении заметок
        keyboard = [
            [
                InlineKeyboardButton("✅ Да, удалить все", callback_data="confirm_clear_yes"),
                InlineKeyboardButton("❌ Отмена", callback_data="confirm_clear_no")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"⚠️ Ты уверен? Это удалит все {count} заметок!\n\n"
            f"Это действие необратимо!",
            reply_markup=reply_markup
        )
    # выдает ошибку если что то не правильно
    except Exception as e:
        logger.error(f"Ошибка в clear: {e}")
        await update.message.reply_text(f"❌ Ошибка: {e}")


async def clear_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка подтверждения удаления всех заметок"""
    try:
        query = update.callback_query
        user_id = str(query.from_user.id)

        if query.data == "confirm_clear_yes":
            notes = load_notes()
            count = len(notes.get(user_id, []))
            notes[user_id] = []
            save_notes(notes)

            await query.answer()
            await query.edit_message_text(
                text=f"🗑️ Все {count} заметок удалены!"
            )
        else:
            await query.answer()
            await query.edit_message_text(
                text="❌ Отменено. Заметки сохранены."
            )

    except Exception as e:
        logger.error(f"Ошибка в clear_callback: {e}")
        await query.answer(f"❌ Ошибка: {e}", show_alert=True)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сохранение обычных сообщений как заметок"""
    try:
        user_id = str(update.effective_user.id)
        text = update.message.text

        notes = load_notes()
        if user_id not in notes:
            notes[user_id] = []

        notes[user_id].append({
            "text": text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        save_notes(notes)
        await update.message.reply_text(
            f"✅ Заметка добавлена:\n📝 {text}\n\n"
            f"Напиши /list чтобы увидеть все заметки"
        )

    except Exception as e:
        logger.error(f"Ошибка в handle_text: {e}")


async def error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Ошибка: {context.error}")


def main():
    print("⏳ Бот запускается...")
    app = Application.builder().token(BOT_TOKEN).build()

    print("➕ Добавляю обработчики...")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("add", add_cmd))
    app.add_handler(CommandHandler("list", list_cmd))
    app.add_handler(CommandHandler("delete", delete_cmd))
    app.add_handler(CommandHandler("clear", clear_cmd))

    # Обработчики кнопок
    app.add_handler(CallbackQueryHandler(delete_callback, pattern="^delete_"))
    app.add_handler(CallbackQueryHandler(clear_callback, pattern="^confirm_clear_"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_error_handler(error)

    print("✅ Бот готов! Запускаю polling...")
    print("🤖 БОТ ЗАПУЩЕН И РАБОТАЕТ!")
    print("=" * 50)
    # конец кода для бота
    try:
        app.run_polling()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == '__main__':
    main()
