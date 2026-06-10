from typing import Optional
from pydantic import BaseModel, Field

class SupplierCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(None, max_length=100)
    phone: str = Field(None, max_length=20)
    address: str = Field(None, max_length=255)

class SupplierUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=255)
