from fastapi import APIRouter, HTTPException
from models.suppliers import Supplier
from schemas.suppliers import SupplierCreate, SupplierUpdate
from services.suppliers_service import supplier_service

suppliers_router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@suppliers_router.post("/", response_model=Supplier, status_code=201)
async def create_supplier(supplier: SupplierCreate):
    return await supplier_service.create_supplier(supplier)

@suppliers_router.get("/", response_model=list[Supplier])
async def get_suppliers():
    return await supplier_service.get_suppliers()

@suppliers_router.get("/{supplier_id}", response_model=Supplier)
async def get_supplier(supplier_id: int):
    try:
        return await supplier_service.get_supplier(supplier_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@suppliers_router.put("/{supplier_id}", response_model=Supplier)
async def update_supplier(supplier_id: int, supplier: SupplierUpdate):
    try:
        return await supplier_service.update_supplier(supplier_id, supplier)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@suppliers_router.delete("/{supplier_id}", status_code=200)
async def delete_supplier(supplier_id: int):
    await supplier_service.delete_supplier(supplier_id)
    return {"message": "Supplier deleted successfully"}
