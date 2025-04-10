import dotenv, os

from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config() -> Config:

    dotenv.load_dotenv()

    return Config(
        tg_bot=TgBot(token=os.getenv("bot_token"))
    )