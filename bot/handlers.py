from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from . import db, keyboards, service
from .config import (DAILY_QUIZ_SIZE, DEFAULT_TZ, INTERVAL_OPTIONS, LANGUAGES, QUIZ_HOUR,
                     TIMEZONES, WEEKLY_QUIZ_SIZE)

router = Router()


def schedule_text(user) -> str:
    return (f"{INTERVAL_OPTIONS[user['interval_min']]} с {user['day_start']}:00 "
            f"до {user['day_end']}:00, не больше {user['words_per_day']} в день")


def rules_text(user) -> str:
    return (
        "ℹ️ <b>Как работает бот</b>\n\n"
        f"📩 <b>Новые слова</b> приходят по одному: {schedule_text(user)}. "
        "Слова выбираются случайно из твоего уровня и всех уровней ниже и не повторяются. "
        "Каждое полученное слово считается изученным.\n\n"
        "➕ <b>«Ещё слово»</b> присылает новое слово вне очереди, в дневной лимит оно не входит.\n\n"
        f"📝 <b>Тест дня</b> в {QUIZ_HOUR}:00: до {DAILY_QUIZ_SIZE} случайных слов из полученных "
        "за день. Бот пишет перевод, а ты вводишь слово по-немецки: существительные без "
        "артикля, глаголы в инфинитиве. Регистр не важен, вместо ä, ö, ü, ß можно писать "
        "ae, oe, ue, ss. После второй ошибки бот покажет подсказку, после третьей можно "
        "посмотреть ответ, но тогда слово спросят ещё раз в конце теста.\n\n"
        f"🏆 <b>Недельный тест</b> по воскресеньям сразу после теста дня: до {WEEKLY_QUIZ_SIZE} "
        "слов за неделю.\n\n"
        "⛔ Пока тест не пройден, новые слова не приходят. Расписание продолжится "
        "сразу после прохождения теста.\n\n"
        "⚙️ В профиле можно изменить интервал, количество слов в день, время рассылки, "
        "часовой пояс и уровень, а также поставить бота на паузу."
    )


@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id
    db.create_user(user_id, DEFAULT_TZ)
    user = db.get_user(user_id)
    if user["blocked"]:
        db.update_user(user_id, blocked=0)
    if user["level"]:
        await message.answer("С возвращением! 👋", reply_markup=keyboards.main_menu)
        quiz = db.get_active_quiz(user_id)
        if quiz:
            await service.send_question(bot, user_id, quiz["id"])
        return
    await message.answer(
        "Привет! 👋 Я помогу выучить иностранные слова.\n\nКакой язык будем изучать?",
        reply_markup=keyboards.languages,
    )


@router.callback_query(F.data.startswith("lang:"))
async def choose_language(call: CallbackQuery) -> None:
    lang = call.data.split(":")[1]
    if lang not in LANGUAGES:
        await call.answer("Английский появится позже 🙂", show_alert=True)
        return
    db.update_user(call.from_user.id, lang=lang)
    await call.message.edit_text(f"Язык: {LANGUAGES[lang]}\n\nВыбери свой уровень:",
                                 reply_markup=keyboards.levels)
    await call.answer()


@router.callback_query(F.data.startswith("level:"))
async def choose_level(call: CallbackQuery, bot: Bot) -> None:
    level = call.data.split(":")[1]
    user_id = call.from_user.id
    async with service.user_locks[user_id]:
        user = db.get_user(user_id)
        if not user or not user["lang"]:
            await call.answer("Сначала выбери язык: /start", show_alert=True)
            return
        first_time = user["level"] is None
        db.update_user(user_id, level=level)
        await call.message.edit_text(f"Уровень: <b>{level}</b> ✅")
        await call.answer()
        if not first_time:
            return
        user = db.get_user(user_id)
        await bot.send_message(user_id, rules_text(user), reply_markup=keyboards.main_menu)
        # Первое слово сразу, следующее — в ближайший слот по расписанию
        service.reset_schedule(user_id)
        await bot.send_message(user_id, "Вот твоё первое слово:")
        await service.send_new_word(bot, user)


@router.message(F.text == keyboards.BTN_MORE)
async def more_word(message: Message, bot: Bot) -> None:
    user_id = message.from_user.id
    async with service.user_locks[user_id]:
        user = db.get_user(user_id)
        if not user or not user["level"]:
            await message.answer("Сначала настрой бота: /start")
            return
        quiz = db.get_active_quiz(user_id)
        if quiz:
            await message.answer("Сначала пройди тест 📝")
            await service.send_question(bot, user_id, quiz["id"])
            return
        if not await service.send_new_word(bot, user):
            await message.answer("Все слова этого уровня уже изучены 🎉 Выбери уровень выше в профиле.")


def profile_text(user) -> str:
    learned, total = db.progress(user)
    if user["paused"]:
        status = "⏸ на паузе"
    elif db.get_active_quiz(user["id"]):
        status = "📝 ждёт прохождения теста"
    else:
        status = "✅ активен"
    return (
        "👤 <b>Профиль</b>\n\n"
        f"Язык: {LANGUAGES.get(user['lang'], '—')}\n"
        f"Уровень: <b>{user['level']}</b>\n"
        f"Изучено слов: <b>{learned}</b> из {total}\n"
        f"Рассылка: {schedule_text(user)}\n"
        f"Часовой пояс: {TIMEZONES.get(user['tz'], user['tz'])}\n"
        f"Статус: {status}"
    )


@router.message(F.text == keyboards.BTN_PROFILE)
async def show_profile(message: Message) -> None:
    user = db.get_user(message.from_user.id)
    if not user or not user["level"]:
        await message.answer("Сначала настрой бота: /start")
        return
    await message.answer(profile_text(user), reply_markup=keyboards.profile(bool(user["paused"])))


@router.callback_query(F.data == "profile:level")
async def profile_level(call: CallbackQuery) -> None:
    await call.message.answer("Выбери уровень:", reply_markup=keyboards.levels)
    await call.answer()


@router.callback_query(F.data == "profile:tz")
async def profile_tz(call: CallbackQuery) -> None:
    await call.message.answer("Выбери часовой пояс:", reply_markup=keyboards.timezones)
    await call.answer()


@router.callback_query(F.data.startswith("tz:"))
async def choose_tz(call: CallbackQuery) -> None:
    tz = call.data.split(":", 1)[1]
    if tz in TIMEZONES:
        async with service.user_locks[call.from_user.id]:
            db.update_user(call.from_user.id, tz=tz)
            service.reset_schedule(call.from_user.id)
        await call.message.edit_text(f"Часовой пояс: {TIMEZONES[tz]} ✅")
    await call.answer()


@router.callback_query(F.data == "profile:help")
async def profile_help(call: CallbackQuery) -> None:
    await call.message.answer(rules_text(db.get_user(call.from_user.id)))
    await call.answer()


@router.callback_query(F.data == "profile:interval")
async def profile_interval(call: CallbackQuery) -> None:
    await call.message.answer("Как часто присылать слова?", reply_markup=keyboards.intervals)
    await call.answer()


@router.callback_query(F.data == "profile:limit")
async def profile_limit(call: CallbackQuery) -> None:
    await call.message.answer("Сколько слов присылать в день?",
                              reply_markup=keyboards.words_per_day)
    await call.answer()


@router.callback_query(F.data == "profile:hours")
async def profile_hours(call: CallbackQuery) -> None:
    await call.message.answer("С какого часа присылать слова?", reply_markup=keyboards.day_starts)
    await call.answer()


@router.callback_query(F.data.startswith("set:"))
async def change_setting(call: CallbackQuery) -> None:
    _, name, value = call.data.split(":")
    user_id = call.from_user.id
    if name == "start":
        # Время рассылки выбирается в два шага: сначала начало, потом конец
        db.update_user(user_id, day_start=int(value))
        await call.message.edit_text(f"Начало: {value}:00\n\nДо какого часа присылать слова?",
                                     reply_markup=keyboards.day_ends)
        await call.answer()
        return
    column = {"interval": "interval_min", "limit": "words_per_day", "end": "day_end"}[name]
    async with service.user_locks[user_id]:
        db.update_user(user_id, **{column: int(value)})
        service.reset_schedule(user_id)
    await call.message.edit_text(f"✅ Рассылка: {schedule_text(db.get_user(user_id))}")
    await call.answer()


@router.callback_query(F.data == "profile:pause")
async def toggle_pause(call: CallbackQuery) -> None:
    user = db.get_user(call.from_user.id)
    db.update_user(user["id"], paused=0 if user["paused"] else 1)
    user = db.get_user(user["id"])
    await call.message.edit_text(profile_text(user),
                                 reply_markup=keyboards.profile(bool(user["paused"])))
    await call.answer("Пауза включена" if user["paused"] else "Продолжаем!")


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
        if not quiz:
            await message.answer("Сейчас нет активного теста. Используй кнопки меню 👇",
                                 reply_markup=keyboards.main_menu)
            return
        await service.handle_answer(bot, db.get_user(user_id), quiz, message.text)
