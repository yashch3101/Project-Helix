from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Project Helix API"
    app_version: str = "1.0.0"
    app_env: str = "development"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    gemini_api_key: str


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()