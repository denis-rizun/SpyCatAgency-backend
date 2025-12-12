from typing import List

from src.application.breed_validator import BreedValidator
from src.core.exceptions import InvalidBreedError, DatabaseNotFoundError, CatHasActiveMissionError
from src.domain.enums.founder import FindByEnum
from src.infra.database.repositories.manager import RepositoryManager
from src.infra.schemas.cat import CatCreate, CatResponse, CatUpdate


class CatService:
    def __init__(self, repository: RepositoryManager, breed_validator: BreedValidator) -> None:
        self.repository = repository
        self.breed_validator = breed_validator

    async def create_cat(self, cat_data: CatCreate) -> CatResponse:
        is_valid = await self.breed_validator.validate_breed(cat_data.breed)
        if not is_valid:
            raise InvalidBreedError()

        raw = cat_data.model_dump()
        cat = await self.repository.cat.create(**raw, is_flush=True)
        response = CatResponse.model_validate(cat)
        await self.repository.commit()
        return response

    async def get_cat(self, id: int) -> CatResponse:
        cat = await self.repository.cat.get({FindByEnum.ID: id})
        if not cat:
            raise DatabaseNotFoundError(msg=f'Cat(id={id}) not found')

        return CatResponse.model_validate(cat)

    async def get_all_cats(self) -> List[CatResponse]:
        cats = await self.repository.cat.get({}, many=True)
        return [CatResponse.model_validate(cat) for cat in cats]

    async def update_cat(self, id: int, cat_data: CatUpdate) -> CatResponse:
        cat = await self.repository.cat.get({FindByEnum.ID: id})
        if not cat:
            raise DatabaseNotFoundError(msg=f'Cat(id={id}) not found')

        cat.salary = cat_data.salary
        response = CatResponse.model_validate(cat)
        await self.repository.commit()
        return response

    async def delete_cat(self, id: int) -> None:
        cat = await self.repository.cat.get({FindByEnum.ID: id})
        if not cat:
            raise DatabaseNotFoundError(msg=f'Cat(id={id}) not found')

        has_active_mission = await self.repository.cat.has_active_mission(id)
        if has_active_mission:
            raise CatHasActiveMissionError()

        await self.repository.cat.delete(id)
        await self.repository.commit()
