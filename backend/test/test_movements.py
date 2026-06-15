import sys
import os
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

MOVEMENT_PAYLOAD = {
    "product_id": 1,
    "movement_type": "IN",
    "quantity": 5,
    "reason": "Restock from supplier"
}


def get_mock_transaction():
    mock_tx = AsyncMock()
    mock_tx.__aenter__ = AsyncMock()
    mock_tx.__aexit__ = AsyncMock(return_value=False)
    return mock_tx


class TestCreateMovement:
    @patch("services.movement_service.get_db_connection")
    def test_create_movement_in_success(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.transaction = MagicMock(return_value=get_mock_transaction())
        
        created_time = datetime.now()
        mock_conn.fetchrow = AsyncMock(side_effect=[
            {"id": 1, "quantity": 10},
            {
                "id": 100,
                "product_id": 1,
                "movement_type": "IN",
                "quantity": 5,
                "reason": "Restock from supplier",
                "created_at": created_time
            }
        ])
        mock_conn.execute = AsyncMock()
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.post("/api/v1/movements/", json=MOVEMENT_PAYLOAD)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 100
        assert data["movement_type"] == "IN"
        assert data["quantity"] == 5
        mock_conn.execute.assert_called_once()
        assert mock_conn.execute.call_args[0][0].startswith("UPDATE products")
        assert mock_conn.execute.call_args[0][1] == 15

    @patch("services.movement_service.get_db_connection")
    def test_create_movement_out_success(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.transaction = MagicMock(return_value=get_mock_transaction())
        
        created_time = datetime.now()
        mock_conn.fetchrow = AsyncMock(side_effect=[
            {"id": 1, "quantity": 10},
            {
                "id": 101,
                "product_id": 1,
                "movement_type": "OUT",
                "quantity": 3,
                "reason": "Sale to customer",
                "created_at": created_time
            }
        ])
        mock_conn.execute = AsyncMock()
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        payload = {**MOVEMENT_PAYLOAD, "movement_type": "OUT", "quantity": 3, "reason": "Sale to customer"}
        response = client.post("/api/v1/movements/", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 101
        assert data["movement_type"] == "OUT"
        assert data["quantity"] == 3
        mock_conn.execute.assert_called_once()
        assert mock_conn.execute.call_args[0][1] == 7

    @patch("services.movement_service.get_db_connection")
    def test_create_movement_product_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.transaction = MagicMock(return_value=get_mock_transaction())
        mock_conn.fetchrow = AsyncMock(return_value=None)
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.post("/api/v1/movements/", json=MOVEMENT_PAYLOAD)

        assert response.status_code == 404
        assert "Product with id 1 not found" in response.json()["detail"]

    @patch("services.movement_service.get_db_connection")
    def test_create_movement_insufficient_stock(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.transaction = MagicMock(return_value=get_mock_transaction())
        mock_conn.fetchrow = AsyncMock(return_value={"id": 1, "quantity": 2})
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        payload = {**MOVEMENT_PAYLOAD, "movement_type": "OUT", "quantity": 5}
        response = client.post("/api/v1/movements/", json=payload)

        assert response.status_code == 400
        assert "Insufficient stock" in response.json()["detail"]

    def test_create_movement_invalid_type(self):
        payload = {**MOVEMENT_PAYLOAD, "movement_type": "INVALID"}
        response = client.post("/api/v1/movements/", json=payload)
        assert response.status_code == 422


class TestGetMovementsByProduct:
    @patch("services.movement_service.get_db_connection")
    def test_get_movements_success(self, mock_conn_factory):
        mock_conn = AsyncMock()
        created_time = datetime.now()
        mock_conn.fetchrow = AsyncMock(return_value={"id": 1})
        mock_conn.fetch = AsyncMock(return_value=[
            {
                "id": 100,
                "product_id": 1,
                "movement_type": "IN",
                "quantity": 5,
                "reason": "Restock",
                "created_at": created_time
            }
        ])
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/movements/1")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == 100
        assert data[0]["movement_type"] == "IN"

    @patch("services.movement_service.get_db_connection")
    def test_get_movements_product_not_found(self, mock_conn_factory):
        mock_conn = AsyncMock()
        mock_conn.fetchrow = AsyncMock(return_value=None)
        mock_conn.close = AsyncMock()
        mock_conn_factory.return_value = mock_conn

        response = client.get("/api/v1/movements/999")

        assert response.status_code == 404
