from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.breed_validator import BreedValidator
from src.application.cat import CatService
from src.application.mission import MissionService
from src.infra.database.repositories.manager import RepositoryManager
from src.infra.database.sessions.postgres_ import PostgresSession

_postgres_session_factory = PostgresSession.initialize()


async def get_session() -> AsyncGenerator:
    session = _postgres_session_factory()
    try:
        yield session
    finally:
        await session.close()


async def get_repository(session: AsyncSession = Depends(get_session)) -> AsyncGenerator:
    yield RepositoryManager(session)


async def get_cat_service(repository: RepositoryManager = Depends(get_repository)) -> AsyncGenerator:
    breed_validator = BreedValidator(repository)
    yield CatService(repository, breed_validator)


async def get_mission_service(repository: RepositoryManager = Depends(get_repository)) -> AsyncGenerator:
    yield MissionService(repository)
