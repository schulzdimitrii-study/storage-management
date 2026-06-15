import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust path to import frontend app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class TestManagement(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('requests.get')
    def test_management_index_success(self, mock_get):
        mock_categories = MagicMock()
        mock_categories.status_code = 200
        mock_categories.json.return_value = [{"id": 1, "name": "Electronics", "description": "Gadgets"}]
        
        mock_suppliers = MagicMock()
        mock_suppliers.status_code = 200
        mock_suppliers.json.return_value = [{"id": 1, "name": "Acme Corp", "email": "info@acme.com", "phone": "123", "address": "Road"}]
        
        mock_get.side_effect = [mock_categories, mock_suppliers]
        
        response = self.app.get('/management')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Acme Corp', response.data)
        self.assertIn(b'Electronics', response.data)

    @patch('requests.get')
    def test_management_index_exception(self, mock_get):
        mock_get.side_effect = Exception("Database error")
        
        response = self.app.get('/management')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Erro ao carregar dados:'.encode('utf-8'), response.data)

    @patch('requests.post')
    def test_supplier_create_success(self, mock_post):
        mock_res = MagicMock()
        mock_res.status_code = 201
        mock_post.return_value = mock_res
        
        payload = {
            "name": "New Supplier",
            "email": "sup@test.com",
            "phone": "555",
            "address": "Supplier Street"
        }
        
        response = self.app.post('/management/suppliers/create', data=payload)
        self.assertEqual(response.status_code, 302)
        mock_post.assert_called_once()

    @patch('requests.delete')
    def test_supplier_delete_success(self, mock_delete):
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_delete.return_value = mock_res
        
        response = self.app.post('/management/suppliers/delete/1')
        self.assertEqual(response.status_code, 302)
        mock_delete.assert_called_once()

    @patch('requests.post')
    def test_category_create_success(self, mock_post):
        mock_res = MagicMock()
        mock_res.status_code = 201
        mock_post.return_value = mock_res
        
        payload = {
            "name": "New Category",
            "description": "Category Desc"
        }
        
        response = self.app.post('/management/categories/create', data=payload)
        self.assertEqual(response.status_code, 302)
        mock_post.assert_called_once()

    @patch('requests.delete')
    def test_category_delete_success(self, mock_delete):
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_delete.return_value = mock_res
        
        response = self.app.post('/management/categories/delete/1')
        self.assertEqual(response.status_code, 302)
        mock_delete.assert_called_once()

    @patch('requests.put')
    def test_supplier_update_success(self, mock_put):
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_put.return_value = mock_res
        
        payload = {
            "name": "Updated Supplier",
            "email": "updated@test.com",
            "phone": "999",
            "address": "New Supplier Street"
        }
        
        response = self.app.post('/management/suppliers/update/1', data=payload)
        self.assertEqual(response.status_code, 302)
        mock_put.assert_called_once()

    @patch('requests.put')
    def test_category_update_success(self, mock_put):
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_put.return_value = mock_res
        
        payload = {
            "name": "Updated Category",
            "description": "Updated Category Desc"
        }
        
        response = self.app.post('/management/categories/update/1', data=payload)
        self.assertEqual(response.status_code, 302)
        mock_put.assert_called_once()

if __name__ == '__main__':
    unittest.main()
