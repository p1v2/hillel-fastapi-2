from typing import Optional, Any

from pydantic import BaseModel, field_validator, model_validator


class ProductPayload(BaseModel):
    name: str
    price: float
    is_18_plus: Optional[bool] = False

    @field_validator("price")
    @classmethod
    def validate_price(cls, price):
        if price < 0:
            raise ValueError("Price must be greater than 0")
        return price

    @model_validator(mode="before")
    @classmethod
    def validate(cls, value: Any):
        if value["is_18_plus"] and value["price"] < 10:
            raise ValueError("Price must be greater than 10 for 18+ products")

        return value


class Product(ProductPayload):
    id: int


class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class UserInLogin(BaseModel):
    username: str
    password: str
