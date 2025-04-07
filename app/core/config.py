from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALLOWED_ORIGINS: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

settings.ALLOWED_ORIGINS = (
    ["*"]
    if settings.ALLOWED_ORIGINS == "*"
    else [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]
)
