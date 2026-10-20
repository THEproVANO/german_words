"""Проверяет партию слов и дописывает новые строки в data/<lang>_words.csv, пропуская дубли.

    python3 tools/vocab/add_words.py en batch1.csv batch2.csv

Слова тематического уровня BIZ («Бизнес и IT») проверяются на дубли только внутри своей темы:
тематический набор может повторять слова из A1–C2.
"""
import csv
import sys
from collections import Counter
from pathlib import Path

FIELDS = ["level", "pos", "article", "word", "plural", "praesens", "praeteritum", "perfekt",
          "translations", "example", "example_ru"]
LEVELS = ("A1", "A2", "B1", "B2", "C1", "C2")
TOPICS = ("BIZ",)
POS = {"noun", "verb", "adj", "adv", "prep", "pron", "conj", "num", "part", "interj"}
ARTICLES = {"de": ("der", "die", "das"), "en": ("",), "es": ("el", "la")}


def key(r):
    return (r["level"] if r["level"] in TOPICS else "", r["pos"], r["word"].lower())


def check(lang, r):
    e = []
    if r["level"] not in LEVELS + TOPICS: e.append("level")
    if r["pos"] not in POS: e.append("pos")
    if r["pos"] == "noun":
        if r["article"] not in ARTICLES[lang]: e.append("article")
        if lang == "es" and r["plural"] not in ("", "-", "pl"): e.append("plural (es: пусто, - или pl)")
        if lang != "es" and not r["plural"]: e.append("plural")
    elif r["article"] or r["plural"]:
        e.append("article/plural on non-noun")
    if r["pos"] == "verb" and not (r["praeteritum"] and r["perfekt"]): e.append("verb forms")
    if r["pos"] != "verb" and (r["praesens"] or r["praeteritum"] or r["perfekt"]): e.append("verb forms on non-verb")
    if lang == "es" and r["praesens"] and not r["praesens"].startswith(("yo ", "me ")): e.append("praesens")
    if "**" not in r["example"] or r["example"].count("**") % 2: e.append("bold")
    if not (r["word"] and r["translations"] and r["example_ru"]): e.append("empty")
    return e


def main():
    lang, paths = sys.argv[1], sys.argv[2:]
    path = Path(__file__).resolve().parents[2] / "data" / f"{lang}_words.csv"
    if not path.exists():
        path.write_text(";".join(FIELDS) + "\n", encoding="utf-8")
    with path.open(encoding="utf-8") as f:
        existing = list(csv.DictReader(f, delimiter=";"))
    seen = {key(r) for r in existing}
    new, errors, dupes = [], [], []
    for batch in paths:
        with open(batch, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                line = line.rstrip("\n")
                if not line.strip() or line.startswith("level;"):
                    continue
                parts = line.split(";")
                if len(parts) != len(FIELDS):
                    errors.append(f"{batch}:{n} полей {len(parts)}: {line[:60]}")
                    continue
                r = dict(zip(FIELDS, (p.strip() for p in parts)))
                if e := check(lang, r):
                    errors.append(f"{batch}:{n} {e}: {line[:60]}")
                elif key(r) in seen:
                    dupes.append(r["word"])
                else:
                    seen.add(key(r))
                    new.append(r)
    if errors:
        print("ОШИБКИ:", *errors, sep="\n")
        sys.exit(1)
    with path.open("a", encoding="utf-8", newline="") as f:
        csv.DictWriter(f, FIELDS, delimiter=";", lineterminator="\n").writerows(new)
    print(f"добавлено {len(new)}, дубли пропущены {len(dupes)}")
    print("по уровням:", dict(Counter(r["level"] for r in existing + new)), "всего", len(existing + new))


if __name__ == "__main__":
    main()
