from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# --- Быстрые ответы во время урока ---
# ключ — текст кнопки, значение — что реально отправится в диалог с AI
QUICK_REPLIES = {
    "💡 Пример": "Приведи, пожалуйста, конкретный пример — можно из моей сферы.",
    "🔁 Объясни иначе": "Объясни это по-другому, через другую аналогию или пример.",
    "❓ Не понял": "Я не до конца понял. Можешь разжевать ещё раз проще?",
    "➡️ Дальше": "Понятно, давай дальше.",
}


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🆓 Первый шаг")],
            [KeyboardButton(text="📣 Продвижение"), KeyboardButton(text="💼 Бизнес")],
            [KeyboardButton(text="🤖 Технологии"), KeyboardButton(text="📊 Прогресс")],
            [KeyboardButton(text="📝 Конспекты")],
        ],
        resize_keyboard=True,
        persistent=True,
    )


def lesson_kb() -> ReplyKeyboardMarkup:
    """Клавиатура во время урока — быстрые ответы и пауза."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💡 Пример"), KeyboardButton(text="🔁 Объясни иначе")],
            [KeyboardButton(text="❓ Не понял"), KeyboardButton(text="➡️ Дальше")],
            [KeyboardButton(text="⏸ На паузу")],
        ],
        resize_keyboard=True,
        persistent=True,
    )
