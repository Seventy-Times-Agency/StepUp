"""Помощник для нормализации профиля студента в читаемый для промпта текст."""

EXPERIENCE_LABEL = {
    "new":      "Новичок — не имел опыта в digital/маркетинге",
    "beginner": "Начальный уровень — что-то читал, пробовал самостоятельно",
    "related":  "Работает в смежной сфере, имеет бизнес-контекст",
    "pro":      "Уже работает в digital / маркетинге",
}

GOAL_LABEL = {
    "freelance": "Подработка / выход на фриланс",
    "career":    "Смена профессии, хочет войти в digital",
    "business":  "Развивает свой бизнес или проект",
    "curious":   "Общее развитие, без конкретной цели заработка",
}


def format_profile(profile: dict | None) -> str:
    if not profile:
        return ""
    parts = []
    exp = profile.get("experience")
    goal = profile.get("goal")
    ctx = (profile.get("context") or "").strip()
    if exp:
        parts.append(f"• Опыт: {EXPERIENCE_LABEL.get(exp, exp)}")
    if goal:
        parts.append(f"• Цель: {GOAL_LABEL.get(goal, goal)}")
    if ctx:
        parts.append(f"• О себе: {ctx}")
    return "\n".join(parts)
