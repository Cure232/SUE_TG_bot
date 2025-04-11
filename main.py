import asyncio

from aiogram import Bot, Dispatcher

from config.config import config
from config.menu import set_main_menu
from handlers.user_handlers import router


async def main() -> None:
    bot = Bot(token=config.tg_bot.token)

    dp = Dispatcher()
    dp.include_router(router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    