import sys
import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

PRODUCT_PAYLOAD = {
    "name": "Mechanical Keyboard",
    "description": "RGB mechanical keyboard",
    "sku": "KB-123",
    "price": 89.99,
    "quantity": 10,
    "min_quantity": 5,
    "supplier_id": 1,
    "category_ids": [1, 2]
}


def get_mock_transaction():
    mock_tx = AsyncMock()
    mock_tx.__aenter__ = AsyncMock()
    mock_tx.__aexit__ = AsyncMock(return_value=False)
    return mock_tx


class TestCreateProduct:
    @patch("services.products_service.get_db_connection")
    def test_create_product_success(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.transaction = MagicMock(return_value=get_mock_transaction())
        
        # Mocking db queries:
        # 1. check supplier exists -> return one row
        # 2. check categories exist -> return rows for category 1 and 2
        # 3. check SKU uniqueness -> return None (no product with that SKU exists)
        # 4. insert product -> return row with product details
        mock_conn.fetchrow = AsyncMock(side_effect=[
            {"id": 1},  # supplier check
            None,       # SKU check
            {
                "id": 1,
                "name": "Mechanical Keyboard",
                "description": "RGB mechanical keyboard",
                "sku": "KB-123",
                "price": 89.99,
                "quantity": 10,
                "min_quantity": 5,
                "supplier_id": 1
            }  # insert product
        ])
        mock_conn.fetch = AsyncMock(return_value=[{"id": 1}, {"id": 2}])  # categories check
        mock_conn.execute = AsyncMock()
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.post("/api/v1/products/", json=PRODUCT_PAYLOAD)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Mechanical Keyboard"
        assert data["sku"] == "KB-123"
        assert data["category_ids"] == [1, 2]

    @patch("services.products_service.get_db_connection")
    def test_create_product_supplier_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.transaction = MagicMock(return_value=get_mock_transaction())
        mock_conn.fetchrow = AsyncMock(return_value=None)  # supplier check fails
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.post("/api/v1/products/", json=PRODUCT_PAYLOAD)

        assert response.status_code == 400
        assert "Supplier with id 1 not found" in response.json()["detail"]

    @patch("services.products_service.get_db_connection")
    def test_create_product_category_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.transaction = MagicMock(return_value=get_mock_transaction())
        mock_conn.fetchrow = AsyncMock(return_value={"id": 1})  # supplier check succeeds
        mock_conn.fetch = AsyncMock(return_value=[{"id": 1}])  # missing category 2
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.post("/api/v1/products/", json=PRODUCT_PAYLOAD)

        assert response.status_code == 400
        assert "Categories with ids" in response.json()["detail"]

    @patch("services.products_service.get_db_connection")
    def test_create_product_sku_conflict(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.transaction = MagicMock(return_value=get_mock_transaction())
        mock_conn.fetchrow = AsyncMock(side_effect=[
            {"id": 1},  # supplier check
            {"id": 99}  # SKU check returns another product ID (conflict)
        ])
        mock_conn.fetch = AsyncMock(return_value=[{"id": 1}, {"id": 2}])
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.post("/api/v1/products/", json=PRODUCT_PAYLOAD)

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]


class TestGetProducts:
    @patch("services.products_service.get_db_connection")
    def test_get_products_returns_list(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetch = AsyncMock(return_value=[
            {
                "id": 1,
                "name": "Mechanical Keyboard",
                "description": "RGB mechanical keyboard",
                "sku": "KB-123",
                "price": 89.99,
                "quantity": 10,
                "min_quantity": 5,
                "supplier_id": 1,
                "category_ids": [1, 2]
            }
        ])
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/products/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Mechanical Keyboard"
        assert data[0]["category_ids"] == [1, 2]


class TestGetProductById:
    @patch("services.products_service.get_db_connection")
    def test_get_product_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value={
            "id": 1,
            "name": "Mechanical Keyboard",
            "description": "RGB mechanical keyboard",
            "sku": "KB-123",
            "price": 89.99,
            "quantity": 10,
            "min_quantity": 5,
            "supplier_id": 1,
            "category_ids": [1, 2]
        })
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/products/1")

        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["name"] == "Mechanical Keyboard"

    @patch("services.products_service.get_db_connection")
    def test_get_product_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value=None)
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/products/999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


class TestUpdateProduct:
    @patch("services.products_service.get_db_connection")
    def test_update_product_success(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.transaction = MagicMock(return_value=get_mock_transaction())
        
        # Mocking update flow queries:
        # 1. check product exists
        # 2. check supplier exists
        # 3. check categories exist
        # 4. check SKU uniqueness
        # 5. update statement returning updated product
        # 6. final get_product row (called inside update_product)
        mock_conn.fetchrow = AsyncMock(side_effect=[
            {"id": 1},  # product check
            {"id": 1},  # supplier check
            None,       # SKU check
            {
                "id": 1,
                "name": "Mechanical Keyboard Updated",
                "description": "RGB mechanical keyboard",
                "sku": "KB-123-UPD",
                "price": 99.99,
                "quantity": 10,
                "min_quantity": 5,
                "supplier_id": 1
            },          # update product returning
            {
                "id": 1,
                "name": "Mechanical Keyboard Updated",
                "description": "RGB mechanical keyboard",
                "sku": "KB-123-UPD",
                "price": 99.99,
                "quantity": 10,
                "min_quantity": 5,
                "supplier_id": 1,
                "category_ids": [1]
            }           # final get_product
        ])
        mock_conn.fetch = AsyncMock(return_value=[{"id": 1}])  # categories check
        mock_conn.execute = AsyncMock()
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.put(
            "/api/v1/products/1",
            json={"name": "Mechanical Keyboard Updated", "sku": "KB-123-UPD", "price": 99.99, "category_ids": [1], "supplier_id": 1}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Mechanical Keyboard Updated"
        assert data["sku"] == "KB-123-UPD"
        assert data["price"] == 99.99
        assert data["category_ids"] == [1]

    @patch("services.products_service.get_db_connection")
    def test_update_product_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.transaction = MagicMock(return_value=get_mock_transaction())
        mock_conn.fetchrow = AsyncMock(return_value=None)  # product check fails
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.put("/api/v1/products/999", json={"name": "New Name"})

        assert response.status_code == 404


class TestDeleteProduct:
    @patch("services.products_service.get_db_connection")
    def test_delete_product_success(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value={"id": 1})  # product check
        mock_conn.execute = AsyncMock()
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.delete("/api/v1/products/1")

        assert response.status_code == 200
        assert response.json()["message"] == "Product deleted successfully"

    @patch("services.products_service.get_db_connection")
    def test_delete_product_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value=None)  # product check fails
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.delete("/api/v1/products/999")

        assert response.status_code == 404
