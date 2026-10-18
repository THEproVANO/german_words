from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)

from .config import (DAY_END_OPTIONS, DAY_START_OPTIONS, INTERVAL_OPTIONS, LEVELS, TIMEZONES,
                     WORDS_PER_DAY_OPTIONS)

BTN_MORE = "➕ Ещё слово"
BTN_PROFILE = "👤 Профиль"

main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=BTN_MORE), KeyboardButton(text=BTN_PROFILE)]],
    resize_keyboard=True,
)

languages = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🇩🇪 Немецкий", callback_data="lang:de")],
    [InlineKeyboardButton(text="🇬🇧 Английский (скоро)", callback_data="lang:en")],
])

levels = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=lvl, callback_data=f"level:{lvl}") for lvl in LEVELS],
])

timezones = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=name, callback_data=f"tz:{tz}")]
    for tz, name in TIMEZONES.items()
])


intervals = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=name.capitalize(), callback_data=f"set:interval:{minutes}")]
    for minutes, name in INTERVAL_OPTIONS.items()
])

words_per_day = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=str(n), callback_data=f"set:limit:{n}")
     for n in WORDS_PER_DAY_OPTIONS],
])

day_starts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"{h}:00", callback_data=f"set:start:{h}")
     for h in DAY_START_OPTIONS],
])

day_ends = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"{h}:00", callback_data=f"set:end:{h}")
     for h in DAY_END_OPTIONS],
])


def profile(paused: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏱ Интервал", callback_data="profile:interval"),
         InlineKeyboardButton(text="🔢 Слов в день", callback_data="profile:limit")],
        [InlineKeyboardButton(text="🕘 Время рассылки", callback_data="profile:hours"),
         InlineKeyboardButton(text="🕒 Часовой пояс", callback_data="profile:tz")],
        [InlineKeyboardButton(text="📚 Сменить уровень", callback_data="profile:level")],
        [InlineKeyboardButton(text="ℹ️ Как работает бот", callback_data="profile:help")],
        [InlineKeyboardButton(
            text="▶️ Продолжить" if paused else "⏸ Пауза",
            callback_data="profile:pause",
        )],
    ])


def reveal(item_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👀 Показать ответ", callback_data=f"reveal:{item_id}")],
    ])
