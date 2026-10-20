"""Добавляет проверенные партии перевода в data/translations/<lang>_<tl>.csv.

    python3 tools/translate/merge.py es OUT_DIR/de_01.csv OUT_DIR/en_01.csv ...
Язык слов берётся из имени файла (de_01.csv → de). Повторный ключ заменяет старый перевод.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
tl, files = sys.argv[1], sys.argv[2:]
for f in files:
    lang = Path(f).name.split("_")[0]
    path = ROOT / "data" / "translations" / f"{lang}_{tl}.csv"
    rows = {}
    if path.exists():
        rows = {p[0]: p for p in csv.reader(path.open(encoding="utf-8"), delimiter=";") if len(p) == 3}
    new = [p for p in csv.reader(open(f, encoding="utf-8"), delimiter=";") if len(p) == 3]
    rows.update({p[0]: [x.strip() for x in p] for p in new})
    with path.open("w", encoding="utf-8", newline="") as out:
        csv.writer(out, delimiter=";", lineterminator="\n").writerows(rows.values())
    print(f"{f}: +{len(new)}, всего в {path.name}: {len(rows)}")
