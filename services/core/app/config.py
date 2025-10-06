from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str
    REDIS_URL: str
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    # Meilisearch
    MEILI_HOST: str = "http://meilisearch:7700"
    MEILI_MASTER_KEY: str = "meili_master_key"
    # MinIO / S3
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "bframe"
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    SUPERUSER_EMAIL: str | None = None
    SUPERUSER_PASSWORD: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
