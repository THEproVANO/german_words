"""Тексты интерфейса на всех языках бота. t(lang, key, **kwargs) возвращает нужный текст."""

UI_LANGUAGES = {"ru": "🇷🇺 Русский", "en": "🇬🇧 English", "es": "🇪🇸 Español"}
DEFAULT_UI = "ru"

# Первый экран: язык пользователя ещё неизвестен, поэтому вопрос сразу на всех языках
CHOOSE_UI = "🌐 Выбери язык бота\nChoose the bot language\nElige el idioma del bot"

TEXTS = {
    # --- старт ---
    "welcome": {
        "ru": "Привет! 👋 Я помогу выучить иностранные слова.\n\nКакой язык будем изучать?",
        "en": "Hi! 👋 I'll help you learn foreign words.\n\nWhich language do you want to learn?",
        "es": "¡Hola! 👋 Te ayudaré a aprender palabras extranjeras.\n\n¿Qué idioma quieres aprender?",
    },
    "ui_set": {
        "ru": "Язык бота: {name} ✅",
        "en": "Bot language: {name} ✅",
        "es": "Idioma del bot: {name} ✅",
    },
    "learn_de": {"ru": "🇩🇪 Немецкий", "en": "🇩🇪 German", "es": "🇩🇪 Alemán"},
    "learn_en": {"ru": "🇬🇧 Английский", "en": "🇬🇧 English", "es": "🇬🇧 Inglés"},
    "learn_es": {"ru": "🇪🇸 Испанский", "en": "🇪🇸 Spanish", "es": "🇪🇸 Español"},
    "ask_learn": {
        "ru": "Какой язык будем изучать?",
        "en": "Which language do you want to learn?",
        "es": "¿Qué idioma quieres aprender?",
    },
    "btn_learn": {"ru": "🌍 Изучаемый язык", "en": "🌍 Language to learn",
                  "es": "🌍 Idioma que aprendes"},
    "answer_rules_de": {
        "ru": "по-немецки: существительные без артикля, глаголы в инфинитиве. Регистр не важен, "
              "вместо ä, ö, ü, ß можно писать ae, oe, ue, ss.",
        "en": "in German: nouns without the article, verbs in the infinitive. Case doesn't matter, "
              "and you can type ae, oe, ue, ss instead of ä, ö, ü, ß.",
        "es": "en alemán: los sustantivos sin artículo, los verbos en infinitivo. Las mayúsculas "
              "no importan, y puedes escribir ae, oe, ue, ss en lugar de ä, ö, ü, ß.",
    },
    "answer_rules_en": {
        "ru": "по-английски: существительные без артикля (a, the), глаголы в начальной форме, «to» "
              "писать не обязательно. Регистр и апостроф не важны (dont = don't).",
        "en": "in English: nouns without the article (a, the), verbs in the base form, “to” is "
              "optional. Case and apostrophes don't matter (dont = don't).",
        "es": "en inglés: los sustantivos sin artículo (a, the), los verbos en forma base, «to» es "
              "opcional. Las mayúsculas y el apóstrofo no importan (dont = don't).",
    },
    "answer_rules_es": {
        "ru": "по-испански: существительные без артикля, глаголы в инфинитиве. Регистр и ударения "
              "не важны: можно писать a, e, i, o, u, n вместо á, é, í, ó, ú, ñ.",
        "en": "in Spanish: nouns without the article, verbs in the infinitive. Case and accents "
              "don't matter: you can type a, e, i, o, u, n instead of á, é, í, ó, ú, ñ.",
        "es": "en español: los sustantivos sin artículo, los verbos en infinitivo. Las mayúsculas "
              "y las tildes no importan: puedes escribir a, e, i, o, u, n en lugar de á, é, í, ó, ú, ñ.",
    },
    "card_rules_es": {
        "ru": "🗂 <b>Карточка слова</b>: часть речи и уровень; у существительных — артикль el или "
              "la (множественное число образуется по правилу -s / -es, отмечены только слова без "
              "него или только во мн. ч.); у глаголов — форма yo в настоящем времени (если она "
              "неправильная), претерит и причастие (tener (yo tengo) — tuve — tenido); 1–3 перевода "
              "и пример с переводом.",
        "en": "🗂 <b>Word card</b>: part of speech and level; for nouns, the article el or la "
              "(plurals follow the -s / -es rule, so only nouns without a plural or plural-only "
              "ones are marked); for verbs, the irregular “yo” present form (if any), the preterite "
              "and the participle (tener (yo tengo) — tuve — tenido); 1–3 translations and an "
              "example with its translation.",
        "es": "🗂 <b>Ficha de la palabra</b>: categoría y nivel; en los sustantivos, el artículo el "
              "o la (el plural sigue la regla -s / -es; solo se marcan los que no tienen plural o "
              "solo se usan en plural); en los verbos, la forma «yo» del presente si es irregular, "
              "el pretérito indefinido y el participio (tener (yo tengo) — tuve — tenido); "
              "1–3 traducciones y un ejemplo traducido.",
    },
    "card_rules_de": {
        "ru": "🗂 <b>Карточка слова</b>: часть речи и уровень; у существительных — артикль и "
              "множественное число; у глаголов — форма 3-го лица (если корень меняется), "
              "Präteritum и Perfekt (fahren (er fährt) — fuhr — ist gefahren); 1–3 перевода и пример "
              "с переводом.",
        "en": "🗂 <b>Word card</b>: part of speech and level; for nouns, the article and plural; "
              "for verbs, the 3rd person form (if the stem changes), Präteritum and Perfekt "
              "(fahren (er fährt) — fuhr — ist gefahren); 1–3 translations and an example with "
              "its translation.",
        "es": "🗂 <b>Ficha de la palabra</b>: categoría y nivel; en los sustantivos, el artículo y "
              "el plural; en los verbos, la 3.ª persona (si cambia la raíz), el Präteritum y el "
              "Perfekt (fahren (er fährt) — fuhr — ist gefahren); 1–3 traducciones y un ejemplo "
              "traducido.",
    },
    "card_rules_en": {
        "ru": "🗂 <b>Карточка слова</b>: часть речи и уровень; у существительных — множественное "
              "число; у глаголов — три формы: начальная, Past Simple и Past Participle "
              "(go — went — gone); 1–3 перевода и пример с переводом.",
        "en": "🗂 <b>Word card</b>: part of speech and level; for nouns, the plural; for verbs, "
              "three forms: base form, Past Simple and Past Participle (go — went — gone); "
              "1–3 translations and an example with its translation.",
        "es": "🗂 <b>Ficha de la palabra</b>: categoría y nivel; en los sustantivos, el plural; en "
              "los verbos, tres formas: base, Past Simple y Past Participle (go — went — gone); "
              "1–3 traducciones y un ejemplo traducido.",
    },
    "lang_chosen": {
        "ru": "Язык: {language}\n\nВыбери свой уровень:",
        "en": "Language: {language}\n\nChoose your level:",
        "es": "Idioma: {language}\n\nElige tu nivel:",
    },
    "choose_lang_first": {
        "ru": "Сначала выбери язык: /start",
        "en": "Choose a language first: /start",
        "es": "Primero elige un idioma: /start",
    },
    "level_set": {
        "ru": "Уровень: <b>{level}</b> ✅",
        "en": "Level: <b>{level}</b> ✅",
        "es": "Nivel: <b>{level}</b> ✅",
    },
    "first_word": {
        "ru": "Вот твоё первое слово:",
        "en": "Here is your first word:",
        "es": "Aquí tienes tu primera palabra:",
    },
    "welcome_back": {
        "ru": "С возвращением! 👋",
        "en": "Welcome back! 👋",
        "es": "¡Bienvenido de nuevo! 👋",
    },
    "setup_first": {
        "ru": "Сначала настрой бота: /start",
        "en": "Set up the bot first: /start",
        "es": "Primero configura el bot: /start",
    },

    # --- главное меню и слова ---
    "btn_more": {"ru": "➕ Ещё слово", "en": "➕ One more word",
                 "es": "➕ Otra palabra"},
    "btn_profile": {"ru": "👤 Профиль", "en": "👤 Profile", "es": "👤 Perfil"},
    "quiz_first": {
        "ru": "Сначала пройди тест 📝",
        "en": "Finish the quiz first 📝",
        "es": "Primero termina el test 📝",
    },
    "all_learned": {
        "ru": "Все слова этого уровня уже изучены 🎉 Выбери другой уровень в профиле.",
        "en": "You've learned all the words of this level 🎉 Choose another level in your profile.",
        "es": "Ya has aprendido todas las palabras de este nivel 🎉 "
              "Elige otro nivel en tu perfil.",
    },
    "last_word": {
        "ru": "🎉 Это было последнее слово уровня {level}! "
              "Выбери другой уровень в профиле, чтобы продолжить.",
        "en": "🎉 That was the last word of level {level}! "
              "Choose another level in your profile to continue.",
        "es": "🎉 ¡Esa era la última palabra del nivel {level}! "
              "Elige otro nivel en tu perfil para continuar.",
    },
    "no_quiz": {
        "ru": "Сейчас нет активного теста. Используй кнопки меню 👇",
        "en": "There's no active quiz right now. Use the menu buttons 👇",
        "es": "No hay ningún test activo. Usa los botones del menú 👇",
    },
    "no_plural": {"ru": "нет мн. ч.", "en": "no plural", "es": "sin plural"},
    "plural_only": {"ru": "только мн. ч.", "en": "plural only",
                    "es": "solo plural"},

    # --- профиль ---
    "profile": {
        "ru": "👤 <b>Профиль</b>\n\nЯзык: {language}\nУровень: <b>{level}</b>\n"
              "Изучено слов: <b>{learned}</b> из {total}\nРассылка: {schedule}\n"
              "Часовой пояс: {tz}\nЯзык бота: {ui}\nСтатус: {status}",
        "en": "👤 <b>Profile</b>\n\nLanguage: {language}\nLevel: <b>{level}</b>\n"
              "Words learned: <b>{learned}</b> of {total}\nSchedule: {schedule}\n"
              "Time zone: {tz}\nBot language: {ui}\nStatus: {status}",
        "es": "👤 <b>Perfil</b>\n\nIdioma: {language}\nNivel: <b>{level}</b>\n"
              "Palabras aprendidas: <b>{learned}</b> de {total}\nEnvío: {schedule}\n"
              "Zona horaria: {tz}\nIdioma del bot: {ui}\nEstado: {status}",
    },
    "status_paused": {"ru": "⏸ на паузе", "en": "⏸ paused", "es": "⏸ en pausa"},
    "status_quiz": {
        "ru": "📝 ждёт прохождения теста",
        "en": "📝 waiting for the quiz",
        "es": "📝 test pendiente",
    },
    "status_active": {"ru": "✅ активен", "en": "✅ active", "es": "✅ activo"},
    "schedule": {
        "ru": "{interval} с {start}:00 до {end}:00, не больше {limit} в день",
        "en": "{interval} from {start}:00 to {end}:00, up to {limit} a day",
        "es": "{interval} de {start}:00 a {end}:00, máximo {limit} al día",
    },
    "every_30": {"ru": "каждые 30 минут", "en": "every 30 minutes",
                 "es": "cada 30 minutos"},
    "every_60": {"ru": "каждый час", "en": "every hour",
                 "es": "cada hora"},
    "every_120": {"ru": "каждые 2 часа", "en": "every 2 hours",
                  "es": "cada 2 horas"},
    "btn_interval": {"ru": "⏱ Интервал", "en": "⏱ Interval",
                     "es": "⏱ Intervalo"},
    "btn_limit": {"ru": "🔢 Слов в день", "en": "🔢 Words per day",
                  "es": "🔢 Palabras al día"},
    "btn_hours": {"ru": "🕘 Время рассылки", "en": "🕘 Delivery hours",
                  "es": "🕘 Horario de envío"},
    "btn_tz": {"ru": "🕒 Часовой пояс", "en": "🕒 Time zone",
               "es": "🕒 Zona horaria"},
    "btn_level": {"ru": "📚 Сменить уровень", "en": "📚 Change level",
                  "es": "📚 Cambiar nivel"},
    "btn_ui": {"ru": "🌐 Язык бота", "en": "🌐 Bot language",
               "es": "🌐 Idioma del bot"},
    "btn_help": {"ru": "ℹ️ Как работает бот", "en": "ℹ️ How the bot works",
                 "es": "ℹ️ Cómo funciona el bot"},
    "btn_pause": {"ru": "⏸ Пауза", "en": "⏸ Pause", "es": "⏸ Pausa"},
    "btn_resume": {"ru": "▶️ Продолжить", "en": "▶️ Resume",
                   "es": "▶️ Reanudar"},
    "level_BIZ": {"ru": "💼 Работа, бизнес и IT", "en": "💼 Work, business & IT",
                  "es": "💼 Trabajo, negocios e IT"},
    "btn_restart": {"ru": "🔄 Перезапуск (для обновления версии бота)",
                    "en": "🔄 Restart (to update the bot version)",
                    "es": "🔄 Reiniciar (para actualizar el bot)"},
    "restarted": {
        "ru": "🔄 Бот перезапущен: меню и кнопки обновлены. Прогресс и настройки сохранены.",
        "en": "🔄 Bot restarted: the menu and buttons are updated. Your progress and settings are kept.",
        "es": "🔄 Bot reiniciado: el menú y los botones están actualizados. Tu progreso y tus ajustes "
              "se mantienen.",
    },
    "pause_on": {"ru": "Пауза включена", "en": "Paused",
                 "es": "Pausa activada"},
    "pause_off": {"ru": "Продолжаем!", "en": "Let's continue!",
                  "es": "¡Seguimos!"},
    "ask_level": {"ru": "Выбери уровень:", "en": "Choose your level:",
                  "es": "Elige tu nivel:"},
    "ask_tz": {"ru": "Выбери часовой пояс:", "en": "Choose your time zone:",
               "es": "Elige tu zona horaria:"},
    "tz_set": {"ru": "Часовой пояс: {tz} ✅", "en": "Time zone: {tz} ✅",
               "es": "Zona horaria: {tz} ✅"},
    "ask_interval": {
        "ru": "Как часто присылать слова?",
        "en": "How often should I send words?",
        "es": "¿Cada cuánto envío las palabras?",
    },
    "ask_limit": {
        "ru": "Сколько слов присылать в день?",
        "en": "How many words per day?",
        "es": "¿Cuántas palabras al día?",
    },
    "ask_start": {
        "ru": "С какого часа присылать слова?",
        "en": "From what time should I send words?",
        "es": "¿Desde qué hora envío las palabras?",
    },
    "ask_end": {
        "ru": "Начало: {start}:00\n\nДо какого часа присылать слова?",
        "en": "Start: {start}:00\n\nUntil what time should I send words?",
        "es": "Inicio: {start}:00\n\n¿Hasta qué hora envío las palabras?",
    },
    "schedule_set": {
        "ru": "✅ Рассылка: {schedule}",
        "en": "✅ Schedule: {schedule}",
        "es": "✅ Envío: {schedule}",
    },

    # --- тесты ---
    "quiz_daily": {
        "ru": "📝 <b>Тест дня</b>: {n} слов из изученных сегодня.",
        "en": "📝 <b>Daily quiz</b>: {n} words from today.",
        "es": "📝 <b>Test del día</b>: {n} palabras de hoy.",
    },
    "quiz_weekly": {
        "ru": "🏆 <b>Недельный тест</b>: {n} слов из изученных за неделю.",
        "en": "🏆 <b>Weekly quiz</b>: {n} words from this week.",
        "es": "🏆 <b>Test semanal</b>: {n} palabras de esta semana.",
    },
    "quiz_rules": {
        "ru": "Напиши слово {answer_rules}\nПока тест не пройден, новые слова не приходят.",
        "en": "Type the word {answer_rules}\nNo new words until you pass the quiz.",
        "es": "Escribe la palabra {answer_rules}\nNo llegarán palabras nuevas hasta que termines el test.",
    },
    "question": {
        "ru": "Вопрос {n}/{total}\n{flag} <b>{tr}</b> ({pos})\nНачинается на: <code>{hint}</code>",
        "en": "Question {n}/{total}\n{flag} <b>{tr}</b> ({pos})\nStarts with: <code>{hint}</code>",
        "es": "Pregunta {n}/{total}\n{flag} <b>{tr}</b> ({pos})\nEmpieza por: <code>{hint}</code>",
    },
    "correct": {"ru": "✅ Верно! <b>{word}</b>", "en": "✅ Correct! <b>{word}</b>",
                "es": "✅ ¡Correcto! <b>{word}</b>"},
    "wrong1": {
        "ru": "❌ Неверно, попробуй ещё раз.",
        "en": "❌ Wrong, try again.",
        "es": "❌ Incorrecto, inténtalo de nuevo.",
    },
    "wrong2": {
        "ru": "❌ Неверно. Подсказка: <code>{hint}</code>",
        "en": "❌ Wrong. Hint: <code>{hint}</code>",
        "es": "❌ Incorrecto. Pista: <code>{hint}</code>",
    },
    "synonym": {
        "ru": "🤏 «{answer}» — тоже подходит по смыслу, но я загадал другое слово. Подсказка: <code>{hint}</code>",
        "en": "🤏 “{answer}” means the same, but I'm thinking of another word. Hint: <code>{hint}</code>",
        "es": "🤏 «{answer}» significa lo mismo, pero estoy pensando en otra palabra. Pista: <code>{hint}</code>",
    },
    "wrong3": {
        "ru": "❌ Неверно. Попробуй ещё раз или посмотри ответ.",
        "en": "❌ Wrong. Try again or look at the answer.",
        "es": "❌ Incorrecto. Inténtalo de nuevo o mira la respuesta.",
    },
    "btn_reveal": {"ru": "👀 Показать ответ", "en": "👀 Show answer",
                   "es": "👀 Ver la respuesta"},
    "revealed": {
        "ru": "Правильный ответ:\n\n{card}\n\nЭто слово спросим ещё раз в конце теста.",
        "en": "Correct answer:\n\n{card}\n\nThis word will be asked again at the end of the quiz.",
        "es": "Respuesta correcta:\n\n{card}\n\nEsta palabra se volverá a preguntar al final del test.",
    },
    "daily_done": {
        "ru": "🎉 Тест дня пройден! Молодец.",
        "en": "🎉 Daily quiz passed! Well done.",
        "es": "🎉 ¡Test del día superado! ¡Bien hecho!",
    },
    "weekly_done": {
        "ru": "🏆 Недельный тест пройден! Отличная работа.",
        "en": "🏆 Weekly quiz passed! Great job.",
        "es": "🏆 ¡Test semanal superado! ¡Excelente trabajo!",
    },
    "resume": {
        "ru": "Новые слова снова будут приходить по расписанию.",
        "en": "New words will arrive on schedule again.",
        "es": "Las palabras nuevas volverán a llegar según el horario.",
    },

    # --- объём уровня ---
    "ask_scope": {
        "ru": "Уровень: <b>{level}</b> ✅\n\nКакие слова присылать?",
        "en": "Level: <b>{level}</b> ✅\n\nWhich words should I send?",
        "es": "Nivel: <b>{level}</b> ✅\n\n¿Qué palabras envío?",
    },
    "btn_scope_all": {
        "ru": "📚 {level} и все уровни ниже",
        "en": "📚 {level} and all lower levels",
        "es": "📚 {level} y todos los niveles inferiores",
    },
    "btn_scope_only": {
        "ru": "🎯 Только {level}",
        "en": "🎯 Only {level}",
        "es": "🎯 Solo {level}",
    },
    "scope_all": {"ru": "{level} и ниже", "en": "{level} and below",
                  "es": "{level} e inferiores"},
    "scope_only": {"ru": "только {level}", "en": "only {level}",
                   "es": "solo {level}"},

    # --- сводки после тестов ---
    "quiz_stats": {
        "ru": "Результат теста:\n✅ с первой попытки: {first}\n✏️ с ошибками: {mistakes}\n"
              "👀 ответ подсмотрен: {revealed}",
        "en": "Quiz result:\n✅ first try: {first}\n✏️ after mistakes: {mistakes}\n"
              "👀 answer shown: {revealed}",
        "es": "Resultado del test:\n✅ a la primera: {first}\n✏️ tras errores: {mistakes}\n"
              "👀 respuesta mostrada: {revealed}",
    },
    "summary_daily": {
        "ru": "📊 <b>Итоги дня</b>\nСегодня изучено слов: <b>{today}</b>\n"
              "Всего изучено: <b>{learned}</b> из {total} ({percent}%)\n\n{stats}",
        "en": "📊 <b>Today's summary</b>\nWords learned today: <b>{today}</b>\n"
              "Total learned: <b>{learned}</b> of {total} ({percent}%)\n\n{stats}",
        "es": "📊 <b>Resumen del día</b>\nPalabras aprendidas hoy: <b>{today}</b>\n"
              "Total aprendidas: <b>{learned}</b> de {total} ({percent}%)\n\n{stats}",
    },
    "day_words": {
        "ru": "📚 <b>Слова за сегодня</b>\n\n{words}",
        "en": "📚 <b>Today's words</b>\n\n{words}",
        "es": "📚 <b>Palabras de hoy</b>\n\n{words}",
    },
    "summary_weekly": {
        "ru": "📈 <b>Итоги недели</b>\nИзучено за неделю: <b>{week}</b> (в среднем {avg} в день)\n"
              "Всего изучено: <b>{learned}</b> из {total} ({percent}%)\n\n"
              "⚙️ Сейчас: {schedule}.\nЭто до <b>{per_day}</b> слов в день и до <b>{per_week}</b> "
              "в неделю.\n{forecast}\n\n{stats}",
        "en": "📈 <b>Weekly summary</b>\nLearned this week: <b>{week}</b> ({avg} a day on average)\n"
              "Total learned: <b>{learned}</b> of {total} ({percent}%)\n\n"
              "⚙️ Current settings: {schedule}.\nThat's up to <b>{per_day}</b> words a day and up to "
              "<b>{per_week}</b> a week.\n{forecast}\n\n{stats}",
        "es": "📈 <b>Resumen de la semana</b>\nAprendidas esta semana: <b>{week}</b> "
              "({avg} al día de media)\nTotal aprendidas: <b>{learned}</b> de {total} ({percent}%)\n\n"
              "⚙️ Ajustes actuales: {schedule}.\nEso son hasta <b>{per_day}</b> palabras al día y hasta "
              "<b>{per_week}</b> a la semana.\n{forecast}\n\n{stats}",
    },
    "forecast": {
        "ru": "🏁 При таком темпе уровень {level} будет пройден примерно через {days} дн. — к {date}.",
        "en": "🏁 At this pace you'll finish level {level} in about {days} days — by {date}.",
        "es": "🏁 A este ritmo terminarás el nivel {level} en unos {days} días, hacia el {date}.",
    },
    "forecast_done": {
        "ru": "🎉 Все слова уровня {level} уже изучены!",
        "en": "🎉 You've already learned all the words of level {level}!",
        "es": "🎉 ¡Ya has aprendido todas las palabras del nivel {level}!",
    },

    # --- служебные команды ---
    "test_no_words": {
        "ru": "Пока нет слов для теста — сначала получи несколько слов.",
        "en": "No words for a quiz yet — get a few words first.",
        "es": "Aún no hay palabras para un test: primero recibe algunas palabras.",
    },
    "your_id": {
        "ru": "Твой Telegram ID: <code>{id}</code>",
        "en": "Your Telegram ID: <code>{id}</code>",
        "es": "Tu ID de Telegram: <code>{id}</code>",
    },

    # --- описание работы бота ---
    "tr_note": {
        "ru": "",
        "en": "\n\n🇷🇺 For now, word translations are in Russian only.",
        "es": "\n\n🇷🇺 De momento, las traducciones de las palabras de este idioma solo están en ruso.",
    },
    "rules": {
        "ru": "ℹ️ <b>Как работает бот</b>\n\n"
              "📩 <b>Новые слова</b> приходят по одному: {schedule}. Слова выбираются случайно "
              "из твоего уровня (и уровней ниже, если ты так выбрал) и не повторяются. Каждое полученное слово "
              "считается изученным.\n\n"
              "{card_rules}\n\n"
              "➕ <b>«Ещё слово»</b> присылает новое слово вне очереди, в дневной лимит оно "
              "не входит.\n\n"
              "📝 <b>Тест дня</b> в {quiz_hour}:00: до {daily} случайных слов из полученных "
              "за день. Бот пишет перевод, а ты вводишь слово {answer_rules} Синоним с тем же переводом ошибкой не считается — бот подскажет, какое слово загадано. После второй ошибки бот покажет подсказку, после третьей можно "
              "посмотреть ответ, но тогда слово спросят ещё раз в конце теста.\n\n"
              "🏆 <b>Недельный тест</b> по воскресеньям сразу после теста дня: до {weekly} "
              "слов за неделю.\n\n"
              "⛔ Пока тест не пройден, новые слова не приходят. Расписание продолжится сразу "
              "после прохождения теста.\n\n"
              "⚙️ В профиле можно изменить интервал, количество слов в день, время рассылки, "
              "часовой пояс, уровень, изучаемый язык и язык бота, а также поставить бота на паузу.{tr_note}",
        "en": "ℹ️ <b>How the bot works</b>\n\n"
              "📩 <b>New words</b> arrive one at a time: {schedule}. Words are picked at random "
              "from your level (and the levels below, if you chose so), and they never repeat. Every word you "
              "receive counts as learned.\n\n"
              "{card_rules}\n\n"
              "➕ <b>“One more word”</b> sends an extra word right away; it doesn't count toward "
              "the daily limit.\n\n"
              "📝 <b>Daily quiz</b> at {quiz_hour}:00: up to {daily} random words from the ones "
              "you got that day. The bot shows the translation and you type the word {answer_rules} A synonym with the same translation isn't counted as a mistake — the bot will hint which word it means. "
              "After the second mistake you get "
              "a hint; after the third you can see the answer, but then the word will be asked "
              "again at the end of the quiz.\n\n"
              "🏆 <b>Weekly quiz</b> on Sundays right after the daily quiz: up to {weekly} words "
              "from the week.\n\n"
              "⛔ No new words arrive until you pass the quiz. The schedule resumes right after "
              "you pass it.\n\n"
              "⚙️ In your profile you can change the interval, words per day, delivery hours, "
              "time zone, level, language to learn and bot language, or pause the bot.{tr_note}",
        "es": "ℹ️ <b>Cómo funciona el bot</b>\n\n"
              "📩 <b>Las palabras nuevas</b> llegan de una en una: {schedule}. Se eligen al azar "
              "de tu nivel (y de los niveles inferiores, si así lo elegiste), y no se repiten. Cada palabra "
              "recibida cuenta como aprendida.\n\n"
              "{card_rules}\n\n"
              "➕ <b>«Otra palabra»</b> envía una palabra extra al momento; no cuenta para el "
              "límite diario.\n\n"
              "📝 <b>Test del día</b> a las {quiz_hour}:00: hasta {daily} palabras al azar de las "
              "que recibiste ese día. El bot muestra la traducción y tú escribes la palabra "
              "{answer_rules} Un sinónimo con la misma traducción no cuenta como error: el bot te indicará qué palabra busca. Tras el segundo "
              "error recibes una pista; tras el tercero puedes ver la respuesta, pero entonces "
              "la palabra se volverá a preguntar al final del test.\n\n"
              "🏆 <b>Test semanal</b> los domingos, justo después del test del día: hasta "
              "{weekly} palabras de la semana.\n\n"
              "⛔ Hasta que no superes el test, no llegarán palabras nuevas. El horario continúa "
              "en cuanto lo superes.\n\n"
              "⚙️ En tu perfil puedes cambiar el intervalo, las palabras al día, el horario de "
              "envío, la zona horaria, el nivel, el idioma que aprendes y el idioma del bot, o poner el bot en pausa.{tr_note}",
    },
}

POS_NAMES = {
    "ru": {"noun": "существительное", "verb": "глагол", "adj": "прилагательное",
           "adv": "наречие", "prep": "предлог", "pron": "местоимение", "conj": "союз",
           "num": "числительное", "part": "частица", "interj": "междометие"},
    "en": {"noun": "noun", "verb": "verb", "adj": "adjective", "adv": "adverb",
           "prep": "preposition", "pron": "pronoun", "conj": "conjunction", "num": "numeral",
           "part": "particle", "interj": "interjection"},
    "es": {"noun": "sustantivo", "verb": "verbo", "adj": "adjetivo", "adv": "adverbio",
           "prep": "preposición", "pron": "pronombre", "conj": "conjunción", "num": "numeral",
           "part": "partícula", "interj": "interjección"},
}

# Названия городов для часовых поясов: (ru, en, es)
CITIES = {
    "Europe/Kaliningrad": ("Калининград", "Kaliningrad", "Kaliningrado"),
    "Europe/Moscow": ("Москва", "Moscow", "Moscú"),
    "Europe/Samara": ("Самара", "Samara", "Samara"),
    "Asia/Yekaterinburg": ("Екатеринбург", "Yekaterinburg", "Ekaterimburgo"),
    "Asia/Omsk": ("Омск", "Omsk", "Omsk"),
    "Asia/Novosibirsk": ("Новосибирск", "Novosibirsk", "Novosibirsk"),
    "Asia/Irkutsk": ("Иркутск", "Irkutsk", "Irkutsk"),
    "Asia/Vladivostok": ("Владивосток", "Vladivostok", "Vladivostok"),
    "Europe/London": ("Лондон", "London", "Londres"),
    "Europe/Paris": ("Париж", "Paris", "París"),
    "Europe/Berlin": ("Берлин", "Berlin", "Berlín"),
    "Europe/Madrid": ("Мадрид", "Madrid", "Madrid"),
    "America/New_York": ("Нью-Йорк", "New York", "Nueva York"),
    "America/Mexico_City": ("Мехико", "Mexico City", "Ciudad de México"),
    "America/Argentina/Buenos_Aires": ("Буэнос-Айрес", "Buenos Aires", "Buenos Aires"),
}
_CITY_INDEX = {"ru": 0, "en": 1, "es": 2}


def t(lang: str, key: str, **kwargs) -> str:
    texts = TEXTS[key]
    return texts.get(lang, texts[DEFAULT_UI]).format(**kwargs)


def all_variants(key: str) -> set[str]:
    """Текст на всех языках: нужен, чтобы узнавать кнопки меню на любом языке."""
    return set(TEXTS[key].values())


def level_name(lang: str, level: str) -> str:
    """A1…C2 как есть, тематический уровень — названием на языке бота."""
    return TEXTS[f"level_{level}"][lang] if f"level_{level}" in TEXTS else level


def pos_name(lang: str, pos: str) -> str:
    return POS_NAMES.get(lang, POS_NAMES[DEFAULT_UI])[pos]


def city(lang: str, tz: str) -> str:
    names = CITIES.get(tz)
    return names[_CITY_INDEX.get(lang, 0)] if names else tz
