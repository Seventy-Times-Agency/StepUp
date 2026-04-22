"""Короткая диагностика перед первым уроком: опыт, цель, контекст.
Профиль сохраняется и подмешивается в системный промпт каждого урока."""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.db import get_or_create_user, save_user_profile
from keyboards.inline import (
    onboarding_experience_kb,
    onboarding_goal_kb,
    onboarding_skip_context_kb,
)
from states.learning import OnboardingState

log = logging.getLogger(__name__)
router = Router()


INTRO_TEXT = (
    "👋 *Прежде чем начнём — расскажи о себе в 30 секунд.*\n\n"
    "Это нужно, чтобы я подбирал примеры под тебя и объяснял на твоём уровне, "
    "а не «в общем». Никуда кроме тебя эта информация не уходит.\n\n"
    "*Вопрос 1 из 3.* Какой у тебя опыт в digital/маркетинге?"
)

GOAL_PROMPT = "*Вопрос 2 из 3.* Зачем ты идёшь учиться? Выбери самое близкое:"

CONTEXT_PROMPT = (
    "*Вопрос 3 из 3.* Расскажи в 1-2 предложениях чем занимаешься сейчас "
    "и какая сфера тебе интересна — я буду опираться на это в примерах.\n\n"
    "_(Можешь пропустить — тогда примеры будут общие.)_"
)


async def start_onboarding(
    message: Message,
    state: FSMContext,
    course_id: str,
    module_id: str,
    lesson_id: str,
) -> None:
    """Точка входа. Сохраняет в FSM-данных урок, который надо запустить после
    завершения диагностики."""
    await state.set_state(OnboardingState.awaiting_experience)
    await state.update_data(
        pending_course=course_id,
        pending_module=module_id,
        pending_lesson=lesson_id,
    )
    await message.answer(
        INTRO_TEXT,
        reply_markup=onboarding_experience_kb(),
        parse_mode="Markdown",
    )


@router.callback_query(OnboardingState.awaiting_experience, F.data.startswith("ob_exp:"))
async def cb_exp(callback: CallbackQuery, state: FSMContext):
    code = callback.data.split(":", 1)[1]
    user_db_id = await get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username or "",
        full_name=callback.from_user.full_name or "",
    )
    await save_user_profile(user_db_id, experience=code)
    await state.set_state(OnboardingState.awaiting_goal)
    await callback.message.edit_text(
        GOAL_PROMPT,
        reply_markup=onboarding_goal_kb(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(OnboardingState.awaiting_goal, F.data.startswith("ob_goal:"))
async def cb_goal(callback: CallbackQuery, state: FSMContext):
    code = callback.data.split(":", 1)[1]
    user_db_id = await get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username or "",
        full_name=callback.from_user.full_name or "",
    )
    await save_user_profile(user_db_id, goal=code)
    await state.set_state(OnboardingState.awaiting_context)
    await callback.message.edit_text(
        CONTEXT_PROMPT,
        reply_markup=onboarding_skip_context_kb(),
        parse_mode="Markdown",
    )
    await callback.answer()


async def _finish_and_launch(message: Message, state: FSMContext, user_db_id: int):
    data = await state.get_data()
    course_id = data.get("pending_course")
    module_id = data.get("pending_module")
    lesson_id = data.get("pending_lesson")
    await state.clear()
    if course_id and module_id and lesson_id:
        # локальный импорт чтобы не ловить циклический
        from handlers.courses import launch_lesson
        await launch_lesson(message, state, user_db_id, course_id, module_id, lesson_id)


@router.callback_query(OnboardingState.awaiting_context, F.data == "ob_skip_ctx")
async def cb_skip_context(callback: CallbackQuery, state: FSMContext):
    user_db_id = await get_or_create_user(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username or "",
        full_name=callback.from_user.full_name or "",
    )
    await callback.message.edit_text("Готово! Запускаю урок 🚀")
    await callback.answer()
    await _finish_and_launch(callback.message, state, user_db_id)


@router.message(OnboardingState.awaiting_context, F.text)
async def msg_context(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    user_db_id = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or "",
    )
    if text and len(text) >= 3:
        await save_user_profile(user_db_id, context=text[:500])
        await message.answer("Спасибо! Буду использовать это в примерах 🙌")
    else:
        await message.answer("Ок, пропустим — примеры будут общие.")
    await _finish_and_launch(message, state, user_db_id)
