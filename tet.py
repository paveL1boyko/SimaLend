import asyncio

from pydantic_settings import BaseSettings, SettingsConfigDict
from pyrogram import Client

from bot.core.base_api import BaseBotApi


class BaseBotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str


settings = BaseBotSettings()

app = Client("russ", api_id=settings.API_ID, api_hash=settings.API_HASH, workdir="sessions/")

target_first_name = "Telegram"


async def main():
    aa = BaseBotApi(app)

    await aa.join_and_archive_channel("https://t.me/cityholder/game?startapp=1092379081")


asyncio.run(main())
