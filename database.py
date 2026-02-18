import aiosqlite

DB_PATH = "bot.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("PRAGMA foreign_keys = ON")
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_user_id INTEGER PRIMARY KEY,
                lang TEXT NOT NULL DEFAULT 'ru'
            );

            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_user_id INTEGER NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                imap_server TEXT NOT NULL DEFAULT 'imap.mail.ru',
                target_chat_id INTEGER NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                last_uid INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                UNIQUE(telegram_user_id, email)
            );

            CREATE TABLE IF NOT EXISTS processed_emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL,
                uid INTEGER NOT NULL,
                message_id TEXT,
                subject TEXT,
                sender TEXT,
                received_at TEXT,
                forwarded_at TEXT NOT NULL DEFAULT (datetime('now')),
                UNIQUE(account_id, uid),
                FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_user_id INTEGER NOT NULL,
                email TEXT NOT NULL,
                display_name TEXT NOT NULL,
                UNIQUE(telegram_user_id, email)
            );
        """)


async def get_lang(telegram_user_id: int) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT lang FROM users WHERE telegram_user_id = ?",
            (telegram_user_id,),
        )
        row = await cur.fetchone()
        return row["lang"] if row else "ru"


async def set_lang(telegram_user_id: int, lang: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO users (telegram_user_id, lang) VALUES (?, ?) "
            "ON CONFLICT(telegram_user_id) DO UPDATE SET lang = excluded.lang",
            (telegram_user_id, lang),
        )
        await db.commit()


async def add_account(
    telegram_user_id: int,
    email: str,
    password: str,
    imap_server: str,
    target_chat_id: int,
) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO accounts (telegram_user_id, email, password, imap_server, target_chat_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (telegram_user_id, email, password, imap_server, target_chat_id),
        )
        await db.commit()
        return cur.lastrowid


async def get_accounts(telegram_user_id: int, active_only: bool = False) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if active_only:
            cur = await db.execute(
                "SELECT * FROM accounts WHERE telegram_user_id = ? AND is_active = 1",
                (telegram_user_id,),
            )
        else:
            cur = await db.execute(
                "SELECT * FROM accounts WHERE telegram_user_id = ?",
                (telegram_user_id,),
            )
        return [dict(row) for row in await cur.fetchall()]


async def get_all_active_accounts() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM accounts WHERE is_active = 1")
        return [dict(row) for row in await cur.fetchall()]


async def deactivate_account(account_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE accounts SET is_active = 0 WHERE id = ?", (account_id,)
        )
        await db.commit()


async def update_last_uid(account_id: int, uid: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE accounts SET last_uid = ? WHERE id = ?", (uid, account_id)
        )
        await db.commit()


async def add_processed_email(
    account_id: int,
    uid: int,
    message_id: str,
    subject: str,
    sender: str,
    received_at: str,
):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO processed_emails "
            "(account_id, uid, message_id, subject, sender, received_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (account_id, uid, message_id, subject, sender, received_at),
        )
        await db.commit()


async def is_email_processed(account_id: int, uid: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT 1 FROM processed_emails WHERE account_id = ? AND uid = ?",
            (account_id, uid),
        )
        return await cur.fetchone() is not None


async def search_emails(
    account_id: int,
    sender: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        query = "SELECT * FROM processed_emails WHERE account_id = ?"
        params: list = [account_id]
        if sender:
            query += " AND sender LIKE ?"
            params.append(f"%{sender}%")
        if date_from:
            query += " AND received_at >= ?"
            params.append(date_from)
        if date_to:
            query += " AND received_at <= ?"
            params.append(date_to + " 23:59:59")
        query += " ORDER BY received_at DESC LIMIT 50"
        cur = await db.execute(query, params)
        return [dict(row) for row in await cur.fetchall()]


async def set_alias(telegram_user_id: int, email: str, display_name: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO aliases (telegram_user_id, email, display_name) VALUES (?, ?, ?) "
            "ON CONFLICT(telegram_user_id, email) DO UPDATE SET display_name = excluded.display_name",
            (telegram_user_id, email, display_name),
        )
        await db.commit()


async def remove_alias(telegram_user_id: int, email: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM aliases WHERE telegram_user_id = ? AND email = ?",
            (telegram_user_id, email),
        )
        await db.commit()


async def get_aliases(telegram_user_id: int) -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM aliases WHERE telegram_user_id = ?",
            (telegram_user_id,),
        )
        return [dict(row) for row in await cur.fetchall()]


async def get_alias(telegram_user_id: int, email: str) -> str | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT display_name FROM aliases WHERE telegram_user_id = ? AND email = ?",
            (telegram_user_id, email),
        )
        row = await cur.fetchone()
        return row["display_name"] if row else None
