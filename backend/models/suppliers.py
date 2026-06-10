from pydantic import BaseModel, Field
from typing import Optional

class Supplier(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]