from typing import Dict

from fastapi import FastAPI
from fastapi.openapi.models import Response

from mongodb.db import get_products, create_product, update_product, delete_product, get_product, get_average_price, \
    get_average_price_per_category

app = FastAPI()


@app.get("/products")
def read_products_api(category: str = None, sort_by: str = None):
    return get_products(category, sort_by)


@app.post("/products")
def create_product_api(product: Dict):
    created_product = create_product(product)
    print(created_product)

    return created_product


@app.put("/products/{product_id}")
def update_product_api(product_id: str, product: Dict):
    return update_product(product_id, product)


@app.delete("/products/{product_id}")
def delete_product_api(product_id: str):
    return delete_product(product_id)


@app.get("/products/{product_id}")
def read_product_api(product_id: str):
    product = get_product(product_id)

    if product:
        return product
    else:
        return Response(status_code=404, content={"message": "Product not found"})


@app.get("/average_price")
def average_price_api():
    return get_average_price_per_category()
