import json

from aiocache import Cache, cached
from pyrogram import Client

from bot.helper.decorators import error_handler, handle_request

from .base_api import BaseBotApi
from .models import UserProfile


class CryptoBotApi(BaseBotApi):
    def __init__(self, tg_client: Client):
        super().__init__(tg_client)

    @error_handler()
    @handle_request("/api/login")
    async def login(self, *, response_json: dict, json_body: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request("/api/v1/user", method="GET")
    async def get_user(self, *, response_json: dict) -> UserProfile:
        return UserProfile(**response_json)

    @error_handler()
    @handle_request("/api/v1/taps")
    async def taps(self, *, response_json: dict, json_body: dict) -> dict:
        return

    @error_handler()
    @handle_request("/api/v1/taps/booster")
    async def get_booster(self, *, response_json: dict) -> dict:
        return response_json

    @cached(ttl=2 * 60 * 60, cache=Cache.MEMORY)
    @error_handler()
    @handle_request(
        "https://raw.githubusercontent.com/testingstrategy/musk_daily/main/daily.json",
        method="GET",
        full_url=True,
    )
    async def get_helper(self, *, response_json: str) -> dict:
        return json.loads(response_json)
