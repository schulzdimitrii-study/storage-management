from fastapi import APIRouter, HTTPException
from models.products import Product
from schemas.products import ProductCreate, ProductUpdate
from services.products_service import product_service

products_router = APIRouter(prefix="/products", tags=["Products"])

@products_router.post("/", response_model=Product, status_code=201)
async def create_product(product: ProductCreate):
    try:
        return await product_service.create_product(product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@products_router.get("/", response_model=list[Product], status_code=200)
async def get_products():
    return await product_service.get_products()

@products_router.get("/{product_id}", response_model=Product, status_code=200)
async def get_product(product_id: int):
    try:
        return await product_service.get_product(product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@products_router.put("/{product_id}", response_model=Product, status_code=200)
async def update_product(product_id: int, product: ProductUpdate):
    try:
        return await product_service.update_product(product_id, product)
    except ValueError as e:
        error_msg = str(e)
        if "not found" in error_msg and "Product" in error_msg:
            raise HTTPException(status_code=404, detail=error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

@products_router.delete("/{product_id}", status_code=200)
async def delete_product(product_id: int):
    try:
        await product_service.delete_product(product_id)
        return {"message": "Product deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
