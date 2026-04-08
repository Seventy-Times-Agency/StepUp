from aiogram.fsm.state import State, StatesGroup


class LearningState(StatesGroup):
    in_lesson = State()
