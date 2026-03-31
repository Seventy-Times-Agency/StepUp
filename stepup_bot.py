from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# ==========================
# Настройки бота
# ==========================
API_TOKEN = "BOT_TOKEN"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ==========================
# Клавиатура
# ==========================
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Продолжить"))

# ==========================
# Хэндлер на команду /start
# ==========================
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    text = (
        "Привет! 👋 Добро пожаловать в StepUp!\n\n"
        "Мы — команда, которая делает обучение маркетингу, SMM, таргету и "
        "автоматизации продаж простым и понятным. 🚀\n\n"
        "С помощью StepUp ты:\n"
        "- Поймёшь, как работает современный маркетинг и автоматизация\n"
        "- Узнаешь, как управлять лидами и продажами, даже если раньше этим не занимался\n"
        "- Получишь практический опыт, а не только теорию\n\n"
        "🎯 Нажми «Продолжить», чтобы начать первый ознакомительный модуль!"
    )
    await message.answer(text, reply_markup=keyboard)

# ==========================
# Хэндлер на кнопку "Продолжить"
# ==========================
@dp.message_handler(lambda message: message.text == "Продолжить")
async def continue_module(message: types.Message):
    text = "Отлично! 🌟 Дальше пойдёт первый модуль (пока заглушка)."
    await message.answer(text)

# ==========================
# Запуск бота
# ==========================
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
