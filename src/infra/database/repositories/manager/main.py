from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repositories.manager.factory import RepositoryFactory
from src.infra.database.repositories.manager.transaction import TransactionManager


class RepositoryManager(RepositoryFactory, TransactionManager):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
