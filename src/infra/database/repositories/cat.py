from sqlalchemy import select

from src.infra.database.models import Cat, Mission
from src.infra.database.repositories.base import BaseRepository


class CatRepository(BaseRepository[Cat]):
    MODEL = Cat

    async def has_active_mission(self, id: int) -> bool:
        query = (
            select(Mission)
            .where(Mission.cat_id == id)
            .where(Mission.is_completed == False)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
