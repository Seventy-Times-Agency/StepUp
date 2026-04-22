from aiogram.fsm.state import State, StatesGroup


class LearningState(StatesGroup):
    in_lesson = State()


class OnboardingState(StatesGroup):
    awaiting_experience = State()
    awaiting_goal = State()
    awaiting_context = State()
