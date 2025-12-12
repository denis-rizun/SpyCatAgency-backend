from typing import Any, Generic, TypeVar

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.enums.founder import FindByEnum
from src.infra.database.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    MODEL: type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, filters: dict[FindByEnum, Any], many: bool = False) -> ModelType | list[ModelType] | None:
        stmt = select(self.MODEL)

        for field, value in filters.items():
            column = getattr(self.MODEL, field.value)
            if isinstance(value, (list, tuple, set)):
                stmt = stmt.where(column.in_(value))
            else:
                stmt = stmt.where(column == value)

        result = await self.session.execute(stmt)
        scalars = result.scalars()
        return scalars.all() if many else scalars.first()

    async def update_by(
        self,
        sorting_word: FindByEnum | None,
        value: Any | None,
        update_data: dict[str, Any],
        is_return: bool = False,
    ) -> ModelType | None:
        stmt = (
            update(self.MODEL)
            .where(getattr(self.MODEL, sorting_word.value) == value)
            .values(**update_data)
        )
        if is_return:
            stmt = stmt.returning(self.MODEL)

        result = await self.session.execute(stmt)
        if is_return:
            await self.session.flush()
            return result.scalar_one_or_none()

        return None

    async def create(self, is_flush: bool = False, **data) -> ModelType | None:
        model = self.MODEL(**data)
        self.session.add(model)
        if is_flush:
            await self.session.flush()
            return model

        return None

    async def delete(self, id: int) -> None:
        instance = await self.get({FindByEnum.ID: id})
        if instance:
            await self.session.delete(instance)
