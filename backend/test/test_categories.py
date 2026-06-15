import sys
import os
import pytest
from unittest.mock import AsyncMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

CATEGORY_PAYLOAD = {
    "name": "Electronics",
    "description": "Gadgets and devices"
}


class TestCreateCategory:
    @patch("services.category_service.get_db_connection")
    def test_create_category_success(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value={"id": 1, **CATEGORY_PAYLOAD})
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.post("/api/v1/categories/", json=CATEGORY_PAYLOAD)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Electronics"
        assert data["description"] == "Gadgets and devices"
        assert data["id"] == 1

    def test_create_category_missing_name(self):
        response = client.post("/api/v1/categories/", json={"description": "Missing name"})
        assert response.status_code == 422


class TestGetCategories:
    @patch("services.category_service.get_db_connection")
    def test_get_categories_returns_list(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetch = AsyncMock(return_value=[
            {"id": 1, **CATEGORY_PAYLOAD},
            {"id": 2, "name": "Books", "description": None},
        ])
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/categories/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Electronics"
        assert data[1]["name"] == "Books"

    @patch("services.category_service.get_db_connection")
    def test_get_categories_empty(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetch = AsyncMock(return_value=[])
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/categories/")

        assert response.status_code == 200
        assert response.json() == []


class TestGetCategoryById:
    @patch("services.category_service.get_db_connection")
    def test_get_category_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value={"id": 1, **CATEGORY_PAYLOAD})
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/categories/1")

        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["name"] == "Electronics"

    @patch("services.category_service.get_db_connection")
    def test_get_category_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value=None)
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/categories/999")

        assert response.status_code == 404


class TestUpdateCategory:
    @patch("services.category_service.get_db_connection")
    def test_update_category_success(self, mock_conn_factory):
        updated = {**CATEGORY_PAYLOAD, "name": "Home Appliances"}
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(side_effect=[
            {"id": 1},
            {"id": 1, **updated},
        ])
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.put("/api/v1/categories/1", json={"name": "Home Appliances"})

        assert response.status_code == 200
        assert response.json()["name"] == "Home Appliances"

    @patch("services.category_service.get_db_connection")
    def test_update_category_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value=None)
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.put("/api/v1/categories/999", json={"name": "New Category"})

        assert response.status_code == 404


class TestDeleteCategory:
    @patch("services.category_service.get_db_connection")
    def test_delete_category_success(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.execute = AsyncMock()
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.delete("/api/v1/categories/1")

        assert response.status_code == 200
        assert response.json()["message"] == "Category deleted successfully"
