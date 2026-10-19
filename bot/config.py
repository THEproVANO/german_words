import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB_PATH = os.getenv("DB_PATH", str(ROOT / "bot.db"))
DATA_DIR = ROOT / "data"

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
LANGUAGES = ["de"]

# Расписание слов по умолчанию: по одному слову каждые INTERVAL минут с DAY_START до DAY_END,
# но не больше WORDS_PER_DAY в день. Пользователь может изменить это в профиле
INTERVAL = 30
WORDS_PER_DAY = 15
DAY_START = 9
DAY_END = 21
INTERVAL_OPTIONS = [30, 60, 120]
WORDS_PER_DAY_OPTIONS = [5, 10, 15, 20, 25, 30]
DAY_START_OPTIONS = [6, 7, 8, 9, 10, 11, 12]
DAY_END_OPTIONS = [17, 18, 19, 20, 21]

# Время дневного теста. Слова, полученные после этого часа, относятся к следующему дню
QUIZ_HOUR = 22
DAILY_QUIZ_SIZE = 10
WEEKLY_QUIZ_SIZE = 40

DEFAULT_TZ = "Europe/Moscow"
# Часовой пояс по умолчанию в зависимости от выбранного языка бота
DEFAULT_TZ_BY_UI = {"ru": "Europe/Moscow", "en": "Europe/London", "fr": "Europe/Paris",
                    "es": "Europe/Madrid"}
# Часовые пояса для выбора в профиле; названия городов на разных языках — в i18n.CITIES
TIMEZONES = {
    "Europe/Kaliningrad": "UTC+2",
    "Europe/Moscow": "UTC+3",
    "Europe/Samara": "UTC+4",
    "Asia/Yekaterinburg": "UTC+5",
    "Asia/Omsk": "UTC+6",
    "Asia/Novosibirsk": "UTC+7",
    "Asia/Irkutsk": "UTC+8",
    "Asia/Vladivostok": "UTC+10",
    "Europe/London": "UTC+0/+1",
    "Europe/Paris": "UTC+1/+2",
    "Europe/Berlin": "UTC+1/+2",
    "Europe/Madrid": "UTC+1/+2",
    "America/New_York": "UTC−5/−4",
    "America/Mexico_City": "UTC−6",
    "America/Argentina/Buenos_Aires": "UTC−3",
}

TICK_SECONDS = 30
