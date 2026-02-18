import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
GROUP_ID: int = int(os.environ["GROUP_ID"])
IMAP_SERVER: str = os.getenv("IMAP_SERVER", "imap.mail.ru")
POLL_INTERVAL: int = int(os.getenv("POLL_INTERVAL", "60"))
IMAP_EMAIL: str | None = os.getenv("IMAP_EMAIL")
IMAP_PASSWORD: str | None = os.getenv("IMAP_PASSWORD")
