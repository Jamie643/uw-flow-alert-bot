from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    UW_API_TOKEN: str = "YOUR_UW_BEARER_TOKEN"
    DISCORD_WEBHOOK_URL: str | None = None
    MIN_PREMIUM_THRESHOLD: float = 100_000.0
    POLL_INTERVAL_SECONDS: int = 15
    MAX_RETRIES: int = 3

    class Config:
        env_file = ".env"

settings = Settings()
