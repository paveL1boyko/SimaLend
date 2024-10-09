import asyncio
import random

import aiocache
from pyrogram import Client

from bot.config.headers import headers
from bot.config.logger import log
from bot.config.settings import config

from .api import CryptoBotApi
from .models import SessionData


class CryptoBot(CryptoBotApi):
    def __init__(self, tg_client: Client, additional_data: dict) -> None:
        super().__init__(tg_client)
        self.authorized = False
        self.sleep_time = config.BOT_SLEEP_TIME
        self.additional_data: SessionData = SessionData.model_validate(
            {k: v for d in additional_data for k, v in d.items()}
        )

    @aiocache.cached(ttl=config.LOGIN_CACHE_TTL)
    async def login_to_app(self, proxy: str | None) -> bool:
        tg_web_data = await self.get_tg_web_data(proxy=proxy)
        res = await self.login(json_body={"init_data": tg_web_data})
        self.http_client.headers[config.auth_header] = f'Bearer {res["token"]}'
        return True

    async def perform_tap(self):
        self.logger.info("Performing tap...")
        while self.user.energy > config.TAP_MIN_ENERGY:
            random_taps = random.randint(*config.TAP_RANDOM)
            money = random_taps * self.user.tap_coins
            self.user.energy -= money
            self.user.total_coins += money
            if self.user.energy < 0:
                break
            await self.sleeper(additional_delay=5)
            await self.taps(json_body={"quantity": random_taps})
            self.logger.info(
                f"Tapped {random_taps} times | Energy: {self.user.energy} | Balance: <y>{self.user.total_coins}</y>")
        self.logger.info(
            f"Energy not enaught | Energy: {self.user.energy} | Balance: <y>{self.user.total_coins}</y>")

    async def perform_booster(self):
        for _ in range(self.user.boosts):
            self.logger.info("Performing booster...")
            await self.get_booster()
            self.user.energy = self.user.max_energy
            await self.perform_tap()

    async def run(self, proxy: str | None) -> None:
        async with await self.create_http_client(proxy=proxy, headers=headers):
            while True:
                if self.errors >= config.ERRORS_BEFORE_STOP:
                    self.logger.error("Bot stopped (too many errors)")
                    break
                try:
                    if await self.login_to_app(proxy):
                        self.user = await self.get_user()

                    if config.SEND_TAPS:
                        await self.perform_tap()
                    if config.USE_BOOSTER:
                        await self.perform_booster()
                    sleep_time = random.randint(*config.BOT_SLEEP_TIME)
                    self.logger.info(f"🛌 Sleep time: {sleep_time // 60} minutes 🕒")
                    await asyncio.sleep(sleep_time)

                except RuntimeError as error:
                    raise error from error
                except Exception:
                    self.errors += 1
                    await self.login_to_app.cache.clear()
                    self.logger.exception("Unknown error")
                    await self.sleeper(additional_delay=self.errors * 8)


async def run_bot(tg_client: Client, proxy: str | None, additional_data: dict) -> None:
    try:
        await CryptoBot(tg_client=tg_client, additional_data=additional_data).run(proxy=proxy)
    except RuntimeError:
        log.bind(session_name=tg_client.name).exception("Session error")
