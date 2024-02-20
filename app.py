import asyncio
from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from asyncdb.db import SessionLocal
from asyncdb.models import ProductModel
from asyncdb.pydantic_models import Product, ProductPayload, ProductWithExtraData, PaginatedProductResponse
from asyncdb.queries import get_products
from django_api.api import get_django_product_info

app = FastAPI()


async def get_db() -> AsyncSession: # type: ignore
    async with SessionLocal() as session:
        yield session


@app.get("/products",

         response_model=PaginatedProductResponse)
async def read_products(
        offset=Query(0),
        limit=Query(10),
        db: AsyncSession = Depends(get_db),
        product_id=Query(None)
):
    
    if product_id:
        async with db as session:
            query = await session.execute(
                select(ProductModel).filter(ProductModel.id == product_id)
            )
            product = query.scalars().first()
            return PaginatedProductResponse(
            results=[product,],
            total=1,
            offset=0,
            limit=1
        )
    
    else:
        products_models = await get_products(db, offset, limit)

        count_query = select([func.count()]).select_from(ProductModel)
        total = (await db.execute(count_query)).scalar()

        products = [Product.from_orm(product) for product in products_models]

        return PaginatedProductResponse(
            results=products,
            total=total,
            offset=offset,
            limit=limit
        )
            

    # start = datetime.now()
    # django_products = await asyncio.gather(
    #     *[get_django_product_info(product.name) for product in products]
    # )
    # end = datetime.now()
    #
    # print(f"Time taken: {(end - start)}")
    #
    # products_with_extra_data = []
    # for product, django_product in zip(products, django_products):
    #     products_with_extra_data.append(
    #         ProductWithExtraData(
    #             **product.dict(),
    #             extra_data=django_product
    #         )
    #     )
    #
    # return products_with_extra_data


@app.post("/products", response_model=Product)
async def create_product(product_payload: ProductPayload, db: AsyncSession = Depends(get_db)):
    async with db as session:
        db_product = ProductModel(**product_payload.dict())
        # print(product_payload.dict())
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product



@app.put('/products', response_model=Product)
async def update_product(product:Product, db: AsyncSession = Depends(get_db)):
    async with db as session:
        product_ob = await session.get(ProductModel, product.dict()['id'])
        # print(product_ob.id, product_ob.price)
        if product_ob:
            for key, val in product.dict().items():
                setattr(product_ob, key, val)
            await session.commit()
            await session.refresh(product_ob)
            return product_ob
        else:
            return Product(id=-1, name="Does not exist", price=0)



@app.delete('/products/{product_id}')
async def delete_product(product_id:int, db: AsyncSession = Depends(get_db)):
    async with db as session:
        product_ob = await session.get(ProductModel, product_id)
        if product_ob:
            await session.delete(product_ob)
            await session.commit()
            return Product(id=0, name="Product deleted", price=0)
        else:
            return Product(id=-1, name="Does not exist", price=0)