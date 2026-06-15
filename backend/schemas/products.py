from pydantic import BaseModel, Field
from typing import Optional, List

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    sku: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., ge=0.0)
    quantity: int = Field(0, ge=0)
    min_quantity: int = Field(0, ge=0)
    supplier_id: Optional[int] = None
    category_ids: List[int] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    sku: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, ge=0.0)
    quantity: Optional[int] = Field(None, ge=0)
    min_quantity: Optional[int] = Field(None, ge=0)
    supplier_id: Optional[int] = None
    category_ids: Optional[List[int]] = None
