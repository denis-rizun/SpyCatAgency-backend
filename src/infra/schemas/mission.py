from pydantic import BaseModel, Field
from typing import List, Optional


class TargetBase(BaseModel):
    name: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    notes: Optional[str] = None


class TargetCreate(TargetBase):
    pass


class TargetUpdate(BaseModel):
    id: int = Field(..., gt=0)
    notes: Optional[str] = None
    is_completed: Optional[bool] = None


class TargetResponse(TargetBase):
    id: int
    mission_id: int
    is_completed: bool

    class Config:
        from_attributes = True


class MissionBase(BaseModel):
    targets: List[TargetCreate] = Field(..., min_items=1, max_items=3)


class MissionCreate(MissionBase):
    pass


class MissionUpdate(BaseModel):
    targets: Optional[List[TargetUpdate]] = None


class MissionAssign(BaseModel):
    cat_id: int = Field(..., gt=0)


class MissionResponse(BaseModel):
    id: int
    cat_id: Optional[int]
    is_completed: bool
    targets: List[TargetResponse]

    class Config:
        from_attributes = True

