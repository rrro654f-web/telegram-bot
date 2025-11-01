import logging
import os
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, MenuButtonWebApp
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Токен берется из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN не знайдено в змінних середовища!")
    sys.exit(1)

# Текст для описания бота (будет показан при запуске)
BOT_DESCRIPTION = """Ласкаво просимо до нашого магазину, де ви знайдете тільки найкращу техніку Apple — нову та б/у за вигідними цінами! 😊

Відчуйте якість Apple з нашим асортиментом нових та сертифікованих пристроїв! 🍏

Шукаєте надійну техніку Apple? У нас є нові моделі та перевірені пристрої, що задовольнять навіть найвибагливих покупців! 📱

Обирайте нові та сертифіковані продукти Apple — якість і інновації за доступною ціною тільки в нашому магазині! 💻"""

# Текст приветствия с эмодзи
WELCOME_TEXT = """🎉 Ласкаво просимо до нашого магазину!

🌟 Вітаємо вас у нашому магазині — місці, де зручність і вигода завжди поруч!

Ми раді, що ви завітали до нас. Тут ви знайдете великий вибір продукції за привабливими цінами, а також швидкий сервіс і надійну підтримку.

🛍️ **Щоб відкрити магазин**, просто натисніть кнопку "Магазин" нижче. Він відкриється у зручному міні-додатку прямо в Telegram!

🔹 Для вашої зручності ми додали меню, яке відкривається у нижньому кутку чату. Завдяки цьому ви з легкістю знайдете інформацію про оплату, доставку та гарантії.

🔹 Якщо у вас є питання або потрібна допомога у виборі — пишіть нам у Instagram! Посилання на нашу сторінку є в меню.

💬 Ми завжди готові допомогти вам знайти саме те, що вам потрібно!

Дякуємо за ваш вибір та бажаємо приємних покупок! 💛"""

# Ссылка на гифку
GIF_URL = "https://i.gifer.com/3P0Ho.gif"

# URL для Web App
WEB_APP_URL = "https://itconcerent.github.io/markesell/"

async def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    try:
        # Создаем кнопку с Web App
        keyboard = [[
            InlineKeyboardButton(
                "🛍️ Відкрити магазин", 
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Отправляем всё в одном сообщении
        await update.message.reply_animation(
            animation=GIF_URL,
            caption=WELCOME_TEXT,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
        logger.info(f"Отправлено приветственное сообщение пользователю {update.effective_user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

async def shop_command(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /shop для прямого открытия магазина"""
    try:
        keyboard = [[
            InlineKeyboardButton(
                "🛍️ Відкрити магазин", 
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🛍️ Натисніть кнопку нижче, щоб відкрити магазин у міні-додатку:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Ошибка в команде /shop: {e}")

async def menu_command(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /menu для показа основного меню"""
    try:
        keyboard = [
            [InlineKeyboardButton("🛍️ Магазин", web_app=WebAppInfo(url=WEB_APP_URL))],
            [InlineKeyboardButton("📞 Підтримка", url="https://instagram.com")],
            [InlineKeyboardButton("ℹ️ Про нас", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🏪 **Головне меню**\n\nОберіть опцію:",
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Ошибка в команде /menu: {e}")

async def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработчик текстовых сообщений"""
    try:
        text = update.message.text.lower()
        
        if any(word in text for word in ['магазин', 'shop', 'купити', 'товар', 'каталог']):
            keyboard = [[
                InlineKeyboardButton(
                    "🛍️ Відкрити магазин", 
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "🛍️ Ось посилання на наш магазин. Натисніть кнопку, щоб відкрити його у міні-додатку:",
                reply_markup=reply_markup
            )
        else:
            # Для любых других сообщений предлагаем магазин
            keyboard = [[
                InlineKeyboardButton(
                    "🛍️ Відкрити магазин", 
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "🔍 Щоб переглянути наш асортимент, натисніть кнопку нижче:",
                reply_markup=reply_markup
            )
            
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")

async def setup_bot_commands(application: Application):
    """Настройка команд бота для меню"""
    commands = [
        ("start", "Запустити бота"),
        ("shop", "Відкрити магазин"),
        ("menu", "Головне меню")
    ]
    await application.bot.set_my_commands(commands)

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Обработчик ошибок"""
    logger.error(f"Exception while handling an update: {context.error}")

async def post_init(application: Application) -> None:
    """Функция, выполняемая после инициализации бота"""
    try:
        await application.bot.set_my_description(BOT_DESCRIPTION)
        await setup_bot_commands(application)
        
        # Устанавливаем настройки для Web App
        await application.bot.set_chat_menu_button(menu_button=MenuButtonWebApp(
            text="🛍️ Магазин",
            web_app=WebAppInfo(url=WEB_APP_URL)
        ))
        
        logger.info("Настройки бота успешно установлены")
    except Exception as e:
        logger.error(f"Ошибка при установке настроек бота: {e}")

async def post_stop(application: Application) -> None:
    """Функция, выполняемая перед остановкой бота"""
    logger.info("Бот останавливается...")

def main() -> None:
    """Запуск бота"""
    try:
        # Создаем и настраиваем приложение
        application = (
            Application.builder()
            .token(BOT_TOKEN)
            .post_init(post_init)
            .post_stop(post_stop)
            .build()
        )
        
        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("shop", shop_command))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        # Запускаем бота
        logger.info("🤖 Бот успешно запущен и ожидает сообщений...")
        print("🤖 Бот успешно запущен и ожидает сообщений...")
        print("🛍️ Web App будет открываться в мини-приложении для всех пользователей")
        
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
