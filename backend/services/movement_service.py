from models.movement import StockMovement
from schemas.movement import MovementCreate
from db.connection import get_db_connection

class MovementService:
    async def create_movement(self, movement_data: MovementCreate) -> StockMovement:
        conn = await get_db_connection()
        try:
            async with conn.transaction():
                product = await conn.fetchrow(
                    "SELECT id, quantity FROM products WHERE id = $1",
                    movement_data.product_id
                )
                if not product:
                    raise ValueError(f"Product with id {movement_data.product_id} not found")

                current_qty = product["quantity"]

                if movement_data.movement_type == "IN":
                    new_qty = current_qty + movement_data.quantity
                elif movement_data.movement_type == "OUT":
                    if current_qty < movement_data.quantity:
                        raise ValueError(f"Insufficient stock for product id {movement_data.product_id}. Available: {current_qty}, Requested: {movement_data.quantity}")
                    new_qty = current_qty - movement_data.quantity
                else:
                    raise ValueError("Invalid movement type. Must be 'IN' or 'OUT'")

                await conn.execute(
                    "UPDATE products SET quantity = $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2",
                    new_qty, movement_data.product_id
                )

                row = await conn.fetchrow(
                    """INSERT INTO stock_movements (product_id, movement_type, quantity, reason)
                       VALUES ($1, $2, $3, $4)
                       RETURNING id, product_id, movement_type, quantity, reason, created_at""",
                    movement_data.product_id, movement_data.movement_type, movement_data.quantity, movement_data.reason
                )

                return StockMovement(**dict(row))
        finally:
            await conn.close()

    async def get_movements_by_product(self, product_id: int) -> list[StockMovement]:
        conn = await get_db_connection()
        try:
            product = await conn.fetchrow("SELECT id FROM products WHERE id = $1", product_id)
            if not product:
                raise ValueError(f"Product with id {product_id} not found")

            rows = await conn.fetch(
                """SELECT id, product_id, movement_type, quantity, reason, created_at
                   FROM stock_movements
                   WHERE product_id = $1
                   ORDER BY created_at DESC""",
                product_id
            )
            return [StockMovement(**dict(row)) for row in rows]
        finally:
            await conn.close()

movement_service = MovementService()
