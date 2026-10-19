from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from . import db, keyboards, service
from .config import (ADMIN_IDS, DAILY_QUIZ_SIZE, DEFAULT_TZ, DEFAULT_TZ_BY_UI, LANGUAGES,
                     LEVELS, QUIZ_HOUR, TIMEZONES, WEEKLY_QUIZ_SIZE)
from .i18n import CHOOSE_UI, UI_LANGUAGES, all_variants, city, t

router = Router()


def rules_text(user) -> str:
    return t(user["ui_lang"], "rules", schedule=service.schedule_text(user), quiz_hour=QUIZ_HOUR,
             daily=DAILY_QUIZ_SIZE, weekly=WEEKLY_QUIZ_SIZE)


def tz_label(lang: str, tz: str) -> str:
    return f"{city(lang, tz)} ({TIMEZONES[tz]})" if tz in TIMEZONES else tz


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id
    db.create_user(user_id, DEFAULT_TZ)
    user = db.get_user(user_id)
    if user["blocked"]:
        db.update_user(user_id, blocked=0)
    if user["level"] and user["last_slot_date"] is None:
        # Настройка не закончена: уровень выбран, но не ответил, включать ли уровни ниже
        lang = user["ui_lang"]
        await message.answer(t(lang, "ask_scope", level=user["level"]),
                             reply_markup=keyboards.scope(lang, user["level"]))
        return
    if user["level"]:
        lang = user["ui_lang"]
        await message.answer(t(lang, "welcome_back"), reply_markup=keyboards.main_menu(lang))
        quiz = db.get_active_quiz(user_id)
        if quiz:
            await service.send_question(bot, user, quiz["id"])
        return
    await message.answer(CHOOSE_UI, reply_markup=keyboards.ui_languages)


@router.callback_query(F.data.startswith("ui:"))
async def choose_ui(call: CallbackQuery) -> None:
    lang = call.data.split(":")[1]
    if lang not in UI_LANGUAGES:
        await call.answer()
        return
    user = db.get_user(call.from_user.id)
    if not user:
        await call.answer()
        return
    if user["level"]:
        # Смена языка из профиля
        db.update_user(user["id"], ui_lang=lang)
        await call.message.edit_text(t(lang, "ui_set", name=UI_LANGUAGES[lang]))
        await call.message.answer(t(lang, "welcome_back"), reply_markup=keyboards.main_menu(lang))
    else:
        # Первая настройка: заодно подставляем часовой пояс, типичный для этого языка
        db.update_user(user["id"], ui_lang=lang, tz=DEFAULT_TZ_BY_UI[lang])
        await call.message.edit_text(t(lang, "welcome"), reply_markup=keyboards.languages(lang))
    await call.answer()


@router.callback_query(F.data.startswith("lang:"))
async def choose_language(call: CallbackQuery) -> None:
    lang = call.data.split(":")[1]
    ui = db.get_user(call.from_user.id)["ui_lang"]
    if lang not in LANGUAGES:
        await call.answer(t(ui, "en_later"), show_alert=True)
        return
    db.update_user(call.from_user.id, lang=lang)
    await call.message.edit_text(t(ui, "lang_chosen", language=t(ui, f"learn_{lang}")),
                                 reply_markup=keyboards.levels)
    await call.answer()


@router.callback_query(F.data.startswith("level:"))
async def choose_level(call: CallbackQuery, bot: Bot) -> None:
    level = call.data.split(":")[1]
    user_id = call.from_user.id
    async with service.user_locks[user_id]:
        user = db.get_user(user_id)
        if not user or not user["lang"]:
            await call.answer(t(user["ui_lang"] if user else "ru", "choose_lang_first"),
                              show_alert=True)
            return
        lang = user["ui_lang"]
        db.update_user(user_id, level=level)
        await call.answer()
        if level == LEVELS[0]:
            # Ниже первого уровня ничего нет, спрашивать незачем
            db.update_user(user_id, include_lower=1)
            await call.message.edit_text(t(lang, "level_set", level=level))
            await finish_setup(bot, db.get_user(user_id))
            return
        await call.message.edit_text(t(lang, "ask_scope", level=level),
                                     reply_markup=keyboards.scope(lang, level))


@router.callback_query(F.data.startswith("scope:"))
async def choose_scope(call: CallbackQuery, bot: Bot) -> None:
    include_lower = int(call.data.split(":")[1])
    user_id = call.from_user.id
    async with service.user_locks[user_id]:
        db.update_user(user_id, include_lower=include_lower)
        user = db.get_user(user_id)
        lang = user["ui_lang"]
        await call.message.edit_text(
            f"{t(lang, 'level_set', level=user['level'])}\n{scope_text(user)}")
        await call.answer()
        await finish_setup(bot, user)


def scope_text(user) -> str:
    if user["level"] == LEVELS[0]:
        return user["level"]
    return t(user["ui_lang"], "scope_all" if user["include_lower"] else "scope_only",
             level=user["level"])


async def finish_setup(bot: Bot, user) -> None:
    """После первой настройки: правила и первое слово. При смене уровня из профиля — ничего."""
    if user["last_slot_date"] is not None:
        return
    lang = user["ui_lang"]
    await bot.send_message(user["id"], rules_text(user), reply_markup=keyboards.main_menu(lang))
    # Первое слово сразу, следующее — в ближайший слот по расписанию
    service.reset_schedule(user["id"])
    await bot.send_message(user["id"], t(lang, "first_word"))
    await service.send_new_word(bot, user)


@router.message(Command("id"))
async def cmd_id(message: Message) -> None:
    user = db.get_user(message.from_user.id)
    await message.answer(t(user["ui_lang"] if user else "ru", "your_id", id=message.from_user.id))


@router.message(Command("quiz"))
async def cmd_quiz(message: Message, bot: Bot) -> None:
    """Пробный тест для администратора: /quiz — за сегодня, /quiz week — за неделю."""
    user_id = message.from_user.id
    user = db.get_user(user_id)
    if user_id not in ADMIN_IDS or not user or not user["level"]:
        await message.answer(t(user["ui_lang"] if user else "ru", "no_quiz"))
        return
    weekly = "week" in (message.text or "")
    async with service.user_locks[user_id]:
        await service.start_test(bot, user, weekly)


@router.message(F.text.in_(all_variants("btn_more")))
async def more_word(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id
    async with service.user_locks[user_id]:
        user = db.get_user(user_id)
        if not user or not user["level"]:
            await message.answer(t(user["ui_lang"] if user else "ru", "setup_first"))
            return
        lang = user["ui_lang"]
        quiz = db.get_active_quiz(user_id)
        if quiz:
            await message.answer(t(lang, "quiz_first"))
            await service.send_question(bot, user, quiz["id"])
            return
        if not await service.send_new_word(bot, user):
            await message.answer(t(lang, "all_learned"))


def profile_text(user) -> str:
    lang = user["ui_lang"]
    learned, total = db.progress(user)
    if user["paused"]:
        status = t(lang, "status_paused")
    elif db.get_active_quiz(user["id"]):
        status = t(lang, "status_quiz")
    else:
        status = t(lang, "status_active")
    return t(lang, "profile", language=t(lang, f"learn_{user['lang']}"), level=scope_text(user),
             learned=learned, total=total, schedule=service.schedule_text(user),
             tz=tz_label(lang, user["tz"]), ui=UI_LANGUAGES[lang], status=status)


@router.message(F.text.in_(all_variants("btn_profile")))
async def show_profile(message: Message) -> None:
    user = db.get_user(message.from_user.id)
    if not user or not user["level"]:
        await message.answer(t(user["ui_lang"] if user else "ru", "setup_first"))
        return
    await message.answer(profile_text(user),
                         reply_markup=keyboards.profile(user["ui_lang"], bool(user["paused"])))


@router.callback_query(F.data.startswith("profile:"))
async def profile_action(call: CallbackQuery) -> None:
    action = call.data.split(":")[1]
    user = db.get_user(call.from_user.id)
    lang = user["ui_lang"]
    if action == "pause":
        db.update_user(user["id"], paused=0 if user["paused"] else 1)
        user = db.get_user(user["id"])
        await call.message.edit_text(profile_text(user),
                                     reply_markup=keyboards.profile(lang, bool(user["paused"])))
        await call.answer(t(lang, "pause_on" if user["paused"] else "pause_off"))
        return
    if action == "help":
        await call.message.answer(rules_text(user))
    elif action == "ui":
        await call.message.answer(CHOOSE_UI, reply_markup=keyboards.ui_languages)
    else:
        text, markup = {
            "level": ("ask_level", keyboards.levels),
            "tz": ("ask_tz", keyboards.timezones(lang)),
            "interval": ("ask_interval", keyboards.intervals(lang)),
            "limit": ("ask_limit", keyboards.words_per_day),
            "hours": ("ask_start", keyboards.day_starts),
        }[action]
        await call.message.answer(t(lang, text), reply_markup=markup)
    await call.answer()


@router.callback_query(F.data.startswith("tz:"))
async def choose_tz(call: CallbackQuery) -> None:
    tz = call.data.split(":", 1)[1]
    if tz in TIMEZONES:
        async with service.user_locks[call.from_user.id]:
            db.update_user(call.from_user.id, tz=tz)
            service.reset_schedule(call.from_user.id)
        lang = db.get_user(call.from_user.id)["ui_lang"]
        await call.message.edit_text(t(lang, "tz_set", tz=tz_label(lang, tz)))
    await call.answer()


@router.callback_query(F.data.startswith("set:"))
async def change_setting(call: CallbackQuery) -> None:
    _, name, value = call.data.split(":")
    user_id = call.from_user.id
    lang = db.get_user(user_id)["ui_lang"]
    if name == "start":
        # Время рассылки выбирается в два шага: сначала начало, потом конец
        db.update_user(user_id, day_start=int(value))
        await call.message.edit_text(t(lang, "ask_end", start=value),
                                     reply_markup=keyboards.day_ends)
        await call.answer()
        return
    column = {"interval": "interval_min", "limit": "words_per_day", "end": "day_end"}[name]
    async with service.user_locks[user_id]:
        db.update_user(user_id, **{column: int(value)})
        service.reset_schedule(user_id)
    schedule = service.schedule_text(db.get_user(user_id))
    await call.message.edit_text(t(lang, "schedule_set", schedule=schedule))
    await call.answer()


@router.callback_query(F.data.startswith("reveal:"))
async def reveal(call: CallbackQuery, bot: Bot) -> None:
    user_id = call.from_user.id
    async with service.user_locks[user_id]:
        await call.message.edit_reply_markup(reply_markup=None)
        await call.answer()
        await service.reveal_answer(bot, db.get_user(user_id), int(call.data.split(":")[1]))


@router.message(F.text)
async def text_answer(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id
    async with service.user_locks[user_id]:
        quiz = db.get_active_quiz(user_id)
        user = db.get_user(user_id)
        if not quiz:
            lang = user["ui_lang"] if user else "ru"
            reply_markup = keyboards.main_menu(lang) if user and user["level"] else None
            await message.answer(t(lang, "no_quiz"), reply_markup=reply_markup)
            return
        await service.handle_answer(bot, user, quiz, message.text)
