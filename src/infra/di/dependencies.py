from typing import Annotated

from fastapi import Depends

from src.application.cat import CatService
from src.application.mission import MissionService
from src.infra.di.factory import get_cat_service, get_mission_service

CatServiceDI = Annotated[CatService, Depends(get_cat_service)]
MissionServiceDI = Annotated[MissionService, Depends(get_mission_service)]
