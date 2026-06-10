from models.suppliers import Supplier
from schemas.suppliers import SupplierCreate, SupplierUpdate
from db.connection import get_db_connection


class SuppliersService:
    async def create_supplier(self, supplier_data: SupplierCreate) -> Supplier:
        conn = await get_db_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO suppliers (name, email, phone, address)
                   VALUES ($1, $2, $3, $4)
                   RETURNING id, name, email, phone, address""",
                supplier_data.name, supplier_data.email, supplier_data.phone, supplier_data.address
            )
            return Supplier(**dict(row))
        finally:
            await conn.close()

    async def get_suppliers(self) -> list[Supplier]:
        conn = await get_db_connection()
        try:
            rows = await conn.fetch("SELECT id, name, email, phone, address FROM suppliers")
            return [Supplier(**dict(row)) for row in rows]
        finally:
            await conn.close()

    async def get_supplier(self, supplier_id: int) -> Supplier:
        conn = await get_db_connection()
        try:
            row = await conn.fetchrow(
                "SELECT id, name, email, phone, address FROM suppliers WHERE id = $1",
                supplier_id
            )
            if not row:
                raise ValueError(f"Supplier with id {supplier_id} not found")
            return Supplier(**dict(row))
        finally:
            await conn.close()

    async def update_supplier(self, supplier_id: int, supplier_data: SupplierUpdate) -> Supplier:
        conn = await get_db_connection()
        try:
            existing = await conn.fetchrow(
                "SELECT id FROM suppliers WHERE id = $1", supplier_id
            )
            if not existing:
                raise ValueError(f"Supplier with id {supplier_id} not found")

            row = await conn.fetchrow(
                """UPDATE suppliers SET name = COALESCE($1, name), email = COALESCE($2, email),
                   phone = COALESCE($3, phone), address = COALESCE($4, address)
                   WHERE id = $5
                   RETURNING id, name, email, phone, address""",
                supplier_data.name, supplier_data.email, supplier_data.phone, supplier_data.address, supplier_id
            )
            return Supplier(**dict(row))
        finally:
            await conn.close()

    async def delete_supplier(self, supplier_id: int) -> None:
        conn = await get_db_connection()
        try:
            await conn.execute("DELETE FROM suppliers WHERE id = $1", supplier_id)
        finally:
            await conn.close()


supplier_service = SuppliersService()