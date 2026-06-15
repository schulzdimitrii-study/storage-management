
from models.category import Category
from schemas.category import CategoryCreate, CategoryUpdate
from db.connection import get_db_connection


class CategoryService:
    def __init__(self):
        pass

    async def create_category(self, category_data: CategoryCreate):
        conn = await get_db_connection()
        try:
            row = await conn.fetchrow(
                """INSERT INTO categories (name, description)
                VALUES ($1, $2)
                RETURNING id, name, description""",
                category_data.name, category_data.description
            )
            return Category(**dict(row))
        finally:
            await conn.close()

    async def get_categories(self):
        conn = await get_db_connection()
        try:
            rows = await conn.fetch("SELECT id, name, description FROM categories")
            return [Category(**dict(row)) for row in rows]
        finally:
            await conn.close()

    async def get_category(self, category_id: int):
        conn = await get_db_connection()
        try:
            row = await conn.fetchrow(
                "SELECT id, name, description FROM categories WHERE id = $1",
                category_id
            )
            if not row:
                raise ValueError(f"Category with id {category_id} not found")
            return Category(**dict(row))
        finally:
            await conn.close()

    async def update_category(self, category_id: int, category_data: CategoryUpdate):
        conn = await get_db_connection()
        try:
            existing = await conn.fetchrow(
                "SELECT id FROM categories WHERE id = $1", category_id
            )
            if not existing:
                raise ValueError(f"Category with id {category_id} not found")

            row = await conn.fetchrow(
                """UPDATE categories SET name = COALESCE($1, name), description = COALESCE($2, description)
                WHERE id = $3
                RETURNING id, name, description""",
                category_data.name, category_data.description, category_id
            )
            return Category(**dict(row))
        finally:
            await conn.close()

    async def delete_category(self, category_id: int):
        conn = await get_db_connection()
        try:
            await conn.execute("DELETE FROM categories WHERE id = $1", category_id)
        finally:
            await conn.close()


category_service = CategoryService()