from pydantic import BaseModel, Field
from typing import Optional, List

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    sku: str
    price: float
    quantity: int = 0
    min_quantity: int = 0
    supplier_id: Optional[int] = None
    category_ids: List[int] = []
