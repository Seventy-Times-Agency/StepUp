import asyncio
import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ai.tutor import generate_lesson_summary, get_tutor_reply
from content.courses import (
    get_next_lesson,
    is_last_lesson_of_module,
    total_lessons_in_course,
)
from database.db import (
    get_completed_lesson_keys,
    get_conversation,
    get_course_summaries,
    get_or_create_user,
    get_quiz_result,
    mark_course_completed,
    save_lesson_summary,
    save_message,
)
from keyboards.inline import after_lesson_kb, course_completed_kb
from keyboards.reply import main_menu_kb
from states.learning import LearningState

log = logging.getLogger(__name__)
router = Router()


async def _finalize_lesson(user_db_id: int, data: dict) -> None:
    """Сохраняет резюме урока в фоне (не блокирует ответ пользователю)."""
    course_id    = data["course_id"]
    module_id    = data["module_id"]
    lesson_id    = data["lesson_id"]
    lesson_title = data["lesson_title"]
    try:
        history = await get_conversation(user_db_id, course_id, module_id, lesson_id)
        if not history:
            return
        summary = await generate_lesson_summary(lesson_title, history)
        await save_lesson_summary(
            user_db_id, course_id, module_id, lesson_id, lesson_title, summary
        )
        # Если курс пройден — отметить
        completed = await get_completed_lesson_keys(user_db_id, course_id)
        if len(completed) >= total_lessons_in_course(course_id):
            await mark_course_completed(user_db_id, course_id)
    except Exception as e:
        log.warning("Не удалось сохранить резюме урока: %s", e)


async def _finish_lesson(message: Message, state: FSMContext) -> None:
    """Закрывает урок, показывает кнопки «следующий урок / тест» и запускает
    фоновое сохранение резюме."""
    data = await state.get_data()
    await state.clear()

    # Если был не в уроке — просто покажем меню
    if not data or "lesson_id" not in data:
        await message.answer("Главное меню 👇", reply_markup=main_menu_kb())
        return

    course_id = data["course_id"]
    module_id = data["module_id"]
    lesson_id = data["lesson_id"]

    user_db_id = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or "",
    )

    # Возвращаем основное меню (убираем reply-клавиатуру урока)
    await message.answer(
        "✅ Урок завершён. Ты молодец!",
        reply_markup=main_menu_kb(),
    )

    # Кнопки навигации
    next_lesson = get_next_lesson(course_id, module_id, lesson_id)
    quiz_done = await get_quiz_result(user_db_id, course_id, module_id)
    show_quiz = is_last_lesson_of_module(course_id, module_id, lesson_id) and not (
        quiz_done and quiz_done["passed"]
    )

    if not next_lesson and not show_quiz:
        await message.answer(
            "🎉 *Поздравляем!* Ты прошёл весь бесплатный курс «Первый шаг».\n\n"
            "Теперь ты можешь выбрать направление и двигаться глубже.",
            reply_markup=course_completed_kb(course_id),
            parse_mode="Markdown",
        )
    else:
        await message.answer(
            "Что дальше? 👇",
            reply_markup=after_lesson_kb(course_id, module_id, next_lesson, show_quiz),
        )

    # Резюме — в фоне, чтобы юзер не ждал OpenRouter
    asyncio.create_task(_finalize_lesson(user_db_id, data))


# --- /start и /menu работают даже во время урока ---

@router.message(LearningState.in_lesson, CommandStart())
async def lesson_start_command(message: Message, state: FSMContext):
    await _finish_lesson(message, state)


@router.message(LearningState.in_lesson, Command("menu"))
async def lesson_menu_command(message: Message, state: FSMContext):
    await _finish_lesson(message, state)


@router.message(LearningState.in_lesson, F.text == "🚪 Завершить урок")
async def exit_lesson(message: Message, state: FSMContext):
    await _finish_lesson(message, state)


@router.message(LearningState.in_lesson, F.text)
async def handle_lesson_message(message: Message, state: FSMContext):
    data = await state.get_data()
    # Защита от потери state-данных (напр. после рестарта)
    if not data or "lesson_id" not in data:
        await state.clear()
        await message.answer(
            "⚠️ Урок прервался. Вернись в меню и продолжи с того места где остановился.",
            reply_markup=main_menu_kb(),
        )
        return

    course_id     = data["course_id"]
    module_id     = data["module_id"]
    lesson_id     = data["lesson_id"]
    course_title  = data["course_title"]
    module_title  = data["module_title"]
    lesson_title  = data["lesson_title"]
    lesson_plan   = data.get("lesson_plan", "")
    lesson_terms  = data.get("lesson_terms", "")

    user_db_id = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or "",
    )

    await save_message(user_db_id, course_id, module_id, lesson_id, "user", message.text)

    history = await get_conversation(user_db_id, course_id, module_id, lesson_id)
    # последнее сообщение пользователя уже передаётся отдельно
    history = history[:-1]

    thinking = await message.answer("✍️ Репетитор печатает...")
    student_history = await get_course_summaries(user_db_id, course_id)

    try:
        reply = await get_tutor_reply(
            course_title=course_title,
            module_title=module_title,
            lesson_title=lesson_title,
            history=history,
            user_message=message.text,
            lesson_plan=lesson_plan,
            lesson_terms=lesson_terms,
            student_history=student_history or None,
        )
    except Exception as e:
        log.error("Tutor reply error: %s", e)
        await thinking.delete()
        await message.answer("⚠️ Ошибка связи с репетитором. Попробуй ещё раз.")
        return

    await thinking.delete()
    await save_message(user_db_id, course_id, module_id, lesson_id, "assistant", reply)
    await message.answer(reply)
