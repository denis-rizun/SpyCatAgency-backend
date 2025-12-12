from functools import cached_property

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repositories.cat import CatRepository
from src.infra.database.repositories.mission import MissionRepository
from src.infra.database.repositories.target import TargetRepository


class RepositoryFactory:
    _session: AsyncSession | None = None

    @cached_property
    def cat(self) -> CatRepository:
        return CatRepository(session=self._session)

    @cached_property
    def mission(self) -> MissionRepository:
        return MissionRepository(session=self._session)

    @cached_property
    def target(self) -> TargetRepository:
        return TargetRepository(session=self._session)
