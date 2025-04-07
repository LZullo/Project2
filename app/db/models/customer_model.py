from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)

    favorites = relationship(
        "FavoriteProduct",
        back_populates="customer",
        cascade="all, delete-orphan",
        uselist=True,
    )
