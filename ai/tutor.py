from openai import AsyncOpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_BASE_URL
from ai.prompts import get_lesson_system_prompt

client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)


async def get_tutor_reply(
    course_title: str,
    module_title: str,
    lesson_title: str,
    history: list[dict],
    user_message: str,
) -> str:
    system_prompt = get_lesson_system_prompt(course_title, module_title, lesson_title)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = await client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=messages,
        max_tokens=600,
        temperature=0.7,
    )

    return response.choices[0].message.content


async def start_lesson(
    course_title: str,
    module_title: str,
    lesson_title: str,
) -> str:
    """Первое сообщение репетитора при входе в урок."""
    system_prompt = get_lesson_system_prompt(course_title, module_title, lesson_title)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Начинаем урок!"},
    ]

    response = await client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=messages,
        max_tokens=600,
        temperature=0.7,
    )

    return response.choices[0].message.content
