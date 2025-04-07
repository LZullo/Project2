from typing import List, Optional, Union

from pydantic import BaseModel, field_validator

from app.schemas.product_schema import ProductBase


class FavoriteProductBase(BaseModel):
    pass


class FavoriteProductCreate(FavoriteProductBase):
    product_ids: Union[int, List[int]]

    @field_validator("product_ids", mode="before")
    @classmethod
    def ensure_list(cls, v):
        return v if isinstance(v, list) else [v]


class FavoriteListResponse(BaseModel):
    customer_id: int
    favorites: List[ProductBase]

    class Config:
        from_attributes = True


class AddFavoriteRequest(BaseModel):
    product_id: int
    title: str
    image_url: str
    price: float
    review: Optional[str] = None