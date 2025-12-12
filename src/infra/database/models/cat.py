from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from src.infra.database.models.base import BaseModel


class Cat(BaseModel):
    __tablename__ = "cats"

    name = Column(String)
    years_of_experience = Column(Integer)
    breed = Column(String)
    salary = Column(Float)

    missions = relationship(
        argument="Mission",
        back_populates="cat",
        cascade="all, delete-orphan"
    )

