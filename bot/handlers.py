from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from . import db, keyboards, service
from .config import DEFAULT_TZ, LANGUAGES, TIMEZONES

router = Router()

RULES = (
    "Как это работает:\n"
    "• с 9:00 до 21:00 приходит 15 новых слов;\n"
    "• кнопка «Ещё слово» присылает слово вне очереди;\n"
    "• в 22:00 — тест на 10 слов за день. Пока он не пройден, новые слова не приходят;\n"
    "• в воскресенье после теста дня — недельный тест на 40 слов.\n\n"
    "Удачи! 🍀"
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
        await bot.send_message(user_id, RULES, reply_markup=keyboards.main_menu)
        # Первое слово сразу, следующее — в ближайший слот по расписанию
        user = db.get_user(user_id)
        local = service.local_now(user)
        db.update_user(user_id, last_slot_date=local.date().isoformat(),
                       last_slot_idx=service.slot_index(local))
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
        db.update_user(call.from_user.id, tz=tz)
        await call.message.edit_text(f"Часовой пояс: {TIMEZONES[tz]} ✅")
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
