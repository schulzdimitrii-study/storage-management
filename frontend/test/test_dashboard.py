import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import requests

# Adjust path to import frontend app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class TestDashboard(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('requests.get')
    def test_dashboard_index_success(self, mock_get):
        mock_products = MagicMock()
        mock_products.status_code = 200
        mock_products.json.return_value = [
            {"id": 1, "name": "Test Product", "quantity": 10, "min_quantity": 5, "price": 100.0}
        ]
        
        mock_categories = MagicMock()
        mock_categories.status_code = 200
        mock_categories.json.return_value = [{"id": 1, "name": "Electronics"}]
        
        mock_suppliers = MagicMock()
        mock_suppliers.status_code = 200
        mock_suppliers.json.return_value = [{"id": 1, "name": "Acme Corp"}]
        
        mock_movements = MagicMock()
        mock_movements.status_code = 200
        mock_movements.json.return_value = [
            {"id": 1, "product_id": 1, "movement_type": "IN", "quantity": 5, "created_at": "2026-06-15T12:00:00"}
        ]
        
        mock_get.side_effect = [mock_products, mock_categories, mock_suppliers, mock_movements]
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        self.assertIn(b'Test Product', response.data)

    @patch('requests.get')
    def test_dashboard_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Não foi possível conectar à API do Backend'.encode('utf-8'), response.data)

    @patch('requests.get')
    def test_dashboard_generic_exception(self, mock_get):
        mock_get.side_effect = Exception("Generic error")
        
        response = self.app.get('/')
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Generic error', response.data)

if __name__ == '__main__':
    unittest.main()
