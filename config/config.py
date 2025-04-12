import dotenv, os

from dataclasses import dataclass


@dataclass
class TgBot:
    token: str


@dataclass
class PostgresDB:
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str


@dataclass
class Config:
    tg_bot: TgBot
    postgres_db: PostgresDB


def load_config() -> Config:

    dotenv.load_dotenv()

    return Config(
        tg_bot=TgBot(token=os.getenv("bot_token")),
        postgres_db=PostgresDB(
            os.getenv("DB_USER"),
            os.getenv("DB_PASS"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME")
            )
    )

config: Config = load_config()
