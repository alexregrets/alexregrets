import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, GROUP_ID, IMAP_EMAIL, IMAP_PASSWORD, IMAP_SERVER
from database import add_account, init_db
from handlers import router
from imap_poller import polling_loop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    await init_db()

    # Auto-register the default account from .env if provided
    if IMAP_EMAIL and IMAP_PASSWORD:
        try:
            await add_account(0, IMAP_EMAIL, IMAP_PASSWORD, IMAP_SERVER, GROUP_ID)
            logger.info("Default account %s registered from .env", IMAP_EMAIL)
        except Exception:
            pass  # Already registered

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    asyncio.create_task(polling_loop(bot))
    logger.info("Bot starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
