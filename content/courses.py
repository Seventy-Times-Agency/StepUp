CATEGORIES = [
    {"id": "promo",    "title": "Продвижение и контент", "emoji": "📣", "btn": "📣 Продвижение"},
    {"id": "business", "title": "Бизнес и продажи",      "emoji": "💼", "btn": "💼 Бизнес"},
    {"id": "tech",     "title": "Технологии",             "emoji": "🤖", "btn": "🤖 Технологии"},
]

CATEGORIES_BY_ID  = {c["id"]: c for c in CATEGORIES}
CATEGORIES_BY_BTN = {c["btn"]: c for c in CATEGORIES}

INTRO_MODULES = [
    {
        "id": "m1",
        "title": "Как устроен онлайн-рынок",
        "emoji": "🌐",
        "lessons": [
            {
                "id": "m1l1",
                "title": "Что такое digital и почему сейчас самое время",
                "description": "Разберёмся как устроен рынок интернет-маркетинга, почему он растёт и чем отличается от офлайна.",
                "outcome": "Поймёшь как работает digital-рынок и почему сейчас лучший момент войти в сферу",
            },
            {
                "id": "m1l2",
                "title": "Кто платит деньги и за что",
                "description": "Кто такие заказчики, что они покупают у специалистов и как формируется цена на услуги.",
                "outcome": "Узнаешь как бизнес нанимает специалистов и за что платит реальные деньги",
            },
            {
                "id": "m1l3",
                "title": "Какие профессии есть и сколько зарабатывают",
                "description": "Обзор всех востребованных профессий в digital: от SMM до вайб-кодинга. Реальные цифры по доходам.",
                "outcome": "Получишь полную карту профессий и поймёшь какой доход реален на старте и через год",
            },
        ],
        "has_quiz": True,
    },
    {
        "id": "m2",
        "title": "Трафик и контент",
        "emoji": "📣",
        "lessons": [
            {
                "id": "m2l1",
                "title": "SMM — как бренды живут в соцсетях",
                "description": "Что такое SMM на самом деле, как строится работа с соцсетями и что входит в задачи специалиста.",
                "outcome": "Поймёшь суть профессии SMM-специалиста и сможешь оценить — твоё это или нет",
            },
            {
                "id": "m2l2",
                "title": "Реклама и таргет — как бизнес находит клиентов",
                "description": "Как работает таргетированная реклама, какие платформы используются и как считается эффективность.",
                "outcome": "Разберёшься в логике платного трафика и поймёшь как таргетолог влияет на продажи",
            },
            {
                "id": "m2l3",
                "title": "Контент и копирайтинг — слова, которые продают",
                "description": "Чем контент-маркетинг отличается от копирайтинга, что такое продающий текст и как им пользуются бизнесы.",
                "outcome": "Узнаешь как работают слова в маркетинге и сможешь написать первый продающий пост",
            },
        ],
        "has_quiz": True,
    },
    {
        "id": "m3",
        "title": "Продажи и технологии",
        "emoji": "⚙️",
        "lessons": [
            {
                "id": "m3l1",
                "title": "Воронки и CRM — как продавать системно",
                "description": "Что такое воронка продаж, зачем нужна CRM и как автоматизация помогает бизнесу продавать больше.",
                "outcome": "Поймёшь как устроены продажи в онлайн-бизнесе и что такое автоматизация на практике",
            },
            {
                "id": "m3l2",
                "title": "No-code и AI — делать в 10 раз больше",
                "description": "Make, n8n, ChatGPT, Claude — как современные инструменты позволяют работать без программирования.",
                "outcome": "Узнаешь какие no-code и AI инструменты сейчас в тренде и как они меняют профессии",
            },
            {
                "id": "m3l3",
                "title": "Личный бренд и фриланс — продавать себя",
                "description": "Как упаковать себя как специалиста, найти первых клиентов и выстроить стабильный доход.",
                "outcome": "Получишь план первых шагов для выхода на фриланс или продажи своих услуг",
            },
        ],
        "has_quiz": True,
    },
]

INTRO_MODULES_BY_ID = {m["id"]: m for m in INTRO_MODULES}

COURSES = [
    {
        "id": "intro",
        "title": "Первый шаг",
        "emoji": "🆓",
        "is_free": True,
        "category": None,
        "description": (
            "Вводный курс в мир онлайн-маркетинга и заработка в интернете.\n\n"
            "3 модуля · 9 уроков · тесты после каждого модуля\n\n"
            "Пройди и узнай какое направление тебе подходит."
        ),
        "modules": INTRO_MODULES,
    },
    {"id": "smm",       "title": "SMM-специалист",          "emoji": "📱", "is_free": False, "category": "promo",     "description": "Ведение соцсетей, контент-стратегия, работа с аудиторией и аналитика.", "modules": []},
    {"id": "target",    "title": "Таргетолог",               "emoji": "🎯", "is_free": False, "category": "promo",     "description": "Настройка рекламы в VK, Telegram Ads, Meta. Аналитика и оптимизация.", "modules": []},
    {"id": "content",   "title": "Контент-маркетинг",        "emoji": "✍️", "is_free": False, "category": "promo",     "description": "Контент-стратегия, редполитика, дистрибуция и продвижение.", "modules": []},
    {"id": "copy",      "title": "Копирайтинг",              "emoji": "📝", "is_free": False, "category": "promo",     "description": "Продающие тексты, посты, лендинги. Пишем так, чтобы покупали.", "modules": []},
    {"id": "email",     "title": "Email-маркетинг",          "emoji": "📧", "is_free": False, "category": "promo",     "description": "Рассылки, автоворонки, сегментация базы и аналитика.", "modules": []},
    {"id": "influence", "title": "Influence-маркетинг",      "emoji": "🌟", "is_free": False, "category": "promo",     "description": "Работа с блогерами, посевы, коллаборации и оценка эффективности.", "modules": []},
    {"id": "sales",     "title": "Автоматизация продаж",     "emoji": "⚙️", "is_free": False, "category": "business",  "description": "CRM, чат-боты, воронки продаж. Продавай системно и автоматически.", "modules": []},
    {"id": "ecom",      "title": "Маркетплейсы (e-com)",     "emoji": "🛒", "is_free": False, "category": "business",  "description": "Продажи на Ozon и Wildberries: карточки, реклама, масштабирование.", "modules": []},
    {"id": "freelance", "title": "Фриланс и продажа услуг",  "emoji": "💼", "is_free": False, "category": "business",  "description": "Упакуй себя как специалиста, найди клиентов и выстрой доход.", "modules": []},
    {"id": "brand",     "title": "Личный бренд",             "emoji": "⭐", "is_free": False, "category": "business",  "description": "Позиционирование, экспертность и монетизация личного бренда.", "modules": []},
    {"id": "nocode",    "title": "No-code автоматизация",    "emoji": "🔧", "is_free": False, "category": "tech",      "description": "Make, n8n, Zapier — автоматизируй процессы без кода.", "modules": []},
    {"id": "vibe",      "title": "Вайб-кодинг",              "emoji": "🤖", "is_free": False, "category": "tech",      "description": "Создавай продукты с ИИ: Cursor, Claude, v0. Без опыта в разработке.", "modules": []},
]

COURSES_BY_ID = {c["id"]: c for c in COURSES}


def get_courses_by_category(category_id: str) -> list:
    return [c for c in COURSES if c["category"] == category_id]
