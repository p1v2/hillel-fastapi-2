from starlette.responses import JSONResponse
from starlette import status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from asyncdb.models import ProductModel


async def get_products(db: AsyncSession, offset: int, limit: int):
    async with db as session:
        result = await session.execute(select(ProductModel).offset(offset).limit(limit))
        products = result.scalars().all()
        return products


async def search_product(db: AsyncSession, product_id: int) -> Optional[ProductModel]:
    async with db as session:
        result = await session.execute(select(ProductModel).where(ProductModel.id == product_id))
        return result.scalar_one_or_none()


async def delete_product(db: AsyncSession, product_id: int) -> Optional[bool]:
    async with db as session:
        product = await search_product(db, product_id)
        if product is None:
            return None
        result = await session.execute(delete(ProductModel).where(ProductModel.id == product_id))
        await session.commit()
        return bool(result.rowcount)


@app.delete("/products/{product_id}")
async def delete_product_endpoint(product_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_product(db, product_id)
    if deleted is None:
        return JSONResponse({"error": "Product not found"}, status_code=status.HTTP_404_NOT_FOUND)
    elif deleted:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return JSONResponse({"error": "Failed to delete product"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
