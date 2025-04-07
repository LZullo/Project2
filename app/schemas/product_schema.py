from typing import Optional

from pydantic import BaseModel, HttpUrl
from pydantic.config import ConfigDict


class ProductBase(BaseModel):
    """Schema base para representar um produto da API mockada."""

    id: int
    title: str
    image_url: HttpUrl
    price: float
    review: Optional[str] = None

    class Config:
        from_attributes = True 
