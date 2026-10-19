"""Проверяет партию слов и дописывает новые строки в словарь, пропуская дубли."""
import csv, sys
DICT = str(__import__("pathlib").Path(__file__).resolve().parents[2] / "data" / "en_words.csv")
FIELDS = ["level","pos","article","word","plural","praesens","praeteritum","perfekt","translations","example","example_ru"]
POS = {"noun","verb","adj","adv","prep","pron","conj","num","part","interj"}
def key(r): return (r["pos"], r["word"].lower())
with open(DICT, encoding="utf-8") as f:
    existing = list(csv.DictReader(f, delimiter=";"))
seen = {key(r) for r in existing}
new, errors, dupes = [], [], []
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.strip(): continue
            parts = line.split(";")
            if len(parts) != 11: errors.append(f"{path}:{n} полей {len(parts)}: {line[:60]}"); continue
            r = dict(zip(FIELDS, [p.strip() for p in parts]))
            e = []
            if r["level"] not in ("A1","A2","B1","B2","C1","C2"): e.append("level")
            if r["pos"] not in POS: e.append("pos")
            if r["pos"] == "noun" and (r["article"] or not r["plural"]): e.append("noun fields")
            if r["pos"] != "noun" and (r["article"] or r["plural"]): e.append("article/plural on non-noun")
            if r["pos"] == "verb" and not (r["praeteritum"] and r["perfekt"]): e.append("verb forms")
            if "**" not in r["example"] or r["example"].count("**") % 2: e.append("bold")
            if not (r["translations"] and r["example_ru"]): e.append("empty")
            if e: errors.append(f"{path}:{n} {e}: {line[:60]}"); continue
            if key(r) in seen: dupes.append(r["word"]); continue
            seen.add(key(r)); new.append(r)
if errors:
    print("ОШИБКИ:"); print("\n".join(errors)); sys.exit(1)
with open(DICT, "a", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, FIELDS, delimiter=";", lineterminator="\n"); w.writerows(new)
from collections import Counter
total = existing + new
print(f"добавлено {len(new)}, дубли пропущены ({len(dupes)}): {', '.join(dupes)}")
print("по уровням:", dict(Counter(r["level"] for r in total)), "всего", len(total))
