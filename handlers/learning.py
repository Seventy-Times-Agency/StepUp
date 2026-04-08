from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from states.learning import LearningState
from ai.tutor import get_tutor_reply
from database.db import get_or_create_user, save_message, get_conversation
from keyboards.reply import main_menu_kb

router = Router()


@router.message(LearningState.in_lesson, F.text == "🚪 Завершить урок")
async def exit_lesson(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Урок завершён. Возвращаемся в главное меню 👇",
        reply_markup=main_menu_kb(),
    )


@router.message(LearningState.in_lesson, F.text)
async def handle_lesson_message(message: Message, state: FSMContext):
    data = await state.get_data()
    course_id  = data["course_id"]
    module_id  = data["module_id"]
    lesson_id  = data["lesson_id"]
    course_title  = data["course_title"]
    module_title  = data["module_title"]
    lesson_title  = data["lesson_title"]

    user_db_id = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or "",
    )

    await save_message(user_db_id, course_id, module_id, lesson_id, "user", message.text)

    history = await get_conversation(user_db_id, course_id, module_id, lesson_id)
    # убираем последнее сообщение пользователя из истории — оно уже передаётся отдельно
    history = history[:-1]

    thinking = await message.answer("✍️ Репетитор печатает...")

    try:
        reply = await get_tutor_reply(
            course_title=course_title,
            module_title=module_title,
            lesson_title=lesson_title,
            history=history,
            user_message=message.text,
        )
    except Exception as e:
        await thinking.delete()
        await message.answer("⚠️ Ошибка связи с репетитором. Попробуй ещё раз.")
        return

    await thinking.delete()
    await save_message(user_db_id, course_id, module_id, lesson_id, "assistant", reply)
    await message.answer(reply)
