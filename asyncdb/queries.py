from typing import Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from asyncdb.models import ProductModel


async def get_products(db: AsyncSession, offset: int, limit: int):
    async with db as session:
        result = await session.execute(select(ProductModel).offset(offset).limit(limit))

        products = result.scalars().all()

        return products

async def search_product(db: AsyncSession, product_id: int) -> Optional[ProductModel]:
    async with db as session:
        result = await session.execute(
            select(ProductModel)
            .where(ProductModel.id == product_id)
        )
        return result.scalar_one_or_none()

async def delete_product(db: AsyncSession, product_id: int) -> bool:
    async with db as session:
        result = await session.execute(
            delete(ProductModel)
            .where(ProductModel.id == product_id)
        )
        await session.commit()
        return bool(result.rowcount)

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    updated = await queries.delete_product(db, product_id)

    if not updated:
        return Response(status_code=404)
    print("delete_product")
    return Response(status_code=204)
