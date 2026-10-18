from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)

from .config import LEVELS, TIMEZONES

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


def profile(paused: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Сменить уровень", callback_data="profile:level")],
        [InlineKeyboardButton(text="🕒 Часовой пояс", callback_data="profile:tz")],
        [InlineKeyboardButton(
            text="▶️ Продолжить" if paused else "⏸ Пауза",
            callback_data="profile:pause",
        )],
    ])


def reveal(item_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👀 Показать ответ", callback_data=f"reveal:{item_id}")],
    ])
