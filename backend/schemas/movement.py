from pydantic import BaseModel, Field
from typing import Optional

class MovementCreate(BaseModel):
    product_id: int
    movement_type: str = Field(..., pattern="^(IN|OUT)$")
    quantity: int = Field(..., gt=0)
    reason: Optional[str] = None
