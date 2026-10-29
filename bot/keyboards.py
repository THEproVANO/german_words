from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)

from . import db
from .config import DAY_START_OPTIONS, LANGUAGES, TIMEZONES, TOPICS, TRANSLATION_LANGS
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
    """Только языки, для которых загружен словарь (с переводом на язык бота, если он свой).
    Язык самого бота не предлагаем: учить свой язык незачем."""
    def tl(code: str) -> str:
        return lang if lang in TRANSLATION_LANGS and code != lang else "ru"
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(t(lang, f"learn_{code}"), f"lang:{code}")]
        for code in LANGUAGES if code != lang and db.available_levels(code, tl(code))
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


def _rows(buttons: list[InlineKeyboardButton], per_row: int) -> list[list[InlineKeyboardButton]]:
    return [buttons[i:i + per_row] for i in range(0, len(buttons), per_row)]


day_starts = InlineKeyboardMarkup(inline_keyboard=[
    [_button(f"{h}:00", f"sch:s:{h}") for h in DAY_START_OPTIONS],
])


def word_counts(start: int, options: list[int]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=_rows(
        [_button(str(n), f"sch:c:{start}:{n}") for n in options], 6))


def quiz_times(start: int, count: int, options: list[int]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=_rows(
        [_button(f"{m // 60}:{m % 60:02d}", f"sch:q:{start}:{count}:{m}") for m in options], 4))


def profile(lang: str, paused: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [_button(t(lang, "btn_schedule"), "profile:schedule")],
        [_button(t(lang, "btn_tz"), "profile:tz")],
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
