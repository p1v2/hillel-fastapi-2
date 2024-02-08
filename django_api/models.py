from typing import List, Optional

from pydantic import BaseModel


class DjangoProduct(BaseModel):
    category: Optional[str]
    tags: List[str]
    image: Optional[str]
