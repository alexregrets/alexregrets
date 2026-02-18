# CLAUDE.md

This file provides guidance to AI assistants (Claude and others) working in this repository.

---

## Repository Overview

**Repository**: alexregrets/alexregrets
**Project**: uni_mail_bot — Telegram bot that monitors university email (mail.ru) via IMAP and forwards messages with attachments to Telegram chats/groups.

**Stack**: Python 3.12, aiogram 3, imapclient, aiosqlite, python-dotenv

---

## Project Structure

```
├── bot.py              # Entry point: Bot + Dispatcher + IMAP background task
├── handlers.py         # Telegram command handlers (/start, /register, /aliases, /search, etc.)
├── states.py           # aiogram FSM StatesGroup definitions
├── imap_poller.py      # IMAP polling loop (threaded) + Telegram forwarding
├── email_parser.py     # Email parsing: headers, body, attachments, encodings
├── database.py         # SQLite schema + async CRUD via aiosqlite
├── config.py           # Loads .env, exposes settings as module-level constants
├── texts.py            # i18n message strings (ru/en)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Ignores .env, *.db, __pycache__/, venv/
└── CLAUDE.md           # This file
```

---

## General Conventions for AI Assistants

### Reading Code Before Changing It

- Always read a file before editing it.
- Never propose changes based on assumptions about file contents.
- When exploring an unfamiliar area, trace call sites and usages before modifying signatures or interfaces.

### Making Changes

- Keep changes minimal and focused on the stated task.
- Do not refactor, add comments, or clean up code outside the scope of the request.
- Prefer editing existing files over creating new ones.
- Delete code that is no longer used; do not leave dead code behind.
- Do not add error handling for situations that cannot occur.

### Security

- Never introduce command injection, SQL injection, XSS, or other OWASP Top 10 vulnerabilities.
- Do not commit secrets, credentials, API keys, or `.env` files.
- Validate input only at system boundaries (user input, external APIs); trust internal framework guarantees.

### Git Workflow

- Always develop on the designated feature branch; never push directly to `main` or `master` without explicit permission.
- Write clear, descriptive commit messages that explain *why* the change was made, not just *what* changed.
- Stage specific files rather than using `git add -A` or `git add .` to avoid accidentally including sensitive files.
- Do not amend commits that have already been pushed unless explicitly instructed.
- Push with: `git push -u origin <branch-name>`

### Commit Message Format

```
<short imperative summary (50 chars max)>

<optional body explaining motivation and context>
```

---

## Development Workflow

### Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your BOT_TOKEN, IMAP credentials, GROUP_ID
```

### Running the Application

```bash
python bot.py
```

---

## Environment Variables

| Variable        | Description                              | Required |
| --------------- | ---------------------------------------- | -------- |
| `BOT_TOKEN`     | Telegram bot token from @BotFather       | Yes      |
| `GROUP_ID`      | Default Telegram chat ID for forwarding  | Yes      |
| `IMAP_SERVER`   | IMAP server hostname (default: imap.mail.ru) | No   |
| `IMAP_EMAIL`    | Default email for auto-registration      | No       |
| `IMAP_PASSWORD` | App password for default email           | No       |
| `POLL_INTERVAL` | Seconds between IMAP polls (default: 60) | No       |

---

## Key Decisions and Context

- **UID tracking over UNSEEN flags**: UNSEEN flags are unreliable when email is also read via webmail. UID high-water mark (`last_uid`) per account is deterministic.
- **Thread executor for IMAP**: `imapclient` is synchronous. All IMAP calls run in `ThreadPoolExecutor` to avoid blocking the asyncio event loop.
- **No IDLE mode**: IDLE requires persistent connections and complex renewal. Polling every 60s is simpler and sufficient for this use case.
- **Plaintext passwords in SQLite**: Known tradeoff for a personal bot. The `.db` and `.env` files are gitignored.
- **Per-account target_chat_id**: Each registered account forwards to the chat where `/register` was called. The `.env` `GROUP_ID` is used only for the auto-registered default account.
- **i18n via texts.py**: Simple dict-based translation (ru/en). Language preference stored per user in SQLite.
