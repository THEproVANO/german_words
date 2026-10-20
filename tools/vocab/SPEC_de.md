# German vocabulary batch spec (Telegram bot teaching German to Russian speakers)

Output: plain text file, one word per line, NO header, exactly 11 fields separated by `;`:
level;pos;article;word;plural;praesens;praeteritum;perfekt;translations;example;example_ru

- level: the level you were assigned (A1–C2, or BIZ for the "Business & IT" topic set).
- pos: one of noun, verb, adj, adv, prep, pron, conj, num, part, interj
- article: nouns only (required): der, die or das. Empty for non-nouns.
- word: nouns WITHOUT the article, capitalised (Vertrag). Verbs in the infinitive (reflexive with "sich ": sich bewerben).
- plural: nouns only (required): plural form WITHOUT article (Verträge); `-` if no plural in normal use (Personal), `pl` if plural-only (Kosten — then the word itself is in plural form). Empty for non-nouns.
- praesens: verbs only: 3rd person singular with "er ", ONLY if the stem changes (er fährt, er nimmt, er lädt herunter); otherwise empty.
- praeteritum: verbs only (required): Präteritum 3rd person singular (fuhr, lud herunter, bewarb sich).
- perfekt: verbs only (required): auxiliary + Partizip II (ist gefahren, hat heruntergeladen, hat sich beworben).
- translations: 1–3 Russian translations, comma-separated, most common first.
- example: one natural German sentence (5–12 words); the word form in the sentence is wrapped in **double asterisks** (exactly one bolded fragment). Never use `;` inside any field.
- example_ru: full natural Russian translation of the example, no asterisks.

Example lines:
B1;noun;der;Vertrag;Verträge;;;;договор, контракт;Wir haben den **Vertrag** gestern unterschrieben.;Мы вчера подписали договор.
B1;verb;;herunterladen;;er lädt herunter;lud herunter;hat heruntergeladen;скачивать;Ich **lade** die Datei gleich **herunter**.;Я сейчас скачаю файл.
B2;verb;;sich bewerben;;er bewirbt sich;bewarb sich;hat sich beworben;подавать заявку, откликаться (на вакансию);Sie **bewirbt sich** um eine Stelle.;Она откликается на вакансию.

Validate: awk -F';' 'NF!=11 || $10 !~ /\*\*.+\*\*/' FILE   (must print nothing); cut -d';' -f4 FILE | sort | uniq -d
Merge: python3 tools/vocab/add_words.py de FILE
