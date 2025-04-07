from sqlalchemy import (Column, Float, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from app.db.database import Base


class FavoriteProduct(Base):
    __tablename__ = "favorite_products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    review = Column(String, nullable=True)

    customer_id = Column(
        Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("customer_id", "product_id", name="uq_customer_product"),
    )

    customer = relationship("Customer", back_populates="favorites")

