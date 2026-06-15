from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StockMovement(BaseModel):
    id: int
    product_id: int
    movement_type: str = Field(..., pattern="^(IN|OUT)$")
    quantity: int = Field(..., gt=0)
    reason: Optional[str] = None
    created_at: datetime
