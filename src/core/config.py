from functools import cached_property
from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    model_config = ConfigDict(env_file=BASE_DIR / ".env")  # noqa

    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]

    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_HOST: str = ""
    INNER_POSTGRES_PORT: int = 0
    OUTER_POSTGRES_PORT: int = 0

    BREED_VALIDATOR_API_URL: str = ""

    @cached_property
    def postgres_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.INNER_POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    @cached_property
    def alembic_postgres_url(self) -> str:
        return (
            f"postgresql://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.INNER_POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )


settings = Settings()
