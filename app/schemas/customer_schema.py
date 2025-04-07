from typing import List, Optional

from pydantic import BaseModel, EmailStr
from app.schemas.product_schema import ProductBase


class CustomerBase(BaseModel):
    name: str
    email: EmailStr


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class CustomerResponse(CustomerBase):
    id: Optional[int]
    favorites: Optional[List[ProductBase]] = []  

    class Config:
        from_attributes = True
