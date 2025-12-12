from src.core.exceptions import (
    InvalidTargetsCountError,
    DatabaseNotFoundError,
    CatHasActiveMissionError,
    EntityCompletedError,
    EntityAssignedError
)
from src.domain.enums.founder import FindByEnum
from src.infra.database.repositories.manager import RepositoryManager
from src.infra.schemas.mission import MissionCreate, MissionResponse, MissionAssign, MissionUpdate


class MissionService:
    def __init__(self, repository: RepositoryManager) -> None:
        self.repository = repository

    async def create_mission(self, data: MissionCreate) -> MissionResponse:
        if not (1 <= len(data.targets) <= 3):
            raise InvalidTargetsCountError()

        mission = await self.repository.mission.create(is_flush=True)
        for target_data in data.targets:
            await self.repository.target.create(
                is_flush=True,
                mission_id=mission.id,
                name=target_data.name,
                country=target_data.country,
                notes=target_data.notes
            )

        mission = await self.repository.mission.get_with_relations({FindByEnum.ID: mission.id})
        response = MissionResponse.model_validate(mission)
        await self.repository.commit()
        return response

    async def get_mission(self, id: int) -> MissionResponse:
        mission = await self.repository.mission.get_with_relations({FindByEnum.ID: id})
        if not mission:
            raise DatabaseNotFoundError(msg=f"Mission(id={id}) not found")

        return MissionResponse.model_validate(mission)

    async def get_all_missions(self) -> list[MissionResponse]:
        missions = await self.repository.mission.get_with_relations({}, many=True)
        return [MissionResponse.model_validate(mission) for mission in missions]

    async def assign_cat(self, id: int, data: MissionAssign) -> MissionResponse:
        mission = await self.repository.mission.get({FindByEnum.ID: id})
        if not mission:
            raise DatabaseNotFoundError(msg=f"Mission(id={id}) not found")

        cat = await self.repository.cat.get({FindByEnum.ID: data.cat_id})
        if not cat:
            raise DatabaseNotFoundError(msg=f"Cat(id={data.cat_id}) not found")

        has_active_mission = await self.repository.cat.has_active_mission(cat.id)
        if has_active_mission:
            raise CatHasActiveMissionError()

        await self.repository.mission.assign_cat(mission.id, data.cat_id)
        await self.repository.commit()

        mission = await self.repository.mission.get_with_relations({FindByEnum.ID: id})
        return MissionResponse.model_validate(mission)

    async def update_targets(self, id: int, data: MissionUpdate) -> MissionResponse:
        mission = await self.repository.mission.get_with_relations({FindByEnum.ID: id})
        if not mission:
            raise DatabaseNotFoundError(msg=f"Mission(id={id}) not found")

        if mission.is_completed:
            raise EntityCompletedError(f"Mission(id={id}) has already completed")

        if not data.targets:
            return MissionResponse.model_validate(mission)

        for target_update in data.targets:
            target = next(
                (t for t in mission.targets if t.id == target_update.id),
                None
            )
            if not target:
                raise DatabaseNotFoundError(msg=f"Target(id={target_update.id}) not found")

            if target_update.notes is not None:
                if target.is_completed:
                    raise EntityCompletedError(msg=f"Target(id={target_update.id}) has already completed")
                if mission.is_completed:
                    raise EntityCompletedError(msg=f"Mission(id={id}) has already completed")
                target.notes = target_update.notes

            if target_update.is_completed is not None:
                target.is_completed = target_update.is_completed

        if all(t.is_completed for t in mission.targets):
            mission.is_completed = True

        await self.repository.commit()
        
        mission = await self.repository.mission.get_with_relations({FindByEnum.ID: id})
        return MissionResponse.model_validate(mission)

    async def delete_mission(self, mission_id: int) -> None:
        mission = await self.repository.mission.get({FindByEnum.ID: mission_id})
        if not mission:
            raise DatabaseNotFoundError(msg=f"Mission(id={mission_id}) not found")

        is_assigned = await self.repository.mission.is_assigned(mission_id)
        if is_assigned:
            raise EntityAssignedError(f"Mission(id={mission_id}) is assigned to a cat")

        await self.repository.mission.delete(mission_id)
        await self.repository.commit()

