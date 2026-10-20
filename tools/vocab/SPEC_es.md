# Spanish vocabulary batch spec (Telegram bot teaching Spanish to Russian speakers)

Output: plain text file, one word per line, NO header, exactly 11 fields separated by `;`:
level;pos;article;word;plural;praesens;praeteritum;perfekt;translations;example;example_ru

- level: the CEFR level you were assigned (A1, A2, B1, B2, C1 or C2, or BIZ for the "Work, business & IT" topic set). Use Instituto Cervantes "Plan curricular" / common Spanish frequency lists as the guide.
- pos: one of noun, verb, adj, adv, prep, pron, conj, num, part, interj
- article: nouns only (required): `el` or `la` (the singular definite article as actually used: "el agua", "el mapa", "la mano"). Spanish has only these two; for common-gender nouns (estudiante, turista) pick `el`. Empty for non-nouns.
- word: nouns WITHOUT the article, lowercase (la casa -> `casa`). Adjectives in masculine singular (rojo). Verbs in the infinitive (reflexive with -se: levantarse).
- plural: normally EMPTY (Spanish plurals are regular, the learner doesn't memorise them). Only two special values: `-` if the noun has no plural in normal use (salud, gente, sed), `pl` if it is used only in plural (gafas, vacaciones — then put the word itself in plural form). Empty for non-nouns.
- praesens: verbs only: the "yo" present form WITH "yo " prefix, ONLY if irregular or stem-changing in the present (`yo tengo`, `yo quiero`, `yo conozco`, `yo voy`); empty for regular verbs (hablar, comer, vivir). For verbs with no yo-irregularity but stem change in other persons (e.g. jugar -> yo juego) still fill it. For reflexive verbs include the pronoun: `yo me acuesto`.
- praeteritum: verbs only (required): pretérito indefinido, yo form (hablé, tuve, fui, me levanté).
- perfekt: verbs only (required): participio (hablado, tenido, hecho, escrito).
- translations: 1–3 Russian translations, comma-separated, most common first, specific enough to guess the Spanish word.
- example: one natural Spanish sentence (5–12 words) using the word; the word form in the sentence is wrapped in **double asterisks** (exactly one bolded fragment, e.g. "Mañana **voy** a Madrid."). Use correct accents and ¿ ¡. Never use `;` inside any field.
- example_ru: full natural Russian translation of the example, no asterisks.

Example lines:
A1;noun;el;libro;;;;;книга;Este **libro** es muy interesante.;Эта книга очень интересная.
A1;noun;la;mano;;;;;рука, кисть;Lávate las **manos** antes de comer.;Помой руки перед едой.
A1;noun;el;estudiante;;;;;студент;Mi hermana es **estudiante** de medicina.;Моя сестра — студентка медицинского.
A1;noun;la;gente;-;;;;люди;Hay mucha **gente** en la calle.;На улице много людей.
A1;verb;;tener;;yo tengo;tuve;tenido;иметь;**Tengo** dos hermanos.;У меня два брата.
A1;verb;;hablar;;;hablé;hablado;говорить;¿**Hablas** español?;Ты говоришь по-испански?
A1;verb;;levantarse;;;me levanté;levantado;вставать;Me **levanto** a las siete.;Я встаю в семь.
B1;adj;;fiable;;;;;надёжный;Es una fuente muy **fiable**.;Это очень надёжный источник.

Rules:
- Words must genuinely match the level.
- Do NOT include words already in data/es_words.csv if it exists (check the 4th field), and no duplicates within your file.
- Accuracy matters: correct gender/article, irregular verb forms, accents, correct Russian.
- After writing, validate: awk -F';' 'NF!=11 || $10 !~ /\*\*.+\*\*/' FILE   (must print nothing); duplicates: cut -d';' -f4 FILE | sort | uniq -d
- Work ONLY in your own output file (and, if needed, a private subfolder named after your output file); do not touch other files.
