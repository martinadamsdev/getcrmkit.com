import functools

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # Database
    database_url: str = "postgresql+asyncpg://crmkit:crmkit@localhost:15432/crmkit"
    database_url_sync: str = "postgresql://crmkit:crmkit@localhost:15432/crmkit"

    # Redis
    redis_url: str = "redis://localhost:16379/0"

    # Worker
    worker_concurrency: int = 10

    # JWT
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 30
    jwt_refresh_token_short_expire_hours: int = 24

    # Password
    password_min_length: int = 8

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"


@functools.lru_cache
def get_settings() -> Settings:
    return Settings()
