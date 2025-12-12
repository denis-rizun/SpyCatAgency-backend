from sqlalchemy import func, Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
