# Перевод карточек на другой язык бота

1. `python3 tools/translate/split.py de es /tmp/tr/in` — партии слов без перевода.
2. Перевести каждую партию по `INSTRUCTIONS.md` (переводить с немецкого/английского оригинала,
   русский — только подсказка значения) → `/tmp/tr/out/de_01.csv`.
3. `python3 tools/translate/check.py /tmp/tr/in/de_01.tsv /tmp/tr/out/de_01.csv` — должно быть OK.
4. `python3 tools/translate/merge.py es /tmp/tr/out/de_01.csv` — в `data/translations/de_es.csv`.
