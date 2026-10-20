import csv
import html
import re
import sqlite3
import unicodedata

from . import db
from .config import ALL_LEVELS, DATA_DIR, TOPICS, TRANSLATION_LANGS
from .i18n import POS_NAMES, level_name, pos_name, t

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
                if row["level"] not in ALL_LEVELS or row["pos"] not in POS_NAMES["ru"]:
                    raise ValueError(f"{path.name}, строка {n}: неверный уровень или часть речи")
                if not (row["word"] and row["translations"] and row["example"]):
                    raise ValueError(f"{path.name}, строка {n}: не заполнены обязательные поля")
                row["lang"] = lang
                row["key"] = f"{lang}:{row['pos']}:{row['article']}:{row['word']}"
                if row["level"] in TOPICS:
                    # Тематический набор может повторять слова из A1–C2, поэтому ключ свой
                    row["key"] = f"{row['level']}:{row['key']}"
                rows.append(row)
        _add_translations(lang, rows)
        db.upsert_words(rows)
        total += len(rows)
    return total


# Флаги языков: изучаемого слова и перевода
FLAGS = {"ru": "🇷🇺", "de": "🇩🇪", "en": "🇬🇧", "es": "🇪🇸"}


def _add_translations(lang: str, rows: list[dict]) -> None:
    """Подставляет переводы на другие языки бота из data/translations/<lang>_<tl>.csv
    (ключ;перевод;пример). Слова без перевода этим пользователям не присылаются."""
    for tl in TRANSLATION_LANGS:
        path = DATA_DIR / "translations" / f"{lang}_{tl}.csv"
        found = {}
        if path.exists():
            with path.open(encoding="utf-8") as f:
                for parts in csv.reader(f, delimiter=";"):
                    if len(parts) == 3 and parts[1].strip() and parts[2].strip():
                        found[parts[0]] = (parts[1].strip(), parts[2].strip())
        for row in rows:
            row[f"translations_{tl}"], row[f"example_{tl}"] = found.get(row["key"], ("", ""))


def translation(w: sqlite3.Row, tl: str) -> tuple[str, str, str]:
    """(переводы, перевод примера, флаг) на языке tl; если перевода нет — русские."""
    if tl != "ru" and w[f"translations_{tl}"]:
        return w[f"translations_{tl}"], w[f"example_{tl}"], FLAGS[tl]
    return w["translations"], w["example_ru"], FLAGS["ru"]


def word_line(w: sqlite3.Row, tl: str) -> str:
    """Строка для списка слов: «<b>der Apfel</b> — яблоко»."""
    word = f"{w['article']} {w['word']}".strip()
    return f"{FLAGS[w['lang']]} <b>{html.escape(word)}</b> — {html.escape(translation(w, tl)[0])}"


def _bold(text: str) -> str:
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(text))


def format_card(w: sqlite3.Row, lang: str, tl: str = "ru") -> str:
    e = html.escape
    tr, example_tr, flag = translation(w, tl)
    article = w["article"]
    if w["lang"] == "es" and w["plural"] == "pl":
        # Испанские слова только во мн. ч. показываем с артиклем мн. ч.: las vacaciones
        article = {"el": "los", "la": "las"}.get(article, article)
    head = f"<b>{e(article + ' ' if article else '')}{e(w['word'])}</b>"
    if w["pos"] == "noun":
        if w["plural"] == "-":
            head += f", <i>{t(lang, 'no_plural')}</i>"
        elif w["plural"] == "pl":
            head += f", <i>{t(lang, 'plural_only')}</i>"
        elif w["plural"]:
            # В немецком множественное число всегда с артиклем die
            plural = f"die {w['plural']}" if w["lang"] == "de" else w["plural"]
            head += f", {e(plural)}"
    elif w["pos"] == "verb":
        if w["praesens"]:
            head += f" ({e(w['praesens'])})"
        forms = [f for f in (w["praeteritum"], w["perfekt"]) if f]
        if forms:
            head += " — " + " — ".join(e(f) for f in forms)

    return (
        f"{FLAGS[w['lang']]} <i>{pos_name(lang, w['pos'])}</i> · {level_name(lang, w['level'])}\n"
        f"{head}\n"
        f"{flag} {e(tr)}\n\n"
        f"{_bold(w['example'])}\n"
        f"<i>{e(example_tr)}</i>"
    )


# Что можно не вводить в ответе: артикли, немецкое «sich», английское «to»
_OPTIONAL_PREFIX = {"de": r"^(der|die|das|sich) ", "en": r"^(the|an|a|to) ",
                    "es": r"^(el|la|los|las|un|una) "}


def _normalize(text: str, lang: str) -> str:
    text = text.lower().strip()
    if lang == "de":
        for src, dst in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
            text = text.replace(src, dst)
    elif lang == "es":
        # Ударения и тильда не обязательны: «nino» = «niño»
        text = "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c))
    # Знаки препинания и апострофы не важны: «dont» = «don't»
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(_OPTIONAL_PREFIX.get(lang, "^$"), "", text)


def is_correct(answer: str, w: sqlite3.Row) -> bool:
    return _normalize(answer, w["lang"]) == _normalize(w["word"], w["lang"])


def _meanings(translations: str) -> set[str]:
    """Значения перевода без пояснений в скобках: «ехать, ездить (на машине)» → {ехать, ездить}."""
    return {m.strip().lower() for m in re.sub(r"\([^)]*\)", "", translations).split(",") if m.strip()}


def is_synonym(answer: str, w: sqlite3.Row, tl: str = "ru") -> bool:
    """Ответ — другое слово из словаря с тем же переводом (film вместо movie): это не ошибка."""
    normalized = _normalize(answer, w["lang"])
    meanings = _meanings(translation(w, tl)[0])
    return any(other["id"] != w["id"] and _normalize(other["word"], w["lang"]) == normalized
               and meanings & _meanings(translation(other, tl)[0])
               for other in db.words_by_pos(w["lang"], w["pos"]))


def answer_text(w: sqlite3.Row) -> str:
    """Слово без необязательной части («sich», «to») — то, что пользователь должен ввести."""
    return re.sub(r"^(sich|to) ", "", w["word"])


def hint(w: sqlite3.Row, long: bool = False) -> str:
    word = answer_text(w)
    shown = max(1, len(word) // 2) if long else 1
    return word[:shown] + "…"


def quiz_question(w: sqlite3.Row, number: int, total: int, lang: str, tl: str = "ru") -> str:
    tr, _, flag = translation(w, tl)
    return t(lang, "question", n=number, total=total, tr=html.escape(tr), flag=flag,
             learn_flag=FLAGS[w["lang"]],
             pos=pos_name(lang, w["pos"]), hint=html.escape(hint(w)))
