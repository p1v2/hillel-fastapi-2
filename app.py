import queries
from fastapi import FastAPI, Depends, Query, HTTPException
from rest_framework.response import Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from asyncdb.db import SessionLocal
from asyncdb.models import ProductModel
from asyncdb.pydantic_models import Product, ProductPayload, ProductWithExtraData, PaginatedProductResponse, \
    ProductUpdate
from asyncdb.queries import get_products, search_product, delete_product
from django_api.api import get_django_product_info

app = FastAPI()


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@app.get("/products",

         response_model=PaginatedProductResponse)
async def read_products(
        offset=Query(0),
        limit=Query(10),
        db: AsyncSession = Depends(get_db)
):
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
        session.add(db_product)
        await session.commit()
        await session.refresh(db_product)
        return db_product


# PUT Endpoint: Update an existing product by ID
@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product_payload: ProductPayload, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        db_product = await db.execute(select(ProductModel).filter(ProductModel.id == product_id))
        db_product = db_product.scalars().first()

        if db_product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        for key, value in product_payload.dict().items():
            setattr(db_product, key, value)
        print("update_product")
        await db.commit()
        await db.refresh(db_product)


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product_model = await queries.search_product(db, product_id)

    if not product_model:
        return Response(status_code=404)
    print("get_product")
    return Product.from_orm(product_model)


@app.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    updated = await queries.delete_product(db, product_id)

    if not updated:
        return Response(status_code=404)
    print("delete_product")
    return Response(status_code=204)
