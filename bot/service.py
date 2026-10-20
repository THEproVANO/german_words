"""Логика рассылки слов и тестов. Общая для планировщика и обработчиков."""
import asyncio
import html
import logging
import math
import random
import sqlite3
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from . import db, keyboards, words
from .i18n import level_name, t
from .config import DAILY_QUIZ_SIZE, QUIZ_HOUR, TICK_SECONDS, WEEKLY_QUIZ_SIZE

log = logging.getLogger(__name__)

# Не даём планировщику и обработчикам одновременно менять данные одного пользователя
user_locks: defaultdict[int, asyncio.Lock] = defaultdict(asyncio.Lock)


def slots(user: sqlite3.Row) -> list[int]:
    """Время отправки слов (в минутах от полуночи) по настройкам пользователя."""
    times = range(user["day_start"] * 60, user["day_end"] * 60 + 1, user["interval_min"])
    return list(times)[: user["words_per_day"]]


def schedule_text(user: sqlite3.Row) -> str:
    lang = user["ui_lang"]
    return t(lang, "schedule", interval=t(lang, f"every_{user['interval_min']}"),
             start=user["day_start"], end=user["day_end"], limit=user["words_per_day"])


def local_now(user: sqlite3.Row) -> datetime:
    return datetime.now(ZoneInfo(user["tz"]))


def study_date(local: datetime) -> date:
    """Учебный день: слова после времени теста относятся к следующему дню."""
    d = local.date()
    return d + timedelta(days=1) if local.hour >= QUIZ_HOUR else d


def slot_index(user: sqlite3.Row, local: datetime) -> int:
    """Сколько слотов рассылки уже наступило сегодня."""
    minutes = local.hour * 60 + local.minute
    return sum(1 for s in slots(user) if s <= minutes)


def reset_schedule(user_id: int) -> None:
    """Считает уже наступившие сегодня слоты отправленными, чтобы после смены
    настроек или регистрации слова не пришли все разом."""
    user = db.get_user(user_id)
    local = local_now(user)
    db.update_user(user_id, last_slot_date=local.date().isoformat(),
                   last_slot_idx=slot_index(user, local))


# --- слова ---

async def send_new_word(bot: Bot, user: sqlite3.Row) -> bool:
    """Отправляет новое слово. Возвращает False, если слова закончились."""
    word = db.pick_new_word(user)
    if word is None:
        return False
    db.mark_sent(user["id"], word["id"], study_date(local_now(user)))
    lang = user["ui_lang"]
    await bot.send_message(user["id"], words.format_card(word, lang))
    if db.pick_new_word(user) is None:
        await bot.send_message(user["id"], t(lang, "last_word", level=level_name(lang, user["level"])))
    return True


# --- тесты ---

async def send_question(bot: Bot, user: sqlite3.Row, quiz_id: int) -> None:
    item = db.current_item(quiz_id)
    done, total = db.quiz_counts(quiz_id)
    question = words.quiz_question(db.get_word(item["word_id"]), done + 1, total, user["ui_lang"])
    await bot.send_message(user["id"], question)


async def start_quiz(bot: Bot, user: sqlite3.Row, kind: str, d: date, word_ids: list[int]) -> bool:
    """Создаёт тест. Возвращает True, если тест начался (были слова).
    kind: daily, weekly или test_daily / test_weekly — пробные тесты по команде /quiz."""
    weekly = kind.endswith("weekly")
    size = WEEKLY_QUIZ_SIZE if weekly else DAILY_QUIZ_SIZE
    word_ids = random.sample(word_ids, min(size, len(word_ids)))
    quiz_id = db.create_quiz(user["id"], kind, d, word_ids)
    if not word_ids:
        return False
    lang = user["ui_lang"]
    intro = t(lang, "quiz_weekly" if weekly else "quiz_daily", n=len(word_ids))
    rules = t(lang, "quiz_rules", answer_rules=t(lang, f"answer_rules_{user['lang']}"))
    await bot.send_message(user["id"], f"{intro}\n\n{rules}")
    await send_question(bot, user, quiz_id)
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


async def start_test(bot: Bot, user: sqlite3.Row, weekly: bool) -> None:
    """Пробный тест по команде /quiz: слова за сегодня или за последние 7 дней."""
    quiz = db.get_active_quiz(user["id"])
    if quiz:
        await send_question(bot, user, quiz["id"])
        return
    d = study_date(local_now(user))
    word_ids = db.words_for_dates(user["id"], d - timedelta(days=6 if weekly else 0), d)
    if not word_ids:
        await bot.send_message(user["id"], t(user["ui_lang"], "test_no_words"))
        return
    # У пробного теста дата — момент создания, чтобы не занимать место настоящего теста дня
    await start_quiz(bot, user, "test_weekly" if weekly else "test_daily",
                     datetime.now(timezone.utc), word_ids)


def summary_text(user: sqlite3.Row, quiz: sqlite3.Row) -> str:
    """Сводка после теста: прогресс, результат теста, а для недельного — темп и прогноз."""
    lang = user["ui_lang"]
    first, mistakes, revealed = db.quiz_stats(quiz["id"])
    stats = t(lang, "quiz_stats", first=first, mistakes=mistakes, revealed=revealed)
    learned, total = db.progress(user)
    percent = round(100 * learned / total) if total else 0
    if quiz["kind"].startswith("test_"):
        d = study_date(local_now(user))
    else:
        d = date.fromisoformat(quiz["study_date"])

    if not quiz["kind"].endswith("weekly"):
        today = len(db.words_for_dates(user["id"], d, d))
        return t(lang, "summary_daily", today=today, learned=learned, total=total,
                 percent=percent, stats=stats)

    week = len(db.words_for_dates(user["id"], d - timedelta(days=6), d))
    per_day = len(slots(user))
    remaining = total - learned
    if remaining <= 0 or per_day == 0:
        forecast = t(lang, "forecast_done", level=level_name(lang, user["level"]))
    else:
        days = math.ceil(remaining / per_day)
        finish = (local_now(user).date() + timedelta(days=days)).strftime("%d.%m.%Y")
        forecast = t(lang, "forecast", level=level_name(lang, user["level"]), days=days, date=finish)
    avg = f"{week / 7:.1f}" if lang == "en" else f"{week / 7:.1f}".replace(".", ",")
    return t(lang, "summary_weekly", week=week, avg=avg, learned=learned,
             total=total, percent=percent, schedule=schedule_text(user), per_day=per_day,
             per_week=per_day * 7, forecast=forecast, stats=stats)


async def finish_quiz(bot: Bot, user: sqlite3.Row, quiz: sqlite3.Row) -> None:
    db.finish_quiz(quiz["id"])
    lang = user["ui_lang"]
    done = "weekly_done" if quiz["kind"].endswith("weekly") else "daily_done"
    await bot.send_message(user["id"], t(lang, done))
    await bot.send_message(user["id"], summary_text(user, quiz))
    if quiz["kind"] == "daily":
        if await start_weekly_if_due(bot, user, date.fromisoformat(quiz["study_date"])):
            return
    await ensure_quizzes(bot, user)
    if not db.get_active_quiz(user["id"]):
        await bot.send_message(user["id"], t(lang, "resume"))


async def handle_answer(bot: Bot, user: sqlite3.Row, quiz: sqlite3.Row, text: str) -> None:
    lang = user["ui_lang"]
    item = db.current_item(quiz["id"])
    word = db.get_word(item["word_id"])
    if words.is_correct(text, word):
        db.mark_item_done(item["id"])
        full = f"{word['article']} {word['word']}".strip()
        await bot.send_message(user["id"], t(lang, "correct", word=full))
        if db.current_item(quiz["id"]):
            await send_question(bot, user, quiz["id"])
        else:
            await finish_quiz(bot, user, quiz)
        return
    if words.is_synonym(text, word):
        # Синоним не считается ошибкой: просто подсказываем, какое слово загадано
        await bot.send_message(user["id"], t(lang, "synonym", answer=html.escape(text.strip()),
                                             hint=words.hint(word, long=True)))
        return

    attempts = item["attempts"] + 1
    db.set_attempts(item["id"], attempts)
    if attempts == 1:
        await bot.send_message(user["id"], t(lang, "wrong1"))
    elif attempts == 2:
        await bot.send_message(user["id"], t(lang, "wrong2", hint=words.hint(word, long=True)))
    else:
        await bot.send_message(user["id"], t(lang, "wrong3"),
                               reply_markup=keyboards.reveal(lang, item["id"]))


async def reveal_answer(bot: Bot, user: sqlite3.Row, item_id: int) -> None:
    quiz = db.get_active_quiz(user["id"])
    item = db.current_item(quiz["id"]) if quiz else None
    if not item or item["id"] != item_id:
        return
    word = db.get_word(item["word_id"])
    db.move_item_to_end(item["id"], quiz["id"])
    lang = user["ui_lang"]
    await bot.send_message(user["id"], t(lang, "revealed", card=words.format_card(word, lang)))
    await send_question(bot, user, quiz["id"])


# --- планировщик ---

async def process_user(bot: Bot, user: sqlite3.Row) -> None:
    await ensure_quizzes(bot, user)
    if db.get_active_quiz(user["id"]):
        return
    local = local_now(user)
    idx = slot_index(user, local)
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
