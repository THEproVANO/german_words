# Telegram-бот для изучения немецких слов (A1–B2)

- новые слова по расписанию (интервал, лимит в день и время рассылки настраиваются в профиле) + кнопка «Ещё слово»
- в 22:00 тест на 10 слов за день, пока он не пройден, новые слова не приходят
- по воскресеньям после теста дня — недельный тест на 40 слов
- профиль: уровень, прогресс, настройки рассылки, часовой пояс, пауза, описание работы бота

Словарь: `data/de_words.csv` (разделитель `;`, можно редактировать в Excel).
Слова подгружаются в базу при каждом запуске бота.

| Поле | Пример |
|---|---|
| level | A1, A2, B1, B2 |
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

## Полезные команды

```bash
sudo systemctl status german-words-bot     # работает ли бот
sudo journalctl -u german-words-bot -f     # логи в реальном времени (выход: Ctrl+C)
~/german_words/deploy/update.sh            # обновить бота из GitHub
```
