import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from googlesearch import search

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8538731213:AAGpXHCmhBXxcUZD7A4-RyI15n8tEpwVTME"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Напиши мне что хочешь найти, и я дам тебе ссылки 🔍"
    )

async def search_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"Ищу: {query}...")

    try:
        results = list(search(query, num_results=5))

        if not results:
            await update.message.reply_text("Ничего не нашёл 😕")
            return

        response = f"🔍 Результаты по запросу: *{query}*\n\n"
        for i, url in enumerate(results, 1):
            response += f"{i}. {url}\n\n"

        await update.message.reply_text(response, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        await update.message.reply_text(f"Ошибка при поиске: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_query))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()