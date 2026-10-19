from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)

from .config import (DAY_END_OPTIONS, DAY_START_OPTIONS, INTERVAL_OPTIONS, LANGUAGES, TIMEZONES,
                     WORDS_PER_DAY_OPTIONS)
from .i18n import UI_LANGUAGES, city, t


def _button(text: str, data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=data)


def main_menu(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t(lang, "btn_more")),
                   KeyboardButton(text=t(lang, "btn_profile"))]],
        resize_keyboard=True,
    )


ui_languages = InlineKeyboardMarkup(inline_keyboard=[
    [_button(name, f"ui:{code}")] for code, name in UI_LANGUAGES.items()
])


def languages(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(t(lang, f"learn_{code}"), f"lang:{code}")] for code in LANGUAGES
    ])


def levels(available: list[str]) -> InlineKeyboardMarkup:
    """Кнопки уровней по три в ряд — только те уровни, где есть слова."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(lvl, f"level:{lvl}") for lvl in available[i:i + 3]]
        for i in range(0, len(available), 3)
    ])


def scope(lang: str, level: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(t(lang, "btn_scope_all", level=level), "scope:1")],
        [_button(t(lang, "btn_scope_only", level=level), "scope:0")],
    ])


def timezones(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(f"{city(lang, tz)} ({offset})", f"tz:{tz}")]
        for tz, offset in TIMEZONES.items()
    ])


def intervals(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(t(lang, f"every_{m}").capitalize(), f"set:interval:{m}")]
        for m in INTERVAL_OPTIONS
    ])


words_per_day = InlineKeyboardMarkup(inline_keyboard=[
    [_button(str(n), f"set:limit:{n}") for n in WORDS_PER_DAY_OPTIONS],
])

day_starts = InlineKeyboardMarkup(inline_keyboard=[
    [_button(f"{h}:00", f"set:start:{h}") for h in DAY_START_OPTIONS],
])

day_ends = InlineKeyboardMarkup(inline_keyboard=[
    [_button(f"{h}:00", f"set:end:{h}") for h in DAY_END_OPTIONS],
])


def profile(lang: str, paused: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(t(lang, "btn_interval"), "profile:interval"),
         _button(t(lang, "btn_limit"), "profile:limit")],
        [_button(t(lang, "btn_hours"), "profile:hours"),
         _button(t(lang, "btn_tz"), "profile:tz")],
        [_button(t(lang, "btn_level"), "profile:level"),
         _button(t(lang, "btn_learn"), "profile:learn")],
        [_button(t(lang, "btn_ui"), "profile:ui")],
        [_button(t(lang, "btn_help"), "profile:help")],
        [_button(t(lang, "btn_resume" if paused else "btn_pause"), "profile:pause")],
    ])


def reveal(lang: str, item_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(t(lang, "btn_reveal"), f"reveal:{item_id}")],
    ])
