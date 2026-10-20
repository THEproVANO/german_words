# Translate vocabulary cards into Spanish

A Telegram bot teaches German and English words. Cards currently have Russian translations; we add Spanish ones for Spanish-speaking users.

Input file (TSV, one card per line): key, word, part of speech, Russian translations (only a hint for the sense), example sentence (German or English, target word in **bold**), Russian translation of the example (ignore it for translating).

Quality matters more than speed: the Spanish must be accurate for the German/English source, as a good bilingual dictionary would give it.

Output file: one line per input line, SAME ORDER, exactly 3 fields separated by `;`:
key;translations_es;example_es

- key: copied exactly from input.
- translations_es: translate FROM THE GERMAN/ENGLISH WORD ITSELF, not from the Russian. Give 1–3 correct, natural Spanish equivalents a native Spanish speaker would use for this word in this sense (the sense shown by the example sentence). The Russian column is only a hint about which sense is meant; do not mirror Russian wording, Russian-specific clarifications or calques. Nouns without article unless needed; verbs in infinitive; add a short clarification in parentheses only when the Spanish word is ambiguous.
- example_es: translate the ORIGINAL German/English example sentence directly into natural, correct Spanish (no asterisks, no bold). Do NOT translate the Russian sentence. Keep meaning, tense and register of the original.
- Never use `;` inside fields (use commas instead). No header line.

Work in chunks (e.g. 100 lines at a time, appending to the output file) so partial work survives interruptions; if the output file already has lines, continue after the last translated key.
When finished run: python3 tools/translate/check.py INPUT OUTPUT  — it must print OK. Fix anything it reports. Report only "OK" and the line count.
