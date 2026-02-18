import email
import re
from email.header import decode_header, make_header
from email.utils import parseaddr, parsedate_to_datetime


def parse_email(raw_bytes: bytes) -> dict:
    msg = email.message_from_bytes(raw_bytes)

    subject = _decode_header(msg.get("Subject", ""))
    sender_name, sender_email = parseaddr(msg.get("From", ""))
    sender_name = _decode_header(sender_name) if sender_name else ""
    message_id = msg.get("Message-ID", "")

    try:
        dt = parsedate_to_datetime(msg.get("Date", ""))
        date_formatted = dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        date_formatted = msg.get("Date", "")

    body = ""
    html_body = ""
    attachments = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition") or "")

            if "attachment" in disposition or part.get_filename():
                filename = part.get_filename()
                if filename:
                    filename = _decode_header(filename)
                else:
                    ext = content_type.split("/")[-1] if "/" in content_type else "bin"
                    filename = f"attachment.{ext}"
                data = part.get_payload(decode=True)
                if data:
                    attachments.append({"filename": filename, "data": data})

            elif content_type == "text/plain" and not body:
                payload = part.get_payload(decode=True)
                if payload:
                    body = _decode_payload(payload, part.get_content_charset())

            elif content_type == "text/html" and not html_body:
                payload = part.get_payload(decode=True)
                if payload:
                    html_body = _decode_payload(payload, part.get_content_charset())
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            if msg.get_content_type() == "text/html":
                html_body = _decode_payload(payload, msg.get_content_charset())
            else:
                body = _decode_payload(payload, msg.get_content_charset())

    if not body and html_body:
        body = _strip_html_tags(html_body)

    return {
        "message_id": message_id,
        "subject": subject,
        "sender": sender_email,
        "sender_name": sender_name,
        "date": date_formatted,
        "body": body.strip(),
        "attachments": attachments,
    }


def _decode_header(value: str) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def _decode_payload(payload: bytes, charset: str | None) -> str:
    charset = charset or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except (LookupError, UnicodeDecodeError):
        return payload.decode("utf-8", errors="replace")


def _strip_html_tags(html: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"&amp;", "&", text)
    text = re.sub(r"&lt;", "<", text)
    text = re.sub(r"&gt;", ">", text)
    return text.strip()
