from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from asyncdb.models import ProductModel
from syncdb.models import ProductPayload


async def get_products(db: AsyncSession, offset: int, limit: int):
    async with db as session:
        result = await session.execute(
            select(ProductModel)
            .offset(offset)
            .limit(limit)
        )
        products = result.scalars().all()
        return products


async def get_product_by_id(db: AsyncSession, product_id: int):
    async with db as session:
        query = (
            select(ProductModel)
            .where(ProductModel.id == product_id)
        )
        result = await session.execute(query)

    return result.scalar_one_or_none()


async def update_product(db: AsyncSession, product_id: int, product_payload: ProductPayload) -> bool:
    async with db as session:
        query = (
            update(ProductModel)
            .values(**product_payload.dict())
            .where(ProductModel.id == product_id)
        )
        result = await session.execute(query)
        await session.commit()
        return bool(result.rowcount)


async def delete_product(db: AsyncSession, product_id: int) -> bool:
    async with db as session:
        query = (
            delete(ProductModel)
            .where(ProductModel.id == product_id)
        )
        result = await session.execute(query)
        await session.commit()
        return bool(result.rowcount)