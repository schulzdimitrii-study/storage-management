from models.products import Product
from schemas.products import ProductCreate, ProductUpdate
from db.connection import get_db_connection

class ProductsService:
    async def create_product(self, product_data: ProductCreate) -> Product:
        conn = await get_db_connection()
        try:
            async with conn.transaction():
                if product_data.supplier_id is not None:
                    supplier = await conn.fetchrow("SELECT id FROM suppliers WHERE id = $1", product_data.supplier_id)
                    if not supplier:
                        raise ValueError(f"Supplier with id {product_data.supplier_id} not found")

                if product_data.category_ids:
                    categories = await conn.fetch(
                        "SELECT id FROM categories WHERE id = ANY($1)",
                        product_data.category_ids
                    )
                    found_ids = {row["id"] for row in categories}
                    missing_ids = set(product_data.category_ids) - found_ids
                    if missing_ids:
                        raise ValueError(f"Categories with ids {list(missing_ids)} not found")

                existing_sku = await conn.fetchrow("SELECT id FROM products WHERE sku = $1", product_data.sku)
                if existing_sku:
                    raise ValueError(f"Product with SKU '{product_data.sku}' already exists")

                row = await conn.fetchrow(
                    """INSERT INTO products (name, description, sku, price, quantity, min_quantity, supplier_id)
                       VALUES ($1, $2, $3, $4, $5, $6, $7)
                       RETURNING id, name, description, sku, price, quantity, min_quantity, supplier_id""",
                    product_data.name, product_data.description, product_data.sku,
                    product_data.price, product_data.quantity, product_data.min_quantity, product_data.supplier_id
                )
                product_id = row["id"]

                if product_data.category_ids:
                    for cat_id in product_data.category_ids:
                        await conn.execute(
                            "INSERT INTO product_categories (product_id, category_id) VALUES ($1, $2)",
                            product_id, cat_id
                        )

                product_dict = dict(row)
                product_dict["price"] = float(product_dict["price"])
                product_dict["category_ids"] = product_data.category_ids
                return Product(**product_dict)
        finally:
            await conn.close()

    async def get_products(self) -> list[Product]:
        conn = await get_db_connection()
        try:
            rows = await conn.fetch(
                """SELECT p.id, p.name, p.description, p.sku, p.price, p.quantity, p.min_quantity, p.supplier_id,
                          COALESCE(ARRAY_AGG(pc.category_id) FILTER (WHERE pc.category_id IS NOT NULL), '{}') AS category_ids
                   FROM products p
                   LEFT JOIN product_categories pc ON p.id = pc.product_id
                   GROUP BY p.id"""
            )
            result = []
            for r in rows:
                d = dict(r)
                d["price"] = float(d["price"])
                # Convert array pg type to python list
                d["category_ids"] = list(d["category_ids"])
                result.append(Product(**d))
            return result
        finally:
            await conn.close()

    async def get_product(self, product_id: int) -> Product:
        conn = await get_db_connection()
        try:
            row = await conn.fetchrow(
                """SELECT p.id, p.name, p.description, p.sku, p.price, p.quantity, p.min_quantity, p.supplier_id,
                          COALESCE(ARRAY_AGG(pc.category_id) FILTER (WHERE pc.category_id IS NOT NULL), '{}') AS category_ids
                   FROM products p
                   LEFT JOIN product_categories pc ON p.id = pc.product_id
                   WHERE p.id = $1
                   GROUP BY p.id""",
                product_id
            )
            if not row:
                raise ValueError(f"Product with id {product_id} not found")
            d = dict(row)
            d["price"] = float(d["price"])
            d["category_ids"] = list(d["category_ids"])
            return Product(**d)
        finally:
            await conn.close()

    async def update_product(self, product_id: int, product_data: ProductUpdate) -> Product:
        conn = await get_db_connection()
        try:
            async with conn.transaction():
                # Verify product exists
                existing = await conn.fetchrow("SELECT id FROM products WHERE id = $1", product_id)
                if not existing:
                    raise ValueError(f"Product with id {product_id} not found")

                # Verify supplier if provided
                if product_data.supplier_id is not None:
                    supplier = await conn.fetchrow("SELECT id FROM suppliers WHERE id = $1", product_data.supplier_id)
                    if not supplier:
                        raise ValueError(f"Supplier with id {product_data.supplier_id} not found")

                # Verify all categories if provided
                if product_data.category_ids is not None:
                    categories = await conn.fetch(
                        "SELECT id FROM categories WHERE id = ANY($1)",
                        product_data.category_ids
                    )
                    found_ids = {row["id"] for row in categories}
                    missing_ids = set(product_data.category_ids) - found_ids
                    if missing_ids:
                        raise ValueError(f"Categories with ids {list(missing_ids)} not found")

                if product_data.sku is not None:
                    sku_owner = await conn.fetchrow("SELECT id FROM products WHERE sku = $1 AND id != $2", product_data.sku, product_id)
                    if sku_owner:
                        raise ValueError(f"Product with SKU '{product_data.sku}' already exists")

                row = await conn.fetchrow(
                    """UPDATE products SET
                       name = COALESCE($1, name),
                       description = COALESCE($2, description),
                       sku = COALESCE($3, sku),
                       price = COALESCE($4, price),
                       quantity = COALESCE($5, quantity),
                       min_quantity = COALESCE($6, min_quantity),
                       supplier_id = COALESCE($7, supplier_id)
                       WHERE id = $8
                       RETURNING id, name, description, sku, price, quantity, min_quantity, supplier_id""",
                    product_data.name, product_data.description, product_data.sku,
                    product_data.price, product_data.quantity, product_data.min_quantity,
                    product_data.supplier_id, product_id
                )

                if product_data.category_ids is not None:
                    await conn.execute("DELETE FROM product_categories WHERE product_id = $1", product_id)
                    for cat_id in product_data.category_ids:
                        await conn.execute(
                            "INSERT INTO product_categories (product_id, category_id) VALUES ($1, $2)",
                            product_id, cat_id
                        )

                return await self.get_product(product_id)
        finally:
            await conn.close()

    async def delete_product(self, product_id: int) -> None:
        conn = await get_db_connection()
        try:
            existing = await conn.fetchrow("SELECT id FROM products WHERE id = $1", product_id)
            if not existing:
                raise ValueError(f"Product with id {product_id} not found")
            await conn.execute("DELETE FROM products WHERE id = $1", product_id)
        finally:
            await conn.close()

product_service = ProductsService()
