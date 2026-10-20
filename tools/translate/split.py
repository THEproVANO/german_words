"""Нарезает словарь на партии для перевода: только слова, которых ещё нет в data/translations.

    python3 tools/translate/split.py de es OUT_DIR    # → OUT_DIR/de_01.tsv, ...
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
lang, tl, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
done_path = ROOT / "data" / "translations" / f"{lang}_{tl}.csv"
done = set()
if done_path.exists():
    done = {p[0] for p in csv.reader(done_path.open(encoding="utf-8"), delimiter=";") if p}
items = []
for r in csv.DictReader((ROOT / "data" / f"{lang}_words.csv").open(encoding="utf-8"), delimiter=";"):
    key = f"{lang}:{r['pos']}:{r['article']}:{r['word']}"
    if r["level"] == "BIZ":
        key = "BIZ:" + key
    if key in done:
        continue
    word = (r["article"] + " " if r["article"] else "") + r["word"]
    items.append("\t".join([key, word, r["pos"], r["translations"], r["example"], r["example_ru"]]))
out.mkdir(parents=True, exist_ok=True)
for n in range(0, len(items), 600):
    (out / f"{lang}_{n // 600 + 1:02d}.tsv").write_text("\n".join(items[n:n + 600]) + "\n", encoding="utf-8")
print(f"{len(items)} слов без перевода, партий: {(len(items) + 599) // 600}")
