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

# Расписание слов: WORDS_PER_DAY штук, равномерно с DAY_START до DAY_END
WORDS_PER_DAY = 15
DAY_START_MIN = 9 * 60
DAY_END_MIN = 21 * 60

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
