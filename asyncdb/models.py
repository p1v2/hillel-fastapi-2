from sqlalchemy import Column, Integer, String, Float, Boolean

from asyncdb.db import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    price = Column(Float)
    is_18_plus = Column(Boolean, default=False)
