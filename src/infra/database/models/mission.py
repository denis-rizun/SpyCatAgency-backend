from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.infra.database.models.base import BaseModel


class Mission(BaseModel):
    __tablename__ = "missions"

    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=True)
    is_completed = Column(Boolean, default=False)

    cat = relationship(argument="Cat", back_populates="missions")
    targets = relationship(
        argument="Target",
        back_populates="mission",
        cascade="all, delete-orphan"
    )
