import sqlite3
from datetime import date, datetime, timezone

from .config import (ALL_LEVELS, DAY_END, DAY_START, DB_PATH, INTERVAL, LEVELS, TOPICS,
                     WORDS_PER_DAY)

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id             INTEGER PRIMARY KEY,
    lang           TEXT,
    level          TEXT,
    tz             TEXT NOT NULL,
    paused         INTEGER NOT NULL DEFAULT 0,
    blocked        INTEGER NOT NULL DEFAULT 0,
    last_slot_date TEXT,
    last_slot_idx  INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS words (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    lang         TEXT NOT NULL,
    key          TEXT NOT NULL UNIQUE,
    level        TEXT NOT NULL,
    pos          TEXT NOT NULL,
    article      TEXT NOT NULL DEFAULT '',
    word         TEXT NOT NULL,
    plural       TEXT NOT NULL DEFAULT '',
    praesens     TEXT NOT NULL DEFAULT '',
    praeteritum  TEXT NOT NULL DEFAULT '',
    perfekt      TEXT NOT NULL DEFAULT '',
    translations TEXT NOT NULL,
    example      TEXT NOT NULL,
    example_ru   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS user_words (
    user_id    INTEGER NOT NULL,
    word_id    INTEGER NOT NULL,
    sent_at    TEXT NOT NULL,
    study_date TEXT NOT NULL,
    PRIMARY KEY (user_id, word_id)
);
CREATE INDEX IF NOT EXISTS idx_user_words_date ON user_words (user_id, study_date);
CREATE TABLE IF NOT EXISTS quizzes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    kind       TEXT NOT NULL,          -- daily | weekly
    study_date TEXT NOT NULL,
    status     TEXT NOT NULL,          -- active | done
    created_at TEXT NOT NULL,
    UNIQUE (user_id, kind, study_date)
);
CREATE TABLE IF NOT EXISTS quiz_items (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id  INTEGER NOT NULL,
    word_id  INTEGER NOT NULL,
    position INTEGER NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    done     INTEGER NOT NULL DEFAULT 0
);
"""

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA journal_mode=WAL")
conn.executescript(SCHEMA)

# Колонки, добавленные после первого запуска: дописываем их в уже существующую базу
_user_columns = {r["name"] for r in conn.execute("PRAGMA table_info(users)")}
for _name, _default in (("interval_min", INTERVAL), ("words_per_day", WORDS_PER_DAY),
                        ("day_start", DAY_START), ("day_end", DAY_END)):
    if _name not in _user_columns:
        conn.execute(f"ALTER TABLE users ADD COLUMN {_name} INTEGER NOT NULL DEFAULT {_default}")
if "include_lower" not in _user_columns:
    conn.execute("ALTER TABLE users ADD COLUMN include_lower INTEGER NOT NULL DEFAULT 1")
if "ui_lang" not in _user_columns:
    conn.execute("ALTER TABLE users ADD COLUMN ui_lang TEXT NOT NULL DEFAULT 'ru'")
if "revealed" not in {r["name"] for r in conn.execute("PRAGMA table_info(quiz_items)")}:
    conn.execute("ALTER TABLE quiz_items ADD COLUMN revealed INTEGER NOT NULL DEFAULT 0")
# Французский интерфейс убран: у кого он был выбран, переключаем на английский
conn.execute("UPDATE users SET ui_lang = 'en' WHERE ui_lang = 'fr'")
conn.commit()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def levels_up_to(level: str) -> list[str]:
    return LEVELS[: LEVELS.index(level) + 1]


def user_levels(user: sqlite3.Row) -> list[str]:
    """Уровни, из которых пользователь получает слова: выбранный и, по желанию, все ниже.
    У тематического уровня уровней ниже нет."""
    if user["level"] in TOPICS or not user["include_lower"]:
        return [user["level"]]
    return levels_up_to(user["level"])


def _in(values: list) -> str:
    return ",".join("?" * len(values))


# --- users ---

def get_user(user_id: int) -> sqlite3.Row | None:
    return conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def create_user(user_id: int, tz: str) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO users (id, tz, created_at) VALUES (?, ?, ?)",
        (user_id, tz, now_utc()),
    )
    conn.commit()


def update_user(user_id: int, **fields) -> None:
    cols = ", ".join(f"{k} = ?" for k in fields)
    conn.execute(f"UPDATE users SET {cols} WHERE id = ?", (*fields.values(), user_id))
    conn.commit()


def active_users() -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT * FROM users WHERE lang IS NOT NULL AND level IS NOT NULL"
        " AND last_slot_date IS NOT NULL AND paused = 0 AND blocked = 0"
    ).fetchall()


# --- words ---

def upsert_words(rows: list[dict]) -> None:
    conn.executemany(
        """INSERT INTO words (lang, key, level, pos, article, word, plural, praesens,
                              praeteritum, perfekt, translations, example, example_ru)
           VALUES (:lang, :key, :level, :pos, :article, :word, :plural, :praesens,
                   :praeteritum, :perfekt, :translations, :example, :example_ru)
           ON CONFLICT (key) DO UPDATE SET
               level = excluded.level, pos = excluded.pos, article = excluded.article,
               word = excluded.word, plural = excluded.plural, praesens = excluded.praesens,
               praeteritum = excluded.praeteritum, perfekt = excluded.perfekt,
               translations = excluded.translations, example = excluded.example,
               example_ru = excluded.example_ru""",
        rows,
    )
    conn.commit()


def available_levels(lang: str) -> list[str]:
    """Уровни, для которых в словаре изучаемого языка есть слова."""
    present = {r[0] for r in conn.execute("SELECT DISTINCT level FROM words WHERE lang = ?", (lang,))}
    return [lvl for lvl in ALL_LEVELS if lvl in present]


def get_word(word_id: int) -> sqlite3.Row:
    return conn.execute("SELECT * FROM words WHERE id = ?", (word_id,)).fetchone()


def words_by_pos(lang: str, pos: str) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM words WHERE lang = ? AND pos = ?", (lang, pos)).fetchall()


def pick_new_word(user: sqlite3.Row) -> sqlite3.Row | None:
    """Случайное ещё не отправленное слово из уровней пользователя."""
    levels = user_levels(user)
    return conn.execute(
        f"""SELECT * FROM words
            WHERE lang = ? AND level IN ({_in(levels)})
              AND id NOT IN (SELECT word_id FROM user_words WHERE user_id = ?)
              -- То же слово из другого набора (A2 и «Бизнес и IT») второй раз не присылаем
              AND (lang, pos, word) NOT IN (
                  SELECT w.lang, w.pos, w.word FROM user_words uw JOIN words w ON w.id = uw.word_id
                  WHERE uw.user_id = ?)
            ORDER BY RANDOM() LIMIT 1""",
        (user["lang"], *levels, user["id"], user["id"]),
    ).fetchone()


def mark_sent(user_id: int, word_id: int, study_date: date) -> None:
    conn.execute(
        "INSERT OR IGNORE INTO user_words (user_id, word_id, sent_at, study_date)"
        " VALUES (?, ?, ?, ?)",
        (user_id, word_id, now_utc(), study_date.isoformat()),
    )
    conn.commit()


def progress(user: sqlite3.Row) -> tuple[int, int]:
    """(изучено, всего) для уровней пользователя."""
    levels = user_levels(user)
    total = conn.execute(
        f"SELECT COUNT(*) FROM words WHERE lang = ? AND level IN ({_in(levels)})",
        (user["lang"], *levels),
    ).fetchone()[0]
    # Изученным считается и слово, полученное в другом наборе (A2 и «Бизнес и IT»)
    learned = conn.execute(
        f"""SELECT COUNT(*) FROM words w
            WHERE w.lang = ? AND w.level IN ({_in(levels)})
              AND (w.lang, w.pos, w.word) IN (
                  SELECT w2.lang, w2.pos, w2.word FROM user_words uw
                  JOIN words w2 ON w2.id = uw.word_id WHERE uw.user_id = ?)""",
        (user["lang"], *levels, user["id"]),
    ).fetchone()[0]
    return learned, total


def words_for_dates(user_id: int, start: date, end: date) -> list[int]:
    rows = conn.execute(
        "SELECT word_id FROM user_words WHERE user_id = ? AND study_date BETWEEN ? AND ?",
        (user_id, start.isoformat(), end.isoformat()),
    ).fetchall()
    return [r[0] for r in rows]


# --- quizzes ---

def get_active_quiz(user_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM quizzes WHERE user_id = ? AND status = 'active' ORDER BY id LIMIT 1",
        (user_id,),
    ).fetchone()


def get_quiz(user_id: int, kind: str, study_date: date) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM quizzes WHERE user_id = ? AND kind = ? AND study_date = ?",
        (user_id, kind, study_date.isoformat()),
    ).fetchone()


def create_quiz(user_id: int, kind: str, study_date: date, word_ids: list[int]) -> int:
    status = "active" if word_ids else "done"
    cur = conn.execute(
        "INSERT INTO quizzes (user_id, kind, study_date, status, created_at)"
        " VALUES (?, ?, ?, ?, ?)",
        (user_id, kind, study_date.isoformat(), status, now_utc()),
    )
    quiz_id = cur.lastrowid
    conn.executemany(
        "INSERT INTO quiz_items (quiz_id, word_id, position) VALUES (?, ?, ?)",
        [(quiz_id, wid, i) for i, wid in enumerate(word_ids)],
    )
    conn.commit()
    return quiz_id


def current_item(quiz_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM quiz_items WHERE quiz_id = ? AND done = 0 ORDER BY position LIMIT 1",
        (quiz_id,),
    ).fetchone()


def quiz_counts(quiz_id: int) -> tuple[int, int]:
    """(сколько слов уже отвечено, всего слов)."""
    row = conn.execute(
        "SELECT SUM(done), COUNT(*) FROM quiz_items WHERE quiz_id = ?", (quiz_id,)
    ).fetchone()
    return row[0] or 0, row[1]


def set_attempts(item_id: int, attempts: int) -> None:
    conn.execute("UPDATE quiz_items SET attempts = ? WHERE id = ?", (attempts, item_id))
    conn.commit()


def mark_item_done(item_id: int) -> None:
    conn.execute("UPDATE quiz_items SET done = 1 WHERE id = ?", (item_id,))
    conn.commit()


def move_item_to_end(item_id: int, quiz_id: int) -> None:
    conn.execute(
        """UPDATE quiz_items SET attempts = 0, revealed = 1,
               position = (SELECT MAX(position) + 1 FROM quiz_items WHERE quiz_id = ?)
           WHERE id = ?""",
        (quiz_id, item_id),
    )
    conn.commit()


def quiz_stats(quiz_id: int) -> tuple[int, int, int]:
    """(с первой попытки, с ошибками, с подсмотренным ответом)."""
    row = conn.execute(
        """SELECT SUM(revealed = 0 AND attempts = 0), SUM(revealed = 0 AND attempts > 0),
                  SUM(revealed = 1)
           FROM quiz_items WHERE quiz_id = ?""",
        (quiz_id,),
    ).fetchone()
    return row[0] or 0, row[1] or 0, row[2] or 0


def finish_quiz(quiz_id: int) -> None:
    conn.execute("UPDATE quizzes SET status = 'done' WHERE id = ?", (quiz_id,))
    conn.commit()
