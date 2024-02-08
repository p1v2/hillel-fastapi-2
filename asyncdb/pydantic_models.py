from typing import Optional

from pydantic import BaseModel

from django_api.models import DjangoProduct


class ProductPayload(BaseModel):
    name: str
    price: float
    is_18_plus: Optional[bool] = False


class Product(ProductPayload):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class ProductWithExtraData(Product):
    extra_data: Optional[DjangoProduct]


class PaginatedProductResponse(BaseModel):
    results: list[Product]
    total: int
    offset: int
    limit: int

    class Config:
        orm_mode = True
        from_attributes = True
