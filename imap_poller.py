import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

from aiogram import Bot
from aiogram.types import BufferedInputFile
from imapclient import IMAPClient

from config import POLL_INTERVAL
from database import (
    add_processed_email,
    get_alias,
    get_all_active_accounts,
    get_lang,
    is_email_processed,
    update_last_uid,
)
from email_parser import parse_email
from texts import t

logger = logging.getLogger(__name__)
executor = ThreadPoolExecutor(max_workers=4)


def _imap_fetch_new(
    email_addr: str, password: str, imap_server: str, last_uid: int
) -> list[dict]:
    client = IMAPClient(imap_server, port=993, ssl=True, timeout=30)
    try:
        client.login(email_addr, password)
        client.select_folder("INBOX", readonly=True)

        if last_uid > 0:
            uids = client.search([f"UID {last_uid + 1}:*"])
            uids = [u for u in uids if u > last_uid]
        else:
            uids = client.search(["UNSEEN"])

        if not uids:
            return []

        raw_messages = client.fetch(uids, ["RFC822"])
        results = []
        for uid in sorted(uids):
            data = raw_messages.get(uid)
            if not data:
                continue
            raw_bytes = data[b"RFC822"]
            parsed = parse_email(raw_bytes)
            parsed["uid"] = uid
            results.append(parsed)
        return results
    except Exception:
        logger.exception("IMAP fetch failed for %s", email_addr)
        return []
    finally:
        try:
            client.logout()
        except Exception:
            pass


def test_imap_connection(email_addr: str, password: str, imap_server: str):
    client = IMAPClient(imap_server, port=993, ssl=True, timeout=15)
    try:
        client.login(email_addr, password)
        client.select_folder("INBOX", readonly=True)
    finally:
        try:
            client.logout()
        except Exception:
            pass


async def poll_account(bot: Bot, account: dict):
    loop = asyncio.get_running_loop()
    emails = await loop.run_in_executor(
        executor,
        _imap_fetch_new,
        account["email"],
        account["password"],
        account["imap_server"],
        account["last_uid"],
    )

    max_uid = account["last_uid"]
    lang = await get_lang(account["telegram_user_id"])

    for em in emails:
        if await is_email_processed(account["id"], em["uid"]):
            continue

        alias = await get_alias(account["telegram_user_id"], em["sender"])
        display_sender = alias if alias else em["sender"]

        await _forward_to_telegram(bot, account["target_chat_id"], display_sender, em, lang)

        await add_processed_email(
            account["id"],
            em["uid"],
            em.get("message_id", ""),
            em["subject"],
            em["sender"],
            em["date"],
        )

        if em["uid"] > max_uid:
            max_uid = em["uid"]

    if max_uid > account["last_uid"]:
        await update_last_uid(account["id"], max_uid)


async def _forward_to_telegram(
    bot: Bot, chat_id: int, display_sender: str, em: dict, lang: str
):
    body_preview = em["body"]
    if len(body_preview) > 3500:
        body_preview = body_preview[:3500] + "..."

    text = (
        t("email_from", lang, sender=_escape(display_sender))
        + "\n"
        + t("email_subject", lang, subject=_escape(em["subject"]))
        + "\n"
        + t("email_date", lang, date=_escape(em["date"]))
        + "\n\n"
        + _escape(body_preview)
    )

    if len(text) > 4096:
        text = text[:4090] + "\n..."

    await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")

    for att in em.get("attachments", []):
        size_mb = len(att["data"]) // (1024 * 1024)
        if len(att["data"]) > 50 * 1024 * 1024:
            await bot.send_message(
                chat_id=chat_id,
                text=t("email_attachment_too_large", lang, filename=_escape(att["filename"]), size=size_mb),
                parse_mode="HTML",
            )
            continue
        doc = BufferedInputFile(file=att["data"], filename=att["filename"])
        await bot.send_document(chat_id=chat_id, document=doc)


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


async def polling_loop(bot: Bot):
    logger.info("IMAP polling loop started (interval=%ds)", POLL_INTERVAL)
    while True:
        try:
            accounts = await get_all_active_accounts()
            for account in accounts:
                try:
                    await poll_account(bot, account)
                except Exception:
                    logger.exception("Error polling account %s", account["email"])
        except Exception:
            logger.exception("Error in polling loop")
        await asyncio.sleep(POLL_INTERVAL)
