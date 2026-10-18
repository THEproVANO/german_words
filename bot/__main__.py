import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from . import service, words
from .config import BOT_TOKEN
from .handlers import router


async def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    if not BOT_TOKEN:
        raise SystemExit("Не задан BOT_TOKEN. Укажите его в файле .env")

    logging.info("Загружено слов: %d", words.load_words())

    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    scheduler = asyncio.create_task(service.scheduler(bot))
    try:
        await dp.start_polling(bot)
    finally:
        scheduler.cancel()


if __name__ == "__main__":
    asyncio.run(main())
