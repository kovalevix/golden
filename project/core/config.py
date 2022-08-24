from functools import cache

from pydantic import BaseSettings


class TelegramBotSettings(BaseSettings):
    API_TOKEN: str

    class Config:
        env_prefix = "TB_"
        env_file = ".env"


@cache
def get_tb_settings() -> TelegramBotSettings:
    return TelegramBotSettings()
