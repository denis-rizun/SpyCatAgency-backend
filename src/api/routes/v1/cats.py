from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.api.utils import APIUtils
from src.infra.di.dependencies import CatServiceDI
from src.infra.schemas.base import ResponseSchema
from src.infra.schemas.cat import CatResponse, CatCreate, CatUpdate

router = APIRouter(prefix="/cats", tags=["cats"])


@router.post(path="", response_model=ResponseSchema[CatResponse])
async def create_cat(data: CatCreate, service: CatServiceDI) -> ResponseSchema[CatResponse]:
    result = await service.create_cat(data)
    return APIUtils.unify(result, HTTP_201_CREATED)


@router.get(path="", response_model=ResponseSchema[list[CatResponse]])
async def get_all_cats(service: CatServiceDI) -> ResponseSchema[list[CatResponse]]:
    result = await service.get_all_cats()
    return APIUtils.unify(result, HTTP_200_OK)


@router.get(path="/{id}", response_model=ResponseSchema[CatResponse])
async def get_cat(id: int, service: CatServiceDI) -> ResponseSchema[CatResponse]:
    result = await service.get_cat(id)
    return APIUtils.unify(result, HTTP_200_OK)


@router.patch(path="/{id}", response_model=ResponseSchema[CatResponse])
async def update_cat(id: int, data: CatUpdate, service: CatServiceDI) -> ResponseSchema[CatResponse]:
    result = await service.update_cat(id, data)
    return APIUtils.unify(result, HTTP_200_OK)


@router.delete(path="/{id}", response_model=ResponseSchema[CatResponse])
async def delete_cat(id: int, service: CatServiceDI) -> ResponseSchema[None]:
    await service.delete_cat(id)
    return APIUtils.unify(None, HTTP_200_OK)
