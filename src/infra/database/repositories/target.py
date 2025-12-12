from src.infra.database.models import Target
from src.infra.database.repositories.base import BaseRepository


class TargetRepository(BaseRepository[Target]):
    MODEL = Target

