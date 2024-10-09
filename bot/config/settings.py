from pydantic_settings import BaseSettings, SettingsConfigDict

logo = """
Simalend
"""


class BaseBotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str

    SLEEP_BETWEEN_START: list[int] = [10, 20]
    SESSION_AC_DELAY: int = 10
    ERRORS_BEFORE_STOP: int = 5
    USE_PROXY_FROM_FILE: bool = False
    ADD_LOCAL_MACHINE_AS_IP: bool = False

    RANDOM_SLEEP_TIME: int = 8

    BOT_SLEEP_TIME: list[int] = [3000, 3500]

    LOGIN_CACHE_TTL: int = 3600
    REF_ID: str = "refId1092379081"
    auth_header: str = "Authorization"
    base_url: str = "https://simatap.ru"
    bot_name: str = "SimaTapBot"
    bot_app: str = "SimaTap"


class Settings(BaseBotSettings):
    SEND_TAPS: bool = True
    TAP_MIN_ENERGY: int = 200
    USE_BOOSTER: bool = True
    TAP_RANDOM: list = [20, 40]
    EXECUTE_TASKS: bool = True


config = Settings()
