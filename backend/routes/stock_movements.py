from fastapi import APIRouter, HTTPException
from models.movement import StockMovement
from schemas.movement import MovementCreate
from services.movement_service import movement_service

stock_movements_router = APIRouter(prefix="/movements", tags=["Stock Movements"])

@stock_movements_router.post("/", response_model=StockMovement, status_code=201)
async def create_movement(movement: MovementCreate):
    try:
        return await movement_service.create_movement(movement)
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg:
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

@stock_movements_router.get("/{product_id}", response_model=list[StockMovement], status_code=200)
async def get_movements_by_product(product_id: int):
    try:
        return await movement_service.get_movements_by_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
