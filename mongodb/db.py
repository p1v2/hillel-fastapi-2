from typing import Any, Dict, Optional

from bson import ObjectId
from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017/"

client = MongoClient(MONGO_URL)

db = client["products_database"]

collection = db.products


def create_product(product: Dict):
    result = collection.insert_one(product)
    return {**product, "_id": str(result.inserted_id)}


def get_products(category: Optional[str] = None, sort_by: Optional[str] = None):
    if category:
        items = collection.find({"category": category})
    else:
        items = collection.find()

    if sort_by:
        items = items.sort(sort_by)

    return [
        {**item, "_id": str(item["_id"])} for item in items
    ]


def update_product(product_id: str, product: Dict):
    collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product}
    )

    return {**product, "_id": product_id}


def delete_product(product_id: str):
    collection.delete_one({"_id": ObjectId(product_id)})


def get_product(product_id: str):
    item = collection.find_one({"_id": product_id})
    return {**item, "_id": str(item["_id"])} if item else None


def get_average_price():
    pipeline = [
        {
            "$group": {
                "_id": None,
                "average_price": {"$avg": "$price"}
            }
        }
    ]

    avg_result = list(collection.aggregate(pipeline))

    return avg_result


def get_average_price_per_category():
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "average_price": {"$avg": "$price"}
            }
        }
    ]

    avg_result = list(collection.aggregate(pipeline))

    return avg_result
