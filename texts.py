TEXTS = {
    "ru": {
        "welcome": (
            "<b>Email Forwarder Bot</b>\n\n"
            "Бот мониторит почту через IMAP и пересылает письма в Telegram.\n\n"
            "<b>Команды:</b>\n"
            "/register — Добавить почтовый аккаунт\n"
            "/accounts — Список аккаунтов\n"
            "/stop — Остановить мониторинг\n"
            "/aliases — Управление алиасами отправителей\n"
            "/search — Поиск по пересланным письмам\n"
            "/lang — Сменить язык\n"
            "/cancel — Отменить текущую операцию"
        ),
        "register_email": "Введите адрес электронной почты (например user@mail.ru):",
        "register_bad_email": "Не похоже на email. Попробуйте ещё раз:",
        "register_password": (
            "Введите пароль приложения.\n"
            "<i>Совет: создайте пароль приложения в настройках безопасности mail.ru.</i>\n"
            "(Сообщение с паролем будет удалено)"
        ),
        "register_server": "IMAP сервер? Отправьте <code>.</code> для значения по умолчанию ({server}), или введите свой:",
        "register_testing": "Проверяю подключение...",
        "register_fail": "Ошибка подключения: {error}\nПопробуйте /register заново.",
        "register_ok": "Аккаунт {email} зарегистрирован! Письма будут пересылаться в этот чат.",
        "register_duplicate": "Аккаунт {email} уже зарегистрирован.",
        "accounts_empty": "Нет зарегистрированных аккаунтов. Используйте /register.",
        "accounts_header": "<b>Ваши аккаунты:</b>\n",
        "account_line": "[{id}] {email} — {status}",
        "account_active": "активен",
        "account_stopped": "остановлен",
        "stop_usage": "Использование: /stop &lt;id аккаунта&gt;\nСмотрите ID через /accounts.",
        "stop_invalid_id": "Неверный ID аккаунта.",
        "stop_ok": "Аккаунт {id} остановлен.",
        "aliases_empty": "Нет алиасов. Используйте /aliases add или /aliases remove.",
        "aliases_header": "<b>Алиасы:</b>\n",
        "aliases_usage": "Использование: /aliases [list|add|remove]",
        "alias_enter_email": "Введите email отправителя для алиаса:",
        "alias_enter_name": "Введите отображаемое имя для этого отправителя:",
        "alias_set": "Алиас установлен: {email} → {name}",
        "alias_remove_email": "Введите email отправителя для удаления алиаса:",
        "alias_removed": "Алиас удалён.",
        "search_prompt": (
            "Введите запрос поиска:\n"
            "<code>sender:user@example.com from:2025-01-01 to:2025-01-31</code>\n\n"
            "Все поля необязательны. Или просто введите email отправителя."
        ),
        "search_empty": "Писем не найдено.",
        "search_header": "<b>Результаты поиска:</b>\n\n",
        "search_more": "\n\n...и ещё {count}",
        "cancel_nothing": "Нечего отменять.",
        "cancel_ok": "Отменено.",
        "lang_choose": "Выберите язык / Choose language:",
        "lang_set": "Язык установлен: Русский",
        "email_from": "<b>От:</b> {sender}",
        "email_subject": "<b>Тема:</b> {subject}",
        "email_date": "<b>Дата:</b> {date}",
        "email_attachment_too_large": "Вложение <b>{filename}</b> слишком большое ({size} МБ), пропущено.",
    },
    "en": {
        "welcome": (
            "<b>Email Forwarder Bot</b>\n\n"
            "Bot monitors email via IMAP and forwards messages to Telegram.\n\n"
            "<b>Commands:</b>\n"
            "/register — Add an email account\n"
            "/accounts — List your accounts\n"
            "/stop — Stop monitoring an account\n"
            "/aliases — Manage sender aliases\n"
            "/search — Search forwarded emails\n"
            "/lang — Change language\n"
            "/cancel — Cancel current operation"
        ),
        "register_email": "Enter your email address (e.g. user@mail.ru):",
        "register_bad_email": "That doesn't look like an email. Try again:",
        "register_password": (
            "Enter your app password.\n"
            "<i>Tip: Generate an app password in your mail.ru security settings.</i>\n"
            "(The password message will be deleted)"
        ),
        "register_server": "IMAP server? Send <code>.</code> for default ({server}), or enter a custom one:",
        "register_testing": "Testing connection...",
        "register_fail": "Connection failed: {error}\nTry /register again.",
        "register_ok": "Account {email} registered! Emails will be forwarded to this chat.",
        "register_duplicate": "Account {email} is already registered.",
        "accounts_empty": "No accounts registered. Use /register.",
        "accounts_header": "<b>Your accounts:</b>\n",
        "account_line": "[{id}] {email} — {status}",
        "account_active": "active",
        "account_stopped": "stopped",
        "stop_usage": "Usage: /stop &lt;account_id&gt;\nSee IDs via /accounts.",
        "stop_invalid_id": "Invalid account ID.",
        "stop_ok": "Account {id} stopped.",
        "aliases_empty": "No aliases. Use /aliases add or /aliases remove.",
        "aliases_header": "<b>Aliases:</b>\n",
        "aliases_usage": "Usage: /aliases [list|add|remove]",
        "alias_enter_email": "Enter sender email to alias:",
        "alias_enter_name": "Enter display name for this sender:",
        "alias_set": "Alias set: {email} → {name}",
        "alias_remove_email": "Enter sender email to remove alias for:",
        "alias_removed": "Alias removed.",
        "search_prompt": (
            "Enter search query:\n"
            "<code>sender:user@example.com from:2025-01-01 to:2025-01-31</code>\n\n"
            "All fields are optional. Or just enter a sender email."
        ),
        "search_empty": "No emails found.",
        "search_header": "<b>Search results:</b>\n\n",
        "search_more": "\n\n...and {count} more",
        "cancel_nothing": "Nothing to cancel.",
        "cancel_ok": "Cancelled.",
        "lang_choose": "Выберите язык / Choose language:",
        "lang_set": "Language set: English",
        "email_from": "<b>From:</b> {sender}",
        "email_subject": "<b>Subject:</b> {subject}",
        "email_date": "<b>Date:</b> {date}",
        "email_attachment_too_large": "Attachment <b>{filename}</b> is too large ({size} MB), skipped.",
    },
}

DEFAULT_LANG = "ru"


def t(key: str, lang: str = DEFAULT_LANG, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS[DEFAULT_LANG]).get(key, TEXTS[DEFAULT_LANG].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text
