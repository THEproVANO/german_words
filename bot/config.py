import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB_PATH = os.getenv("DB_PATH", str(ROOT / "bot.db"))
DATA_DIR = ROOT / "data"

LEVELS = ["A1", "A2", "B1", "B2"]
LANGUAGES = {"de": "🇩🇪 Немецкий"}

# Расписание слов по умолчанию: по одному слову каждые INTERVAL минут с DAY_START до DAY_END,
# но не больше WORDS_PER_DAY в день. Пользователь может изменить это в профиле
INTERVAL = 30
WORDS_PER_DAY = 15
DAY_START = 9
DAY_END = 21
INTERVAL_OPTIONS = {30: "каждые 30 минут", 60: "каждый час", 120: "каждые 2 часа"}
WORDS_PER_DAY_OPTIONS = [5, 10, 15, 20, 25, 30]
DAY_START_OPTIONS = [6, 7, 8, 9, 10, 11, 12]
DAY_END_OPTIONS = [17, 18, 19, 20, 21]

# Время дневного теста. Слова, полученные после этого часа, относятся к следующему дню
QUIZ_HOUR = 22
DAILY_QUIZ_SIZE = 10
WEEKLY_QUIZ_SIZE = 40

DEFAULT_TZ = "Europe/Moscow"
TIMEZONES = {
    "Europe/Kaliningrad": "Калининград (UTC+2)",
    "Europe/Moscow": "Москва (UTC+3)",
    "Europe/Samara": "Самара (UTC+4)",
    "Asia/Yekaterinburg": "Екатеринбург (UTC+5)",
    "Asia/Omsk": "Омск (UTC+6)",
    "Asia/Novosibirsk": "Новосибирск (UTC+7)",
    "Asia/Irkutsk": "Иркутск (UTC+8)",
    "Asia/Vladivostok": "Владивосток (UTC+10)",
    "Europe/Berlin": "Берлин (UTC+1/+2)",
}

TICK_SECONDS = 30
