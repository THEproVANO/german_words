# Telegram-бот для изучения немецких, английских и испанских слов (A1–C2)

- новые слова по расписанию (интервал, лимит в день и время рассылки настраиваются в профиле) + кнопка «Ещё слово»
- в 22:00 тест на 10 слов за день, пока он не пройден, новые слова не приходят
- по воскресеньям после теста дня — недельный тест на 40 слов
- кроме уровней A1–C2 есть тематический набор «💼 Работа, бизнес и IT» (уровень `BIZ` в словаре); слова, уже полученные
  в другом наборе, повторно не присылаются и считаются изученными
- после выбора уровня — вопрос: присылать слова только этого уровня или всех уровней ниже
- после теста дня — сводка прогресса и результат теста; после недельного — итоги недели, темп и прогноз
- профиль: изучаемый язык, уровень, прогресс, настройки рассылки, часовой пояс, язык бота, пауза, перезапуск (обновляет меню и кнопки), описание работы бота
- интерфейс на русском, английском, французском и испанском (тексты в `bot/i18n.py`); переводы слов пока только на русский

Словари: `data/de_words.csv`, `data/en_words.csv` и `data/es_words.csv` (разделитель `;`, можно редактировать в Excel).
Слова подгружаются в базу при каждом запуске бота. Чтобы добавить язык, достаточно файла
`data/<код>_words.csv` и кода в `LANGUAGES` (`bot/config.py`); кнопки уровней строятся по тем уровням,
где есть слова, а кнопка языка появляется, только когда для него есть словарь.

В английском словаре `article` и `praesens` пустые, у глаголов `praeteritum` / `perfekt` —
Past Simple / Past Participle (`go;;;went;gone`), `plural` — множественное число (`child;children`).

В испанском `article` — el или la, `plural` пустой (мн. ч. образуется по правилу, отмечаются только `-` и `pl`),
у глаголов `praesens` — форма yo, если она неправильная (`yo tengo`), `praeteritum` — претерит (yo),
`perfekt` — причастие: `tener;;yo tengo;tuve;tenido`.

| Поле | Пример |
|---|---|
| level | A1, A2, B1, B2, C1, C2, BIZ (тема «Работа, бизнес и IT») |
| pos | noun, verb, adj, adv, prep, pron, conj, num, part, interj |
| article | der / die / das (только для существительных) |
| word | Bahnhof, fahren, sich freuen |
| plural | Bahnhöfe (`-` — нет мн. ч., `pl` — только мн. ч.) |
| praesens | er fährt (только если корень меняется) |
| praeteritum / perfekt | fuhr / ist gefahren |
| translations | ехать, ездить |
| example | Morgen **fahre** ich nach Berlin. |
| example_ru | Завтра я еду в Берлин. |

## Установка на сервер (Ubuntu 24.04)

Под пользователем `bot`:

```bash
cd ~
git clone https://github.com/THEproVANO/german_words.git
cd german_words
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
nano .env          # вставить BOT_TOKEN, сохранить: Ctrl+O, Enter, Ctrl+X
```

Автозапуск:

```bash
sudo cp deploy/german-words-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now german-words-bot
```

## Команды бота

- `/start` — начать или вернуться в бота
- `/id` — показать свой Telegram ID
- `/quiz` — пробный тест дня прямо сейчас, `/quiz week` — пробный недельный тест
  (только для администраторов: их ID перечисляются через запятую в `ADMIN_IDS` в файле `.env`)

## Полезные команды

```bash
sudo systemctl status german-words-bot     # работает ли бот
sudo journalctl -u german-words-bot -f     # логи в реальном времени (выход: Ctrl+C)
~/german_words/deploy/update.sh            # обновить бота из GitHub
```
