import asyncio
import re

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import IMAP_SERVER
from database import (
    add_account,
    deactivate_account,
    get_accounts,
    get_aliases,
    get_lang,
    remove_alias,
    search_emails,
    set_alias,
    set_lang,
)
from imap_poller import test_imap_connection
from states import AddAlias, RegisterAccount, RemoveAlias, SearchEmails
from texts import t

router = Router()


async def _lang(user_id: int) -> str:
    return await get_lang(user_id)


# --- /start ---


@router.message(CommandStart())
async def cmd_start(message: Message):
    lang = await _lang(message.from_user.id)
    await message.answer(t("welcome", lang))


# --- /lang ---


@router.message(Command("lang"))
async def cmd_lang(message: Message):
    lang = await _lang(message.from_user.id)
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Русский", callback_data="lang:ru"),
                InlineKeyboardButton(text="English", callback_data="lang:en"),
            ]
        ]
    )
    await message.answer(t("lang_choose", lang), reply_markup=kb)


@router.callback_query(lambda c: c.data and c.data.startswith("lang:"))
async def cb_lang(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    await set_lang(callback.from_user.id, lang)
    await callback.message.edit_text(t("lang_set", lang))
    await callback.answer()


# --- /cancel ---


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    lang = await _lang(message.from_user.id)
    current = await state.get_state()
    if current is None:
        await message.answer(t("cancel_nothing", lang))
        return
    await state.clear()
    await message.answer(t("cancel_ok", lang))


# --- /register ---


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    lang = await _lang(message.from_user.id)
    await state.set_state(RegisterAccount.waiting_for_email)
    await message.answer(t("register_email", lang))


@router.message(RegisterAccount.waiting_for_email)
async def register_email(message: Message, state: FSMContext):
    lang = await _lang(message.from_user.id)
    email_addr = message.text.strip()
    if "@" not in email_addr:
        await message.answer(t("register_bad_email", lang))
        return
    await state.update_data(email=email_addr)
    await state.set_state(RegisterAccount.waiting_for_password)
    await message.answer(t("register_password", lang))


@router.message(RegisterAccount.waiting_for_password)
async def register_password(message: Message, state: FSMContext):
    lang = await _lang(message.from_user.id)
    password = message.text.strip()
    try:
        await message.delete()
    except Exception:
        pass
    await state.update_data(password=password)
    await state.set_state(RegisterAccount.waiting_for_server)
    await message.answer(t("register_server", lang, server=IMAP_SERVER))


@router.message(RegisterAccount.waiting_for_server)
async def register_server(message: Message, state: FSMContext):
    lang = await _lang(message.from_user.id)
    server = message.text.strip()
    if server == ".":
        server = IMAP_SERVER

    data = await state.get_data()
    await message.answer(t("register_testing", lang))

    loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(
            None, test_imap_connection, data["email"], data["password"], server
        )
    except Exception as e:
        await state.clear()
        await message.answer(t("register_fail", lang, error=str(e)))
        return

    try:
        await add_account(
            message.from_user.id,
            data["email"],
            data["password"],
            server,
            message.chat.id,
        )
    except Exception:
        await state.clear()
        await message.answer(t("register_duplicate", lang, email=data["email"]))
        return

    await state.clear()
    await message.answer(t("register_ok", lang, email=data["email"]))


# --- /accounts ---


@router.message(Command("accounts"))
async def cmd_accounts(message: Message):
    lang = await _lang(message.from_user.id)
    accounts = await get_accounts(message.from_user.id)
    if not accounts:
        await message.answer(t("accounts_empty", lang))
        return
    lines = []
    for acc in accounts:
        status = t("account_active", lang) if acc["is_active"] else t("account_stopped", lang)
        lines.append(t("account_line", lang, id=acc["id"], email=acc["email"], status=status))
    await message.answer(t("accounts_header", lang) + "\n".join(lines), parse_mode="HTML")


# --- /stop ---


@router.message(Command("stop"))
async def cmd_stop(message: Message):
    lang = await _lang(message.from_user.id)
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(t("stop_usage", lang), parse_mode="HTML")
        return
    try:
        account_id = int(args[1])
    except ValueError:
        await message.answer(t("stop_invalid_id", lang))
        return
    await deactivate_account(account_id)
    await message.answer(t("stop_ok", lang, id=account_id))


# --- /aliases ---


@router.message(Command("aliases"))
async def cmd_aliases(message: Message, state: FSMContext):
    lang = await _lang(message.from_user.id)
    parts = message.text.split(maxsplit=1)
    subcommand = parts[1].strip() if len(parts) > 1 else "list"

    if subcommand == "list":
        aliases_list = await get_aliases(message.from_user.id)
        if not aliases_list:
            await message.answer(t("aliases_empty", lang))
            return
        lines = [f"{a['email']} → {a['display_name']}" for a in aliases_list]
        await message.answer(
            t("aliases_header", lang) + "\n".join(lines), parse_mode="HTML"
        )

    elif subcommand == "add":
        await state.set_state(AddAlias.waiting_for_email)
        await message.answer(t("alias_enter_email", lang))

    elif subcommand == "remove":
        await state.set_state(RemoveAlias.waiting_for_email)
        await message.answer(t("alias_remove_email", lang))

    else:
        await message.answer(t("aliases_usage", lang))


@router.message(AddAlias.waiting_for_email)
async def alias_add_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text.strip())
    lang = await _lang(message.from_user.id)
    await state.set_state(AddAlias.waiting_for_name)
    await message.answer(t("alias_enter_name", lang))


@router.message(AddAlias.waiting_for_name)
async def alias_add_name(message: Message, state: FSMContext):
    data = await state.get_data()
    name = message.text.strip()
    await set_alias(message.from_user.id, data["email"], name)
    await state.clear()
    lang = await _lang(message.from_user.id)
    await message.answer(t("alias_set", lang, email=data["email"], name=name))


@router.message(RemoveAlias.waiting_for_email)
async def alias_remove_email(message: Message, state: FSMContext):
    await remove_alias(message.from_user.id, message.text.strip())
    await state.clear()
    lang = await _lang(message.from_user.id)
    await message.answer(t("alias_removed", lang))


# --- /search ---


@router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext):
    lang = await _lang(message.from_user.id)
    await state.set_state(SearchEmails.waiting_for_query)
    await message.answer(t("search_prompt", lang), parse_mode="HTML")


@router.message(SearchEmails.waiting_for_query)
async def search_query(message: Message, state: FSMContext):
    lang = await _lang(message.from_user.id)
    query = message.text.strip()
    await state.clear()

    sender = None
    date_from = None
    date_to = None

    sender_match = re.search(r"sender:(\S+)", query)
    from_match = re.search(r"from:(\S+)", query)
    to_match = re.search(r"to:(\S+)", query)

    if sender_match:
        sender = sender_match.group(1)
    elif not from_match and not to_match:
        sender = query

    if from_match:
        date_from = from_match.group(1)
    if to_match:
        date_to = to_match.group(1)

    accounts = await get_accounts(message.from_user.id, active_only=False)
    all_results = []
    for acc in accounts:
        results = await search_emails(
            acc["id"], sender=sender, date_from=date_from, date_to=date_to
        )
        all_results.extend(results)

    if not all_results:
        await message.answer(t("search_empty", lang))
        return

    lines = []
    for em in all_results[:20]:
        lines.append(f"{em['received_at']} | {em['sender']} | {em['subject']}")

    text = t("search_header", lang) + "\n".join(lines)
    if len(all_results) > 20:
        text += t("search_more", lang, count=len(all_results) - 20)

    if len(text) > 4096:
        text = text[:4090] + "\n..."

    await message.answer(text, parse_mode="HTML")
