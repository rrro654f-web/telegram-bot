import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackContext
from dotenv import load_dotenv

# Завантажуємо змінні середовища
load_dotenv()

# Налаштування логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Отримання токена з змінних середовища
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logging.error("❌ BOT_TOKEN не знайдено! Додайте його в змінні середовища.")
    exit(1)

# ... (інший ваш код залишається без змін) ...

def main() -> None:
    """Запуск бота"""
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        
        # Налаштування опису бота
        bot = application.bot
        bot.set_my_description(BOT_DESCRIPTION)
        
        logging.info("🤖 Бот запускається на Railway...")
        application.run_polling()
        
    except Exception as e:
        logging.error(f"Помилка запуску: {e}")

if __name__ == '__main__':
    main()
