from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    APP_NAME: str = "BOMBA API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: str = "sqlite:///products.db"

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug_value(cls, value):
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "debug"}:
                return True
            if normalized in {"0", "false", "no", "off", "release"}:
                return False
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()