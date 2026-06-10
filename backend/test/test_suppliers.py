import sys
import os
import pytest
from unittest.mock import AsyncMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

SUPPLIER_PAYLOAD = {
    "name": "Acme Corp",
    "email": "contact@acme.com",
    "phone": "11999999999",
    "address": "123 Main St"
}


class TestHealthcheck:
    def test_root_returns_running(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "API is running! 🚀"


class TestCreateSupplier:
    @patch("services.suppliers_service.get_db_connection")
    def test_create_supplier_success(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value={"id": 1, **SUPPLIER_PAYLOAD})
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.post("/api/v1/suppliers/", json=SUPPLIER_PAYLOAD)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Acme Corp"
        assert data["email"] == "contact@acme.com"
        assert data["id"] == 1

    def test_create_supplier_missing_name(self):
        response = client.post("/api/v1/suppliers/", json={"email": "x@x.com"})
        assert response.status_code == 422


class TestGetSuppliers:
    @patch("services.suppliers_service.get_db_connection")
    def test_get_suppliers_returns_list(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetch = AsyncMock(return_value=[
            {"id": 1, **SUPPLIER_PAYLOAD},
            {"id": 2, "name": "Beta Inc", "email": "b@b.com", "phone": None, "address": None},
        ])
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/suppliers/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["name"] == "Acme Corp"
        assert data[1]["name"] == "Beta Inc"

    @patch("services.suppliers_service.get_db_connection")
    def test_get_suppliers_empty(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetch = AsyncMock(return_value=[])
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/suppliers/")

        assert response.status_code == 200
        assert response.json() == []


class TestGetSupplierById:
    @patch("services.suppliers_service.get_db_connection")
    def test_get_supplier_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value={"id": 1, **SUPPLIER_PAYLOAD})
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/suppliers/1")

        assert response.status_code == 200
        assert response.json()["id"] == 1
        assert response.json()["name"] == "Acme Corp"

    @patch("services.suppliers_service.get_db_connection")
    def test_get_supplier_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value=None)
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/suppliers/999")

        assert response.status_code == 404


class TestUpdateSupplier:
    @patch("services.suppliers_service.get_db_connection")
    def test_update_supplier_success(self, mock_conn_factory):
        updated = {**SUPPLIER_PAYLOAD, "name": "Acme Updated"}
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(side_effect=[
            {"id": 1},
            {"id": 1, **updated},
        ])
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.put("/api/v1/suppliers/1", json={"name": "Acme Updated"})

        assert response.status_code == 200
        assert response.json()["name"] == "Acme Updated"

    @patch("services.suppliers_service.get_db_connection")
    def test_update_supplier_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value=None)
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.put("/api/v1/suppliers/999", json={"name": "Ghost"})

        assert response.status_code == 404


class TestDeleteSupplier:
    @patch("services.suppliers_service.get_db_connection")
    def test_delete_supplier_success(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.execute = AsyncMock()
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.delete("/api/v1/suppliers/1")

        assert response.status_code == 200
        assert response.json()["message"] == "Supplier deleted successfully"
