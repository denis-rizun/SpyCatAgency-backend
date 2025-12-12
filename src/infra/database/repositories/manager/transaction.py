from sqlalchemy.ext.asyncio import AsyncSession


class TransactionManager:
    _session: AsyncSession | None = None

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except Exception as e:
            await self.rollback()
            raise e

    async def flush(self) -> None:
        await self._session.flush()

    async def rollback(self) -> None:
        await self._session.rollback()
