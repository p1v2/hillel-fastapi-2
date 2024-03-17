from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from asyncdb.models import ProductModel


async def get_products(db: AsyncSession, offset: int, limit: int):
    async with db as session:
        result = await session.execute(select(ProductModel).offset(offset).limit(limit))

        products = result.scalars().all()

        return products

async def get_product_by_id(product_id: int, db: AsyncSession):
    async with db as session:
        result = await session.execute(select(ProductModel).where(ProductModel.id == product_id))
        row = result.scalars().all()

        if row is None:
            raise HTTPException(status_code=404, detail="Product not found")

        return row


async def update_product_by_id(product_id: int, db: AsyncSession):
    async with db as session:
        await session.execute(update(ProductModel).where(ProductModel.id == product_id).values(
                name=ProductModel.name,
                price=ProductModel.price,
                is_18_plus=ProductModel.is_18_plus,
            )
        )

async def delete_product_by_id(product_id: int, db: AsyncSession):
    async with db as session:
        await session.execute(delete(ProductModel).where(ProductModel.id == product_id))
