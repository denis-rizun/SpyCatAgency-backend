from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from src.api.utils import APIUtils
from src.infra.di.dependencies import MissionServiceDI
from src.infra.schemas.base import ResponseSchema
from src.infra.schemas.mission import MissionResponse, MissionCreate, MissionUpdate, MissionAssign

router = APIRouter(prefix="/missions", tags=["missions"])


@router.post(path="", response_model=ResponseSchema[MissionResponse])
async def create_mission(
    data: MissionCreate,
    service: MissionServiceDI
) -> ResponseSchema[MissionResponse]:
    result = await service.create_mission(data)
    return APIUtils.unify(result, HTTP_201_CREATED)


@router.get(path="", response_model=ResponseSchema[list[MissionResponse]])
async def get_all_missions(service: MissionServiceDI) -> ResponseSchema[list[MissionResponse]]:
    result = await service.get_all_missions()
    return APIUtils.unify(result, HTTP_200_OK)


@router.get(path="/{id}", response_model=ResponseSchema[MissionResponse])
async def get_mission(
    id: int,
    service: MissionServiceDI
) -> ResponseSchema[MissionResponse]:
    result = await service.get_mission(id)
    return APIUtils.unify(result, HTTP_200_OK)


@router.post(path="/{id}/assign", response_model=ResponseSchema[MissionResponse])
async def assign_cat(
    id: int,
    assign_data: MissionAssign,
    service: MissionServiceDI
) -> ResponseSchema[MissionResponse]:
    result = await service.assign_cat(id, assign_data)
    return APIUtils.unify(result, HTTP_200_OK)


@router.patch(path="/{id}/targets", response_model=ResponseSchema[MissionResponse])
async def update_targets(
    id: int,
    mission_data: MissionUpdate,
    service: MissionServiceDI
):
    result = await service.update_targets(id, mission_data)
    return APIUtils.unify(result, HTTP_200_OK)



@router.delete(path="/{id}", response_model=ResponseSchema[None])
async def delete_mission(id: int, service: MissionServiceDI) -> ResponseSchema[None]:
    await service.delete_mission(id)
    return APIUtils.unify(None, HTTP_200_OK)


