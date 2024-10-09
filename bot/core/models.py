from pydantic import BaseModel, Field


class SessionData(BaseModel):
    user_agent: str = Field(validation_alias="User-Agent")
    proxy: str | None = None




class UserProfile(BaseModel):
    level: int
    energy: int
    max_energy: int
    tap_coins: int
    total_coins: int
    week_total_coins: int
    previous_week_total_coins: int
    boosts: int
    max_boosts: int
    energy_ps: int
    is_subscribed: bool
    is_morse_completed: bool
