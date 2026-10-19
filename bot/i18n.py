"""Тексты интерфейса на всех языках бота. t(lang, key, **kwargs) возвращает нужный текст."""

UI_LANGUAGES = {"ru": "🇷🇺 Русский", "en": "🇬🇧 English", "fr": "🇫🇷 Français", "es": "🇪🇸 Español"}
DEFAULT_UI = "ru"

# Первый экран: язык пользователя ещё неизвестен, поэтому вопрос сразу на всех языках
CHOOSE_UI = ("🌐 Выбери язык бота\nChoose the bot language\n"
             "Choisis la langue du bot\nElige el idioma del bot")

TEXTS = {
    # --- старт ---
    "welcome": {
        "ru": "Привет! 👋 Я помогу выучить иностранные слова.\n\nКакой язык будем изучать?",
        "en": "Hi! 👋 I'll help you learn foreign words.\n\nWhich language do you want to learn?",
        "fr": "Salut ! 👋 Je vais t'aider à apprendre des mots étrangers.\n\n"
              "Quelle langue veux-tu apprendre ?",
        "es": "¡Hola! 👋 Te ayudaré a aprender palabras extranjeras.\n\n¿Qué idioma quieres aprender?",
    },
    "ui_set": {
        "ru": "Язык бота: {name} ✅",
        "en": "Bot language: {name} ✅",
        "fr": "Langue du bot : {name} ✅",
        "es": "Idioma del bot: {name} ✅",
    },
    "learn_de": {"ru": "🇩🇪 Немецкий", "en": "🇩🇪 German", "fr": "🇩🇪 Allemand", "es": "🇩🇪 Alemán"},
    "learn_en_soon": {
        "ru": "🇬🇧 Английский (скоро)",
        "en": "🇬🇧 English (coming soon)",
        "fr": "🇬🇧 Anglais (bientôt)",
        "es": "🇬🇧 Inglés (próximamente)",
    },
    "en_later": {
        "ru": "Английский появится позже 🙂",
        "en": "English is coming later 🙂",
        "fr": "L'anglais arrivera plus tard 🙂",
        "es": "El inglés llegará más tarde 🙂",
    },
    "lang_chosen": {
        "ru": "Язык: {language}\n\nВыбери свой уровень:",
        "en": "Language: {language}\n\nChoose your level:",
        "fr": "Langue : {language}\n\nChoisis ton niveau :",
        "es": "Idioma: {language}\n\nElige tu nivel:",
    },
    "choose_lang_first": {
        "ru": "Сначала выбери язык: /start",
        "en": "Choose a language first: /start",
        "fr": "Choisis d'abord une langue : /start",
        "es": "Primero elige un idioma: /start",
    },
    "level_set": {
        "ru": "Уровень: <b>{level}</b> ✅",
        "en": "Level: <b>{level}</b> ✅",
        "fr": "Niveau : <b>{level}</b> ✅",
        "es": "Nivel: <b>{level}</b> ✅",
    },
    "first_word": {
        "ru": "Вот твоё первое слово:",
        "en": "Here is your first word:",
        "fr": "Voici ton premier mot :",
        "es": "Aquí tienes tu primera palabra:",
    },
    "welcome_back": {
        "ru": "С возвращением! 👋",
        "en": "Welcome back! 👋",
        "fr": "Bon retour ! 👋",
        "es": "¡Bienvenido de nuevo! 👋",
    },
    "setup_first": {
        "ru": "Сначала настрой бота: /start",
        "en": "Set up the bot first: /start",
        "fr": "Configure d'abord le bot : /start",
        "es": "Primero configura el bot: /start",
    },

    # --- главное меню и слова ---
    "btn_more": {"ru": "➕ Ещё слово", "en": "➕ One more word", "fr": "➕ Encore un mot",
                 "es": "➕ Otra palabra"},
    "btn_profile": {"ru": "👤 Профиль", "en": "👤 Profile", "fr": "👤 Profil", "es": "👤 Perfil"},
    "quiz_first": {
        "ru": "Сначала пройди тест 📝",
        "en": "Finish the quiz first 📝",
        "fr": "Termine d'abord le test 📝",
        "es": "Primero termina el test 📝",
    },
    "all_learned": {
        "ru": "Все слова этого уровня уже изучены 🎉 Выбери уровень выше в профиле.",
        "en": "You've learned all the words of this level 🎉 Choose a higher level in your profile.",
        "fr": "Tu as appris tous les mots de ce niveau 🎉 Choisis un niveau supérieur dans ton profil.",
        "es": "Ya has aprendido todas las palabras de este nivel 🎉 "
              "Elige un nivel superior en tu perfil.",
    },
    "last_word": {
        "ru": "🎉 Это было последнее слово уровня {level}! "
              "Выбери уровень выше в профиле, чтобы продолжить.",
        "en": "🎉 That was the last word of level {level}! "
              "Choose a higher level in your profile to continue.",
        "fr": "🎉 C'était le dernier mot du niveau {level} ! "
              "Choisis un niveau supérieur dans ton profil pour continuer.",
        "es": "🎉 ¡Esa era la última palabra del nivel {level}! "
              "Elige un nivel superior en tu perfil para continuar.",
    },
    "no_quiz": {
        "ru": "Сейчас нет активного теста. Используй кнопки меню 👇",
        "en": "There's no active quiz right now. Use the menu buttons 👇",
        "fr": "Aucun test en cours. Utilise les boutons du menu 👇",
        "es": "No hay ningún test activo. Usa los botones del menú 👇",
    },
    "no_plural": {"ru": "нет мн. ч.", "en": "no plural", "fr": "pas de pluriel", "es": "sin plural"},
    "plural_only": {"ru": "только мн. ч.", "en": "plural only", "fr": "pluriel uniquement",
                    "es": "solo plural"},

    # --- профиль ---
    "profile": {
        "ru": "👤 <b>Профиль</b>\n\nЯзык: {language}\nУровень: <b>{level}</b>\n"
              "Изучено слов: <b>{learned}</b> из {total}\nРассылка: {schedule}\n"
              "Часовой пояс: {tz}\nЯзык бота: {ui}\nСтатус: {status}",
        "en": "👤 <b>Profile</b>\n\nLanguage: {language}\nLevel: <b>{level}</b>\n"
              "Words learned: <b>{learned}</b> of {total}\nSchedule: {schedule}\n"
              "Time zone: {tz}\nBot language: {ui}\nStatus: {status}",
        "fr": "👤 <b>Profil</b>\n\nLangue : {language}\nNiveau : <b>{level}</b>\n"
              "Mots appris : <b>{learned}</b> sur {total}\nEnvoi : {schedule}\n"
              "Fuseau horaire : {tz}\nLangue du bot : {ui}\nStatut : {status}",
        "es": "👤 <b>Perfil</b>\n\nIdioma: {language}\nNivel: <b>{level}</b>\n"
              "Palabras aprendidas: <b>{learned}</b> de {total}\nEnvío: {schedule}\n"
              "Zona horaria: {tz}\nIdioma del bot: {ui}\nEstado: {status}",
    },
    "status_paused": {"ru": "⏸ на паузе", "en": "⏸ paused", "fr": "⏸ en pause", "es": "⏸ en pausa"},
    "status_quiz": {
        "ru": "📝 ждёт прохождения теста",
        "en": "📝 waiting for the quiz",
        "fr": "📝 test en attente",
        "es": "📝 test pendiente",
    },
    "status_active": {"ru": "✅ активен", "en": "✅ active", "fr": "✅ actif", "es": "✅ activo"},
    "schedule": {
        "ru": "{interval} с {start}:00 до {end}:00, не больше {limit} в день",
        "en": "{interval} from {start}:00 to {end}:00, up to {limit} a day",
        "fr": "{interval} de {start}h à {end}h, {limit} par jour maximum",
        "es": "{interval} de {start}:00 a {end}:00, máximo {limit} al día",
    },
    "every_30": {"ru": "каждые 30 минут", "en": "every 30 minutes", "fr": "toutes les 30 minutes",
                 "es": "cada 30 minutos"},
    "every_60": {"ru": "каждый час", "en": "every hour", "fr": "toutes les heures",
                 "es": "cada hora"},
    "every_120": {"ru": "каждые 2 часа", "en": "every 2 hours", "fr": "toutes les 2 heures",
                  "es": "cada 2 horas"},
    "btn_interval": {"ru": "⏱ Интервал", "en": "⏱ Interval", "fr": "⏱ Intervalle",
                     "es": "⏱ Intervalo"},
    "btn_limit": {"ru": "🔢 Слов в день", "en": "🔢 Words per day", "fr": "🔢 Mots par jour",
                  "es": "🔢 Palabras al día"},
    "btn_hours": {"ru": "🕘 Время рассылки", "en": "🕘 Delivery hours", "fr": "🕘 Heures d'envoi",
                  "es": "🕘 Horario de envío"},
    "btn_tz": {"ru": "🕒 Часовой пояс", "en": "🕒 Time zone", "fr": "🕒 Fuseau horaire",
               "es": "🕒 Zona horaria"},
    "btn_level": {"ru": "📚 Сменить уровень", "en": "📚 Change level", "fr": "📚 Changer de niveau",
                  "es": "📚 Cambiar nivel"},
    "btn_ui": {"ru": "🌐 Язык бота", "en": "🌐 Bot language", "fr": "🌐 Langue du bot",
               "es": "🌐 Idioma del bot"},
    "btn_help": {"ru": "ℹ️ Как работает бот", "en": "ℹ️ How the bot works",
                 "fr": "ℹ️ Comment fonctionne le bot", "es": "ℹ️ Cómo funciona el bot"},
    "btn_pause": {"ru": "⏸ Пауза", "en": "⏸ Pause", "fr": "⏸ Pause", "es": "⏸ Pausa"},
    "btn_resume": {"ru": "▶️ Продолжить", "en": "▶️ Resume", "fr": "▶️ Reprendre",
                   "es": "▶️ Reanudar"},
    "pause_on": {"ru": "Пауза включена", "en": "Paused", "fr": "Pause activée",
                 "es": "Pausa activada"},
    "pause_off": {"ru": "Продолжаем!", "en": "Let's continue!", "fr": "On continue !",
                  "es": "¡Seguimos!"},
    "ask_level": {"ru": "Выбери уровень:", "en": "Choose your level:", "fr": "Choisis ton niveau :",
                  "es": "Elige tu nivel:"},
    "ask_tz": {"ru": "Выбери часовой пояс:", "en": "Choose your time zone:",
               "fr": "Choisis ton fuseau horaire :", "es": "Elige tu zona horaria:"},
    "tz_set": {"ru": "Часовой пояс: {tz} ✅", "en": "Time zone: {tz} ✅",
               "fr": "Fuseau horaire : {tz} ✅", "es": "Zona horaria: {tz} ✅"},
    "ask_interval": {
        "ru": "Как часто присылать слова?",
        "en": "How often should I send words?",
        "fr": "À quelle fréquence envoyer les mots ?",
        "es": "¿Cada cuánto envío las palabras?",
    },
    "ask_limit": {
        "ru": "Сколько слов присылать в день?",
        "en": "How many words per day?",
        "fr": "Combien de mots par jour ?",
        "es": "¿Cuántas palabras al día?",
    },
    "ask_start": {
        "ru": "С какого часа присылать слова?",
        "en": "From what time should I send words?",
        "fr": "À partir de quelle heure envoyer les mots ?",
        "es": "¿Desde qué hora envío las palabras?",
    },
    "ask_end": {
        "ru": "Начало: {start}:00\n\nДо какого часа присылать слова?",
        "en": "Start: {start}:00\n\nUntil what time should I send words?",
        "fr": "Début : {start}h\n\nJusqu'à quelle heure envoyer les mots ?",
        "es": "Inicio: {start}:00\n\n¿Hasta qué hora envío las palabras?",
    },
    "schedule_set": {
        "ru": "✅ Рассылка: {schedule}",
        "en": "✅ Schedule: {schedule}",
        "fr": "✅ Envoi : {schedule}",
        "es": "✅ Envío: {schedule}",
    },

    # --- тесты ---
    "quiz_daily": {
        "ru": "📝 <b>Тест дня</b>: {n} слов из изученных сегодня.",
        "en": "📝 <b>Daily quiz</b>: {n} words from today.",
        "fr": "📝 <b>Test du jour</b> : {n} mots appris aujourd'hui.",
        "es": "📝 <b>Test del día</b>: {n} palabras de hoy.",
    },
    "quiz_weekly": {
        "ru": "🏆 <b>Недельный тест</b>: {n} слов из изученных за неделю.",
        "en": "🏆 <b>Weekly quiz</b>: {n} words from this week.",
        "fr": "🏆 <b>Test de la semaine</b> : {n} mots appris cette semaine.",
        "es": "🏆 <b>Test semanal</b>: {n} palabras de esta semana.",
    },
    "quiz_rules": {
        "ru": "Напиши слово по-немецки: существительные — без артикля, глаголы — в инфинитиве.\n"
              "Пока тест не пройден, новые слова не приходят.",
        "en": "Type the word in German: nouns without the article, verbs in the infinitive.\n"
              "No new words until you pass the quiz.",
        "fr": "Écris le mot en allemand : les noms sans article, les verbes à l'infinitif.\n"
              "Pas de nouveaux mots tant que le test n'est pas réussi.",
        "es": "Escribe la palabra en alemán: los sustantivos sin artículo, "
              "los verbos en infinitivo.\nNo llegarán palabras nuevas hasta que termines el test.",
    },
    "question": {
        "ru": "Вопрос {n}/{total}\n🇷🇺 <b>{tr}</b> ({pos})\nНачинается на: <code>{hint}</code>",
        "en": "Question {n}/{total}\n🇷🇺 <b>{tr}</b> ({pos})\nStarts with: <code>{hint}</code>",
        "fr": "Question {n}/{total}\n🇷🇺 <b>{tr}</b> ({pos})\nCommence par : <code>{hint}</code>",
        "es": "Pregunta {n}/{total}\n🇷🇺 <b>{tr}</b> ({pos})\nEmpieza por: <code>{hint}</code>",
    },
    "correct": {"ru": "✅ Верно! <b>{word}</b>", "en": "✅ Correct! <b>{word}</b>",
                "fr": "✅ Correct ! <b>{word}</b>", "es": "✅ ¡Correcto! <b>{word}</b>"},
    "wrong1": {
        "ru": "❌ Неверно, попробуй ещё раз.",
        "en": "❌ Wrong, try again.",
        "fr": "❌ Faux, réessaie.",
        "es": "❌ Incorrecto, inténtalo de nuevo.",
    },
    "wrong2": {
        "ru": "❌ Неверно. Подсказка: <code>{hint}</code>",
        "en": "❌ Wrong. Hint: <code>{hint}</code>",
        "fr": "❌ Faux. Indice : <code>{hint}</code>",
        "es": "❌ Incorrecto. Pista: <code>{hint}</code>",
    },
    "wrong3": {
        "ru": "❌ Неверно. Попробуй ещё раз или посмотри ответ.",
        "en": "❌ Wrong. Try again or look at the answer.",
        "fr": "❌ Faux. Réessaie ou regarde la réponse.",
        "es": "❌ Incorrecto. Inténtalo de nuevo o mira la respuesta.",
    },
    "btn_reveal": {"ru": "👀 Показать ответ", "en": "👀 Show answer", "fr": "👀 Voir la réponse",
                   "es": "👀 Ver la respuesta"},
    "revealed": {
        "ru": "Правильный ответ:\n\n{card}\n\nЭто слово спросим ещё раз в конце теста.",
        "en": "Correct answer:\n\n{card}\n\nThis word will be asked again at the end of the quiz.",
        "fr": "Bonne réponse :\n\n{card}\n\nCe mot sera redemandé à la fin du test.",
        "es": "Respuesta correcta:\n\n{card}\n\nEsta palabra se volverá a preguntar al final del test.",
    },
    "daily_done": {
        "ru": "🎉 Тест дня пройден! Молодец.",
        "en": "🎉 Daily quiz passed! Well done.",
        "fr": "🎉 Test du jour réussi ! Bravo.",
        "es": "🎉 ¡Test del día superado! ¡Bien hecho!",
    },
    "weekly_done": {
        "ru": "🏆 Недельный тест пройден! Отличная работа.",
        "en": "🏆 Weekly quiz passed! Great job.",
        "fr": "🏆 Test de la semaine réussi ! Excellent travail.",
        "es": "🏆 ¡Test semanal superado! ¡Excelente trabajo!",
    },
    "resume": {
        "ru": "Новые слова снова будут приходить по расписанию.",
        "en": "New words will arrive on schedule again.",
        "fr": "Les nouveaux mots arriveront de nouveau selon le programme.",
        "es": "Las palabras nuevas volverán a llegar según el horario.",
    },

    # --- объём уровня ---
    "ask_scope": {
        "ru": "Уровень: <b>{level}</b> ✅\n\nКакие слова присылать?",
        "en": "Level: <b>{level}</b> ✅\n\nWhich words should I send?",
        "fr": "Niveau : <b>{level}</b> ✅\n\nQuels mots dois-je envoyer ?",
        "es": "Nivel: <b>{level}</b> ✅\n\n¿Qué palabras envío?",
    },
    "btn_scope_all": {
        "ru": "📚 {level} и все уровни ниже",
        "en": "📚 {level} and all lower levels",
        "fr": "📚 {level} et tous les niveaux inférieurs",
        "es": "📚 {level} y todos los niveles inferiores",
    },
    "btn_scope_only": {
        "ru": "🎯 Только {level}",
        "en": "🎯 Only {level}",
        "fr": "🎯 Seulement {level}",
        "es": "🎯 Solo {level}",
    },
    "scope_all": {"ru": "{level} и ниже", "en": "{level} and below",
                  "fr": "{level} et inférieurs", "es": "{level} e inferiores"},
    "scope_only": {"ru": "только {level}", "en": "only {level}", "fr": "seulement {level}",
                   "es": "solo {level}"},

    # --- сводки после тестов ---
    "quiz_stats": {
        "ru": "Результат теста:\n✅ с первой попытки: {first}\n✏️ с ошибками: {mistakes}\n"
              "👀 ответ подсмотрен: {revealed}",
        "en": "Quiz result:\n✅ first try: {first}\n✏️ after mistakes: {mistakes}\n"
              "👀 answer shown: {revealed}",
        "fr": "Résultat du test :\n✅ du premier coup : {first}\n✏️ après des erreurs : {mistakes}\n"
              "👀 réponse affichée : {revealed}",
        "es": "Resultado del test:\n✅ a la primera: {first}\n✏️ tras errores: {mistakes}\n"
              "👀 respuesta mostrada: {revealed}",
    },
    "summary_daily": {
        "ru": "📊 <b>Итоги дня</b>\nСегодня изучено слов: <b>{today}</b>\n"
              "Всего изучено: <b>{learned}</b> из {total} ({percent}%)\n\n{stats}",
        "en": "📊 <b>Today's summary</b>\nWords learned today: <b>{today}</b>\n"
              "Total learned: <b>{learned}</b> of {total} ({percent}%)\n\n{stats}",
        "fr": "📊 <b>Bilan du jour</b>\nMots appris aujourd'hui : <b>{today}</b>\n"
              "Total appris : <b>{learned}</b> sur {total} ({percent} %)\n\n{stats}",
        "es": "📊 <b>Resumen del día</b>\nPalabras aprendidas hoy: <b>{today}</b>\n"
              "Total aprendidas: <b>{learned}</b> de {total} ({percent}%)\n\n{stats}",
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
        "fr": "📈 <b>Bilan de la semaine</b>\nMots appris cette semaine : <b>{week}</b> "
              "({avg} par jour en moyenne)\nTotal appris : <b>{learned}</b> sur {total} ({percent} %)\n\n"
              "⚙️ Réglages actuels : {schedule}.\nSoit jusqu'à <b>{per_day}</b> mots par jour et jusqu'à "
              "<b>{per_week}</b> par semaine.\n{forecast}\n\n{stats}",
        "es": "📈 <b>Resumen de la semana</b>\nAprendidas esta semana: <b>{week}</b> "
              "({avg} al día de media)\nTotal aprendidas: <b>{learned}</b> de {total} ({percent}%)\n\n"
              "⚙️ Ajustes actuales: {schedule}.\nEso son hasta <b>{per_day}</b> palabras al día y hasta "
              "<b>{per_week}</b> a la semana.\n{forecast}\n\n{stats}",
    },
    "forecast": {
        "ru": "🏁 При таком темпе уровень {level} будет пройден примерно через {days} дн. — к {date}.",
        "en": "🏁 At this pace you'll finish level {level} in about {days} days — by {date}.",
        "fr": "🏁 À ce rythme, tu termineras le niveau {level} dans environ {days} jours, vers le {date}.",
        "es": "🏁 A este ritmo terminarás el nivel {level} en unos {days} días, hacia el {date}.",
    },
    "forecast_done": {
        "ru": "🎉 Все слова уровня {level} уже изучены!",
        "en": "🎉 You've already learned all the words of level {level}!",
        "fr": "🎉 Tu as déjà appris tous les mots du niveau {level} !",
        "es": "🎉 ¡Ya has aprendido todas las palabras del nivel {level}!",
    },

    # --- служебные команды ---
    "test_no_words": {
        "ru": "Пока нет слов для теста — сначала получи несколько слов.",
        "en": "No words for a quiz yet — get a few words first.",
        "fr": "Pas encore de mots pour un test — reçois d'abord quelques mots.",
        "es": "Aún no hay palabras para un test: primero recibe algunas palabras.",
    },
    "your_id": {
        "ru": "Твой Telegram ID: <code>{id}</code>",
        "en": "Your Telegram ID: <code>{id}</code>",
        "fr": "Ton identifiant Telegram : <code>{id}</code>",
        "es": "Tu ID de Telegram: <code>{id}</code>",
    },

    # --- описание работы бота ---
    "rules": {
        "ru": "ℹ️ <b>Как работает бот</b>\n\n"
              "📩 <b>Новые слова</b> приходят по одному: {schedule}. Слова выбираются случайно "
              "из твоего уровня (и уровней ниже, если ты так выбрал) и не повторяются. Каждое полученное слово "
              "считается изученным.\n\n"
              "➕ <b>«Ещё слово»</b> присылает новое слово вне очереди, в дневной лимит оно "
              "не входит.\n\n"
              "📝 <b>Тест дня</b> в {quiz_hour}:00: до {daily} случайных слов из полученных "
              "за день. Бот пишет перевод, а ты вводишь слово по-немецки: существительные без "
              "артикля, глаголы в инфинитиве. Регистр не важен, вместо ä, ö, ü, ß можно писать "
              "ae, oe, ue, ss. После второй ошибки бот покажет подсказку, после третьей можно "
              "посмотреть ответ, но тогда слово спросят ещё раз в конце теста.\n\n"
              "🏆 <b>Недельный тест</b> по воскресеньям сразу после теста дня: до {weekly} "
              "слов за неделю.\n\n"
              "⛔ Пока тест не пройден, новые слова не приходят. Расписание продолжится сразу "
              "после прохождения теста.\n\n"
              "⚙️ В профиле можно изменить интервал, количество слов в день, время рассылки, "
              "часовой пояс, уровень и язык бота, а также поставить бота на паузу.",
        "en": "ℹ️ <b>How the bot works</b>\n\n"
              "📩 <b>New words</b> arrive one at a time: {schedule}. Words are picked at random "
              "from your level (and the levels below, if you chose so), and they never repeat. Every word you "
              "receive counts as learned.\n\n"
              "➕ <b>“One more word”</b> sends an extra word right away; it doesn't count toward "
              "the daily limit.\n\n"
              "📝 <b>Daily quiz</b> at {quiz_hour}:00: up to {daily} random words from the ones "
              "you got that day. The bot shows the translation and you type the word in German: "
              "nouns without the article, verbs in the infinitive. Case doesn't matter, and you "
              "can type ae, oe, ue, ss instead of ä, ö, ü, ß. After the second mistake you get "
              "a hint; after the third you can see the answer, but then the word will be asked "
              "again at the end of the quiz.\n\n"
              "🏆 <b>Weekly quiz</b> on Sundays right after the daily quiz: up to {weekly} words "
              "from the week.\n\n"
              "⛔ No new words arrive until you pass the quiz. The schedule resumes right after "
              "you pass it.\n\n"
              "⚙️ In your profile you can change the interval, words per day, delivery hours, "
              "time zone, level and bot language, or pause the bot.\n\n"
              "🇷🇺 For now, word translations are in Russian only.",
        "fr": "ℹ️ <b>Comment fonctionne le bot</b>\n\n"
              "📩 <b>Les nouveaux mots</b> arrivent un par un : {schedule}. Ils sont choisis au "
              "hasard dans ton niveau (et les niveaux inférieurs si tu l'as choisi), sans répétition. Chaque "
              "mot reçu compte comme appris.\n\n"
              "➕ <b>« Encore un mot »</b> envoie tout de suite un mot supplémentaire ; il ne "
              "compte pas dans la limite quotidienne.\n\n"
              "📝 <b>Test du jour</b> à {quiz_hour}h : jusqu'à {daily} mots au hasard parmi ceux "
              "reçus dans la journée. Le bot affiche la traduction et tu écris le mot en "
              "allemand : les noms sans article, les verbes à l'infinitif. Les majuscules ne "
              "comptent pas, et tu peux écrire ae, oe, ue, ss au lieu de ä, ö, ü, ß. Après la "
              "deuxième erreur, tu reçois un indice ; après la troisième, tu peux voir la "
              "réponse, mais le mot sera alors redemandé à la fin du test.\n\n"
              "🏆 <b>Test de la semaine</b> le dimanche, juste après le test du jour : jusqu'à "
              "{weekly} mots de la semaine.\n\n"
              "⛔ Tant que le test n'est pas réussi, aucun nouveau mot n'arrive. Le programme "
              "reprend dès que tu l'as réussi.\n\n"
              "⚙️ Dans ton profil, tu peux changer l'intervalle, le nombre de mots par jour, "
              "les heures d'envoi, le fuseau horaire, le niveau et la langue du bot, ou mettre "
              "le bot en pause.\n\n"
              "🇷🇺 Pour l'instant, les traductions des mots sont uniquement en russe.",
        "es": "ℹ️ <b>Cómo funciona el bot</b>\n\n"
              "📩 <b>Las palabras nuevas</b> llegan de una en una: {schedule}. Se eligen al azar "
              "de tu nivel (y de los niveles inferiores, si así lo elegiste), y no se repiten. Cada palabra "
              "recibida cuenta como aprendida.\n\n"
              "➕ <b>«Otra palabra»</b> envía una palabra extra al momento; no cuenta para el "
              "límite diario.\n\n"
              "📝 <b>Test del día</b> a las {quiz_hour}:00: hasta {daily} palabras al azar de las "
              "que recibiste ese día. El bot muestra la traducción y tú escribes la palabra en "
              "alemán: los sustantivos sin artículo, los verbos en infinitivo. Las mayúsculas no "
              "importan, y puedes escribir ae, oe, ue, ss en lugar de ä, ö, ü, ß. Tras el segundo "
              "error recibes una pista; tras el tercero puedes ver la respuesta, pero entonces "
              "la palabra se volverá a preguntar al final del test.\n\n"
              "🏆 <b>Test semanal</b> los domingos, justo después del test del día: hasta "
              "{weekly} palabras de la semana.\n\n"
              "⛔ Hasta que no superes el test, no llegarán palabras nuevas. El horario continúa "
              "en cuanto lo superes.\n\n"
              "⚙️ En tu perfil puedes cambiar el intervalo, las palabras al día, el horario de "
              "envío, la zona horaria, el nivel y el idioma del bot, o poner el bot en pausa.\n\n"
              "🇷🇺 De momento, las traducciones de las palabras solo están en ruso.",
    },
}

POS_NAMES = {
    "ru": {"noun": "существительное", "verb": "глагол", "adj": "прилагательное",
           "adv": "наречие", "prep": "предлог", "pron": "местоимение", "conj": "союз",
           "num": "числительное", "part": "частица", "interj": "междометие"},
    "en": {"noun": "noun", "verb": "verb", "adj": "adjective", "adv": "adverb",
           "prep": "preposition", "pron": "pronoun", "conj": "conjunction", "num": "numeral",
           "part": "particle", "interj": "interjection"},
    "fr": {"noun": "nom", "verb": "verbe", "adj": "adjectif", "adv": "adverbe",
           "prep": "préposition", "pron": "pronom", "conj": "conjonction", "num": "numéral",
           "part": "particule", "interj": "interjection"},
    "es": {"noun": "sustantivo", "verb": "verbo", "adj": "adjetivo", "adv": "adverbio",
           "prep": "preposición", "pron": "pronombre", "conj": "conjunción", "num": "numeral",
           "part": "partícula", "interj": "interjección"},
}

# Названия городов для часовых поясов: (ru, en, fr, es)
CITIES = {
    "Europe/Kaliningrad": ("Калининград", "Kaliningrad", "Kaliningrad", "Kaliningrado"),
    "Europe/Moscow": ("Москва", "Moscow", "Moscou", "Moscú"),
    "Europe/Samara": ("Самара", "Samara", "Samara", "Samara"),
    "Asia/Yekaterinburg": ("Екатеринбург", "Yekaterinburg", "Iekaterinbourg", "Ekaterimburgo"),
    "Asia/Omsk": ("Омск", "Omsk", "Omsk", "Omsk"),
    "Asia/Novosibirsk": ("Новосибирск", "Novosibirsk", "Novossibirsk", "Novosibirsk"),
    "Asia/Irkutsk": ("Иркутск", "Irkutsk", "Irkoutsk", "Irkutsk"),
    "Asia/Vladivostok": ("Владивосток", "Vladivostok", "Vladivostok", "Vladivostok"),
    "Europe/London": ("Лондон", "London", "Londres", "Londres"),
    "Europe/Paris": ("Париж", "Paris", "Paris", "París"),
    "Europe/Berlin": ("Берлин", "Berlin", "Berlin", "Berlín"),
    "Europe/Madrid": ("Мадрид", "Madrid", "Madrid", "Madrid"),
    "America/New_York": ("Нью-Йорк", "New York", "New York", "Nueva York"),
    "America/Mexico_City": ("Мехико", "Mexico City", "Mexico", "Ciudad de México"),
    "America/Argentina/Buenos_Aires": ("Буэнос-Айрес", "Buenos Aires", "Buenos Aires",
                                       "Buenos Aires"),
}
_CITY_INDEX = {"ru": 0, "en": 1, "fr": 2, "es": 3}


def t(lang: str, key: str, **kwargs) -> str:
    texts = TEXTS[key]
    return texts.get(lang, texts[DEFAULT_UI]).format(**kwargs)


def all_variants(key: str) -> set[str]:
    """Текст на всех языках: нужен, чтобы узнавать кнопки меню на любом языке."""
    return set(TEXTS[key].values())


def pos_name(lang: str, pos: str) -> str:
    return POS_NAMES.get(lang, POS_NAMES[DEFAULT_UI])[pos]


def city(lang: str, tz: str) -> str:
    names = CITIES.get(tz)
    return names[_CITY_INDEX.get(lang, 0)] if names else tz
