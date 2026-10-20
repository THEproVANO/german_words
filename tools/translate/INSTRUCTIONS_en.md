# Translate vocabulary cards into English

A Telegram bot teaches German and Spanish words. Cards currently have Russian translations; we add English ones for English-speaking users.

Input file (TSV, one card per line): key, word, part of speech, Russian translations (only a hint for the sense), example sentence (German or Spanish, target word in **bold**), Russian translation of the example (ignore it for translating).

Quality matters more than speed: the English must be accurate for the German/Spanish source, as a good bilingual dictionary would give it.

Output file: one line per input line, SAME ORDER, exactly 3 fields separated by `;`:
key;translations_en;example_en

- key: copied exactly from input.
- translations_en: translate FROM THE GERMAN/SPANISH WORD ITSELF, not from the Russian. Give 1–3 correct, natural English equivalents a native English speaker would use for this word in this sense (the sense shown by the example sentence). The Russian column is only a hint about which sense is meant; do not mirror Russian wording, Russian-specific clarifications or calques. Nouns without article unless needed; verbs as bare infinitive WITHOUT "to" (e.g. "go, leave"); add a short clarification in parentheses only when the English word is ambiguous.
- example_en: translate the ORIGINAL German/Spanish example sentence directly into natural, correct English (no asterisks, no bold). Do NOT translate the Russian sentence. Keep meaning, tense and register of the original.
- Never use `;` inside fields (use commas instead). No header line.

Work in chunks (e.g. 100 lines at a time, appending to the output file) so partial work survives interruptions; if the output file already has lines, continue after the last translated key.
When finished run: python3 tools/translate/check.py INPUT OUTPUT  — it must print OK. Fix anything it reports. Report only "OK" and the line count.
