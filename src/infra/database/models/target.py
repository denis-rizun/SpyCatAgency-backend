from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.infra.database.models.base import BaseModel


class Target(BaseModel):
    __tablename__ = "targets"

    mission_id = Column(Integer, ForeignKey("missions.id"))
    name = Column(String)
    country = Column(String)
    notes = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)

    mission = relationship(argument="Mission", back_populates="targets")
