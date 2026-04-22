from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from database.db import get_or_create_user
from keyboards.reply import main_menu_kb

router = Router()

WELCOME_TEXT = (
    "Привет! 👋 Добро пожаловать в *StepUp*!\n\n"
    "Мы делаем обучение маркетингу, SMM, таргету и "
    "автоматизации простым и понятным. 🚀\n\n"
    "Выбери категорию внизу 👇"
)

MENU_TEXT = "Главное меню 👇"


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or "",
    )
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_kb(), parse_mode="Markdown")


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(MENU_TEXT, reply_markup=main_menu_kb())
