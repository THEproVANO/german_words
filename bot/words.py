import csv
import html
import re
import sqlite3

from . import db
from .config import DATA_DIR, LEVELS
from .i18n import POS_NAMES, pos_name, t

FIELDS = ["level", "pos", "article", "word", "plural", "praesens", "praeteritum",
          "perfekt", "translations", "example", "example_ru"]


def load_words() -> int:
    """Загружает словари data/<lang>_words.csv в базу. Возвращает число слов."""
    total = 0
    for path in sorted(DATA_DIR.glob("*_words.csv")):
        lang = path.name.split("_")[0]
        rows = []
        with path.open(encoding="utf-8") as f:
            for n, row in enumerate(csv.DictReader(f, delimiter=";"), start=2):
                row = {k: (row.get(k) or "").strip() for k in FIELDS}
                if row["level"] not in LEVELS or row["pos"] not in POS_NAMES["ru"]:
                    raise ValueError(f"{path.name}, строка {n}: неверный уровень или часть речи")
                if not (row["word"] and row["translations"] and row["example"]):
                    raise ValueError(f"{path.name}, строка {n}: не заполнены обязательные поля")
                row["lang"] = lang
                row["key"] = f"{lang}:{row['pos']}:{row['article']}:{row['word']}"
                rows.append(row)
        db.upsert_words(rows)
        total += len(rows)
    return total


def _bold(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(text))


def format_card(w: sqlite3.Row, lang: str) -> str:
    e = html.escape
    head = f"<b>{e(w['article'] + ' ' if w['article'] else '')}{e(w['word'])}</b>"
    if w["pos"] == "noun":
        if w["plural"] == "-":
            head += f", <i>{t(lang, 'no_plural')}</i>"
        elif w["plural"] == "pl":
            head += f", <i>{t(lang, 'plural_only')}</i>"
        elif w["plural"]:
            head += f", die {e(w['plural'])}"
    elif w["pos"] == "verb":
        if w["praesens"]:
            head += f" ({e(w['praesens'])})"
        forms = [f for f in (w["praeteritum"], w["perfekt"]) if f]
        if forms:
            head += " — " + " — ".join(e(f) for f in forms)

    return (
        f"<i>{pos_name(lang, w['pos'])}</i> · {w['level']}\n"
        f"{head}\n"
        f"🇷🇺 {e(w['translations'])}\n\n"
        f"{_bold(w['example'])}\n"
        f"<i>{e(w['example_ru'])}</i>"
    )


def _normalize(text: str) -> str:
    text = text.lower().strip()
    for src, dst in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(src, dst)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^(der|die|das) ", "", text)
    text = re.sub(r"^sich ", "", text)
    return text


def is_correct(answer: str, w: sqlite3.Row) -> bool:
    return _normalize(answer) == _normalize(w["word"])


def answer_text(w: sqlite3.Row) -> str:
    """Слово без артикля и без «sich» — то, что пользователь должен ввести."""
    return re.sub(r"^sich ", "", w["word"])


def hint(w: sqlite3.Row, long: bool = False) -> str:
    word = answer_text(w)
    shown = max(1, len(word) // 2) if long else 1
    return word[:shown] + "…"


def quiz_question(w: sqlite3.Row, number: int, total: int, lang: str) -> str:
    return t(lang, "question", n=number, total=total, tr=html.escape(w["translations"]),
             pos=pos_name(lang, w["pos"]), hint=html.escape(hint(w)))
