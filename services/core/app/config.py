from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    SUPERUSER_EMAIL: str | None = None
    SUPERUSER_PASSWORD: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
