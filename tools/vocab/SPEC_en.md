# English vocabulary batch spec (for a Telegram bot teaching English to Russian speakers)

Output: plain text file, one word per line, NO header, exactly 11 fields separated by `;`:
level;pos;article;word;plural;praesens;praeteritum;perfekt;translations;example;example_ru

- level: the CEFR level you were assigned (A2, B1 or B2).
- pos: one of noun, verb, adj, adv, prep, pron, conj, num, part, interj
- article: ALWAYS empty.
- word: base form, lowercase (except proper-like words). Verbs WITHOUT "to". Phrasal verbs allowed (e.g. "give up").
- plural: nouns only (required for nouns): plural form; `-` if uncountable/no plural; `pl` if plural-only (e.g. "jeans", "scissors"). Empty for non-nouns.
- praesens: ALWAYS empty.
- praeteritum: verbs only: past simple (e.g. "went"; variants with "/" like "learned/learnt"). Empty for non-verbs.
- perfekt: verbs only: past participle (e.g. "gone"). Empty for non-verbs.
- translations: 1–3 Russian translations, comma-separated, most common meaning first, specific enough that the learner can guess the English word.
- example: one natural English sentence (5–12 words) using the word; the word form in the sentence is wrapped in **double asterisks** (exactly one bolded fragment, e.g. "She **went** home early."). Never use `;` inside any field.
- example_ru: full natural Russian translation of the example, no asterisks.

Example lines:
A2;noun;;knife;knives;;;;нож;Can you pass me the **knife**, please?;Передай мне, пожалуйста, нож.
A2;noun;;furniture;-;;;;мебель;We bought new **furniture** for the living room.;Мы купили новую мебель для гостиной.
A2;verb;;choose;;;chose;chosen;выбирать;You can **choose** any colour you like.;Ты можешь выбрать любой цвет, который нравится.
B1;adj;;reliable;;;;;надёжный;He is a very **reliable** colleague.;Он очень надёжный коллега.

Rules:
- Words must genuinely match the level (Cambridge English Vocabulary Profile / Oxford 3000-5000 is a good guide).
- Do NOT include words already in data/en_words.csv (check the 4th field), and no duplicates within your file.
- Accuracy matters: correct irregular forms, correct plurals, correct Russian.
- After writing, validate with: awk -F';' 'NF!=11 || $10 !~ /\*\*.+\*\*/' FILE   (must print nothing) and check duplicates with: cut -d';' -f4 FILE | sort | uniq -d
- Write the file with a single heredoc or several appends; do not edit anything else in the repo.
