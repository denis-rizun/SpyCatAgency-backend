from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.infra.database.models import Mission
from src.infra.database.repositories.base import BaseRepository


class MissionRepository(BaseRepository[Mission]):
    MODEL = Mission

    async def get_with_relations(self, filters: dict, many: bool = False) -> Mission | None | list[Mission]:
        stmt = select(self.MODEL).options(
            selectinload(Mission.targets),
            selectinload(Mission.cat)
        )

        for field, value in filters.items():
            column = getattr(self.MODEL, field.value)
            if isinstance(value, (list, tuple, set)):
                stmt = stmt.where(column.in_(value))
            else:
                stmt = stmt.where(column == value)

        result = await self.session.execute(stmt)
        scalars = result.scalars()
        return scalars.all() if many else scalars.first()

    async def is_assigned(self, id: int) -> bool:
        query = (
            select(Mission)
            .where(Mission.id == id)
            .where(Mission.cat_id != None)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def assign_cat(self, id: int, cat_id: int) -> None:
        query = (
            update(Mission)
            .where(Mission.id == id)
            .values(cat_id=cat_id)
        )
        await self.session.execute(query)
