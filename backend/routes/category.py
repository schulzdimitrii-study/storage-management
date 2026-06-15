from fastapi import APIRouter, HTTPException
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate
from services.category_service import category_service

categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.post("/", response_model=Category, status_code=201)
async def create_category(category: CategoryCreate):
    return await category_service.create_category(category)

@categories_router.get("/", response_model=list[Category], status_code=200)
async def get_categories():
    return await category_service.get_categories()

@categories_router.get("/{category_id}", response_model=Category, status_code=200)
async def get_category(category_id: int):
    try:
        return await category_service.get_category(category_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@categories_router.put("/{category_id}", response_model=Category, status_code=200)
async def update_category(category_id: int, category: CategoryUpdate):
    try:
        return await category_service.update_category(category_id, category)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@categories_router.delete("/{category_id}", status_code=200)
async def delete_category(category_id: int):
    try:
        await category_service.delete_category(category_id)
        return {"message": "Category deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

