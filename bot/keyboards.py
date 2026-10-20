from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)

from . import db
from .config import (DAY_END_OPTIONS, DAY_START_OPTIONS, INTERVAL_OPTIONS, LANGUAGES, TIMEZONES,
                     TOPICS,
                     WORDS_PER_DAY_OPTIONS)
from .i18n import UI_LANGUAGES, city, level_name, t


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
    """Только языки, для которых загружен словарь."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(t(lang, f"learn_{code}"), f"lang:{code}")]
        for code in LANGUAGES if db.available_levels(code)
    ])


def levels(lang: str, available: list[str]) -> InlineKeyboardMarkup:
    """Кнопки уровней по три в ряд и тематические наборы отдельными строками —
    только те, где есть слова."""
    cefr = [lvl for lvl in available if lvl not in TOPICS]
    rows = [[_button(lvl, f"level:{lvl}") for lvl in cefr[i:i + 3]] for i in range(0, len(cefr), 3)]
    rows += [[_button(level_name(lang, lvl), f"level:{lvl}")] for lvl in available if lvl in TOPICS]
    return InlineKeyboardMarkup(inline_keyboard=rows)


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
        [_button(t(lang, "btn_restart"), "profile:restart")],
    ])


def reveal(lang: str, item_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(t(lang, "btn_reveal"), f"reveal:{item_id}")],
    ])
