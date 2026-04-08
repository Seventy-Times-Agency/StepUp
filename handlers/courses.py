from aiogram import Router, F
from aiogram.types import CallbackQuery
from content.courses import COURSES_BY_ID
from keyboards.inline import courses_list_kb, course_detail_kb, back_to_menu_kb
from database.db import get_or_create_user, get_user_progress, start_course

router = Router()


@router.callback_query(F.data == "courses")
async def cb_courses(callback: CallbackQuery):
    await callback.message.edit_text(
        "📚 *Список курсов*\n\nВыбери курс, чтобы узнать подробнее:",
        reply_markup=courses_list_kb(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("course:"))
async def cb_course_detail(callback: CallbackQuery):
    course_id = callback.data.split(":")[1]
    course = COURSES_BY_ID.get(course_id)
    if not course:
        await callback.answer("Курс не найден", show_alert=True)
        return

    tag = "🆓 БЕСПЛАТНО" if course["is_free"] else "🔒 Скоро"
    text = f"{course['emoji']} *{course['title']}*\n{tag}\n\n{course['description']}"
    if course["lessons_count"] > 0:
        text += f"\n\n📖 Уроков: {course['lessons_count']}"

    await callback.message.edit_text(
        text,
        reply_markup=course_detail_kb(course_id, course["is_free"]),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("start_course:"))
async def cb_start_course(callback: CallbackQuery):
    course_id = callback.data.split(":")[1]
    course = COURSES_BY_ID.get(course_id)
    if not course:
        await callback.answer("Курс не найден", show_alert=True)
        return

    user_db_id = await get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username or "",
        full_name=callback.from_user.full_name or "",
    )
    await start_course(user_db_id, course_id)

    await callback.message.edit_text(
        f"🚀 *{course['title']}*\n\n"
        "Контент курса готовится\\. Совсем скоро здесь появятся уроки\\!\n\n"
        "_Следи за обновлениями\\._",
        reply_markup=back_to_menu_kb(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()


@router.callback_query(F.data == "soon")
async def cb_soon(callback: CallbackQuery):
    await callback.answer("Этот курс скоро будет доступен! 🔜", show_alert=True)


@router.callback_query(F.data == "progress")
async def cb_progress(callback: CallbackQuery):
    user_db_id = await get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username or "",
        full_name=callback.from_user.full_name or "",
    )
    progress = await get_user_progress(user_db_id)

    if not progress:
        text = (
            "📊 *Мой прогресс*\n\n"
            "Ты ещё не начал ни одного курса\\.\n\n"
            "Начни с бесплатного курса *«Первый шаг»*\\! 👇"
        )
        parse_mode = "MarkdownV2"
    else:
        lines = ["📊 *Мой прогресс*\n"]
        for course_id, data in progress.items():
            course = COURSES_BY_ID.get(course_id)
            if course:
                status = "✅ Завершён" if data["completed"] else f"📖 Урок {data['lesson_id'] + 1}"
                lines.append(f"{course['emoji']} {course['title']}: {status}")
        text = "\n".join(lines)
        parse_mode = "Markdown"

    await callback.message.edit_text(text, reply_markup=back_to_menu_kb(), parse_mode=parse_mode)
    await callback.answer()
