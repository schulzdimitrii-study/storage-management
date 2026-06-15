from pydantic import BaseModel, Field
from typing import Optional

class Category(BaseModel):
    id: int = Field(..., ge=1)
    name: str = Field(..., min_length=1)
    description: Optional[str] = None