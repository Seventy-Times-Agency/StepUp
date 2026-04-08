from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from content.courses import COURSES


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Курсы", callback_data="courses")],
        [InlineKeyboardButton(text="📊 Мой прогресс", callback_data="progress")],
    ])


def courses_list_kb() -> InlineKeyboardMarkup:
    buttons = []
    for course in COURSES:
        if course["is_free"]:
            label = f"{course['emoji']} {course['title']} — БЕСПЛАТНО"
        else:
            label = f"{course['emoji']} {course['title']} — Скоро"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"course:{course['id']}")])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def course_detail_kb(course_id: str, is_free: bool) -> InlineKeyboardMarkup:
    buttons = []
    if is_free:
        buttons.append([InlineKeyboardButton(text="▶️ Начать курс", callback_data=f"start_course:{course_id}")])
    else:
        buttons.append([InlineKeyboardButton(text="🔒 Скоро будет доступно", callback_data="soon")])
    buttons.append([InlineKeyboardButton(text="⬅️ К списку курсов", callback_data="courses")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 К курсам", callback_data="courses")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ])
