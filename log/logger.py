import logging
from aiogram import Bot

from config.config import config

LOG_CHAT_ID = -1002538493689

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(funcName)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


async def log_to_chat(bot: Bot, text: str):
    try:
        await bot.send_message(chat_id=LOG_CHAT_ID, text=text,
                               message_thread_id=config.tg_bot.chat_thread_id)
    except Exception as e:
        logger.error(f"Ошибка отправки лога в чат: {e}")
        print(f"Ошибка отправки лога в чат: {e}")


async def log_registration_start(bot: Bot, username: str, user_id: int):
    text = (
        f"🟡 Начата регистрация!\n"
        f"Пользователь: @{username} ({user_id})"
    )
    await log_to_chat(bot, text)


async def log_registration_end(bot: Bot, username: str, user_id: int, data: dict):
    text = (
        f"🟢 Регистрация завершена!\n"
        f"Пользователь: @{username} ({user_id})\n"
        f"Группа: {data.get('group_num')}\n"
        f"Игра: {data.get('game')}"
    )
    await log_to_chat(bot, text)
