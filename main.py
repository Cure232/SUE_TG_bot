import asyncio

from aiogram import Bot, Dispatcher

from config.config import config
from config.menu import set_main_menu
from handlers.solo_handlers import router as solo_router
from handlers.team_handlers import router as team_router
from handlers.common_handlers import router as commom_router


async def main() -> None:
    bot = Bot(token=config.tg_bot.token)

    dp = Dispatcher()
    dp.include_router(commom_router)
    dp.include_router(solo_router)
    dp.include_router(team_router)

    await set_main_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    