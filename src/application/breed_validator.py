import httpx

from src.core.config import settings
from src.infra.database.repositories.manager import RepositoryManager


class BreedValidator:
    def __init__(self, repository: RepositoryManager) -> None:
        self.repository = repository
        self._breeds_cache = None

    async def validate_breed(self, breed: str) -> bool:
        breeds = await self._get_breeds()
        return breed.lower() in [b.lower() for b in breeds]

    async def _get_breeds(self) -> list[str]:
        if self._breeds_cache is not None:
            return self._breeds_cache

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(settings.BREED_VALIDATOR_API_URL)
                response.raise_for_status()
                breeds_data = response.json()
        except httpx.RequestError:
            return []

        self._breeds_cache = [breed.get("name", "") for breed in breeds_data]
        return self._breeds_cache
