from pathlib import Path
from typing import List, Optional

from pydantic import BaseSettings

BASE_PATH = Path(__file__).resolve().parent


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_db: str
    postgres_port: int
    database_min_connection_count: int = 5
    database_max_connection_count: int = 10

    redis_user: Optional[str]
    redis_password: Optional[str]
    redis_host: str
    redis_db: str
    redis_port: int

    dev: bool = True

    log_level: str = "INFO"

    project: str = "PROJECT"

    allowed_hosts: List[str] = ["localhost"]

    sentry_dsn: str
    environment: str

    @property
    def database_uri(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"  # noqa: E501

    @property
    def redis_uri(self):
        if self.redis_user and self.redis_password:
            return f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"  # noqa: E501
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    class Config:
        env_file = BASE_PATH.parent.parent.joinpath("dev.env")
        env_file_encoding = "utf-8"


settings = Settings()
