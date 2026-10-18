"""Логика рассылки слов и тестов. Общая для планировщика и обработчиков."""
import asyncio
import logging
import random
import sqlite3
from collections import defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from . import db, keyboards, words
from .config import (DAILY_QUIZ_SIZE, DAY_END_MIN, DAY_START_MIN, QUIZ_HOUR, TICK_SECONDS,
                     WEEKLY_QUIZ_SIZE, WORDS_PER_DAY)

log = logging.getLogger(__name__)

# Не даём планировщику и обработчикам одновременно менять данные одного пользователя
user_locks: defaultdict[int, asyncio.Lock] = defaultdict(asyncio.Lock)

SLOTS = [
    DAY_START_MIN + round(k * (DAY_END_MIN - DAY_START_MIN) / (WORDS_PER_DAY - 1))
    for k in range(WORDS_PER_DAY)
]


def local_now(user: sqlite3.Row) -> datetime:
    return datetime.now(ZoneInfo(user["tz"]))


def study_date(local: datetime) -> date:
    """Учебный день: слова после времени теста относятся к следующему дню."""
    d = local.date()
    return d + timedelta(days=1) if local.hour >= QUIZ_HOUR else d


def slot_index(local: datetime) -> int:
    """Сколько слотов рассылки уже наступило сегодня (0..WORDS_PER_DAY)."""
    minutes = local.hour * 60 + local.minute
    return sum(1 for s in SLOTS if s <= minutes)


# --- слова ---

async def send_new_word(bot: Bot, user: sqlite3.Row) -> bool:
    """Отправляет новое слово. Возвращает False, если слова закончились."""
    word = db.pick_new_word(user)
    if word is None:
        return False
    db.mark_sent(user["id"], word["id"], study_date(local_now(user)))
    await bot.send_message(user["id"], words.format_card(word))
    if db.pick_new_word(user) is None:
        await bot.send_message(
            user["id"],
            f"🎉 Это было последнее слово уровня {user['level']}! "
            "Выбери уровень выше в профиле, чтобы продолжить.",
        )
    return True


# --- тесты ---

async def send_question(bot: Bot, user_id: int, quiz_id: int) -> None:
    item = db.current_item(quiz_id)
    done, total = db.quiz_counts(quiz_id)
    await bot.send_message(user_id, words.quiz_question(db.get_word(item["word_id"]), done + 1, total))


async def start_quiz(bot: Bot, user: sqlite3.Row, kind: str, d: date, word_ids: list[int]) -> bool:
    """Создаёт тест. Возвращает True, если тест начался (были слова)."""
    size = DAILY_QUIZ_SIZE if kind == "daily" else WEEKLY_QUIZ_SIZE
    word_ids = random.sample(word_ids, min(size, len(word_ids)))
    quiz_id = db.create_quiz(user["id"], kind, d, word_ids)
    if not word_ids:
        return False
    if kind == "daily":
        intro = f"📝 <b>Тест дня</b>: {len(word_ids)} слов из изученных сегодня."
    else:
        intro = f"🏆 <b>Недельный тест</b>: {len(word_ids)} слов из изученных за неделю."
    await bot.send_message(
        user["id"],
        f"{intro}\n\nНапиши слово по-немецки: существительные — без артикля, "
        "глаголы — в инфинитиве.\nПока тест не пройден, новые слова не приходят.",
    )
    await send_question(bot, user["id"], quiz_id)
    return True


async def start_weekly_if_due(bot: Bot, user: sqlite3.Row, d: date) -> bool:
    """После дневного теста за воскресенье запускает недельный тест."""
    if d.weekday() != 6 or db.get_quiz(user["id"], "weekly", d):
        return False
    word_ids = db.words_for_dates(user["id"], d - timedelta(days=6), d)
    return await start_quiz(bot, user, "weekly", d, word_ids)


async def ensure_quizzes(bot: Bot, user: sqlite3.Row) -> None:
    """Запускает тесты за последний завершившийся учебный день, если их ещё не было."""
    if db.get_active_quiz(user["id"]):
        return
    d = study_date(local_now(user)) - timedelta(days=1)
    if not db.get_quiz(user["id"], "daily", d):
        if await start_quiz(bot, user, "daily", d, db.words_for_dates(user["id"], d, d)):
            return
    await start_weekly_if_due(bot, user, d)


async def finish_quiz(bot: Bot, user: sqlite3.Row, quiz: sqlite3.Row) -> None:
    db.finish_quiz(quiz["id"])
    if quiz["kind"] == "daily":
        text = "🎉 Тест дня пройден! Молодец."
    else:
        text = "🏆 Недельный тест пройден! Отличная работа."
    await bot.send_message(user["id"], text)
    if quiz["kind"] == "daily":
        if await start_weekly_if_due(bot, user, date.fromisoformat(quiz["study_date"])):
            return
    await ensure_quizzes(bot, user)
    if not db.get_active_quiz(user["id"]):
        await bot.send_message(user["id"], "Новые слова снова будут приходить по расписанию.")


async def handle_answer(bot: Bot, user: sqlite3.Row, quiz: sqlite3.Row, text: str) -> None:
    item = db.current_item(quiz["id"])
    word = db.get_word(item["word_id"])
    if words.is_correct(text, word):
        db.mark_item_done(item["id"])
        full = f"{word['article']} {word['word']}".strip()
        await bot.send_message(user["id"], f"✅ Верно! <b>{full}</b>")
        if db.current_item(quiz["id"]):
            await send_question(bot, user["id"], quiz["id"])
        else:
            await finish_quiz(bot, user, quiz)
        return

    attempts = item["attempts"] + 1
    db.set_attempts(item["id"], attempts)
    if attempts == 1:
        await bot.send_message(user["id"], "❌ Неверно, попробуй ещё раз.")
    elif attempts == 2:
        await bot.send_message(
            user["id"], f"❌ Неверно. Подсказка: <code>{words.hint(word, long=True)}</code>"
        )
    else:
        await bot.send_message(
            user["id"], "❌ Неверно. Попробуй ещё раз или посмотри ответ.",
            reply_markup=keyboards.reveal(item["id"]),
        )


async def reveal_answer(bot: Bot, user: sqlite3.Row, item_id: int) -> None:
    quiz = db.get_active_quiz(user["id"])
    item = db.current_item(quiz["id"]) if quiz else None
    if not item or item["id"] != item_id:
        return
    word = db.get_word(item["word_id"])
    db.move_item_to_end(item["id"], quiz["id"])
    await bot.send_message(
        user["id"],
        f"Правильный ответ:\n\n{words.format_card(word)}\n\n"
        "Это слово спросим ещё раз в конце теста.",
    )
    await send_question(bot, user["id"], quiz["id"])


# --- планировщик ---

async def process_user(bot: Bot, user: sqlite3.Row) -> None:
    await ensure_quizzes(bot, user)
    if db.get_active_quiz(user["id"]):
        return
    local = local_now(user)
    idx = slot_index(local)
    today = local.date().isoformat()
    if idx == 0 or (user["last_slot_date"] == today and user["last_slot_idx"] >= idx):
        return
    # Отправляем одно слово за текущий слот; пропущенные (например, во время теста) не догоняем
    db.update_user(user["id"], last_slot_date=today, last_slot_idx=idx)
    await send_new_word(bot, user)


async def scheduler(bot: Bot) -> None:
    while True:
        for user in db.active_users():
            async with user_locks[user["id"]]:
                user = db.get_user(user["id"])
                if user["paused"] or user["blocked"]:
                    continue
                try:
                    await process_user(bot, user)
                except TelegramForbiddenError:
                    db.update_user(user["id"], blocked=1)
                    log.info("Пользователь %s заблокировал бота", user["id"])
                except Exception:
                    log.exception("Ошибка при обработке пользователя %s", user["id"])
        await asyncio.sleep(TICK_SECONDS)
