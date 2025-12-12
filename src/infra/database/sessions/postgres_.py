from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from src.core.config import settings


class PostgresSession:

    @classmethod
    def initialize(cls, echo: bool = False, expire: bool = True) -> async_sessionmaker:
        engine = cls._create_engine(echo=echo)
        return async_sessionmaker(bind=engine, expire_on_commit=expire)

    @staticmethod
    def _create_engine(echo: bool) -> AsyncEngine:
        return create_async_engine(
            url=settings.postgres_url,
            query_cache_size=1200,
            pool_size=20,
            max_overflow=200,
            future=True,
            echo=echo,
        )
