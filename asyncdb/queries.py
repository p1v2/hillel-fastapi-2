from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from asyncdb.models import ProductModel


async def get_products(db: AsyncSession, offset: int, limit: int):
    async with db as session:
        result = await session.execute(select(ProductModel).offset(offset).limit(limit))

        products = result.scalars().all()

        return products
