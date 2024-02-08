from datetime import datetime, time
from typing import Optional

import aiohttp

from django_api.models import DjangoProduct


async def get_django_product_info(product_name: str) -> Optional[DjangoProduct]:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://localhost:8001/api/products/?q={product_name}") as response:
            response = await response.json()

            try:
                result = response["results"][0]

                category = result.get("category")
                category_name = category.get("name") if category else None
                tags = [tag["name"] for tag in result["tags"]]

                return DjangoProduct(
                    category=category_name,
                    tags=tags,
                    image=result["image"]
                )
            except IndexError:
                return None
