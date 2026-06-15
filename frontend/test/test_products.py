import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust path to import frontend app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

class TestProducts(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('requests.get')
    def test_products_index_success(self, mock_get):
        mock_products = MagicMock()
        mock_products.status_code = 200
        mock_products.json.return_value = [
            {"id": 1, "name": "Laptop", "sku": "LAP-101", "price": 999.99, "quantity": 10, "min_quantity": 2, "supplier_id": 1, "category_ids": [1]}
        ]
        
        mock_categories = MagicMock()
        mock_categories.status_code = 200
        mock_categories.json.return_value = [{"id": 1, "name": "Electronics"}]
        
        mock_suppliers = MagicMock()
        mock_suppliers.status_code = 200
        mock_suppliers.json.return_value = [{"id": 1, "name": "Acme Corp"}]
        
        mock_get.side_effect = [mock_products, mock_categories, mock_suppliers]
        
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Laptop', response.data)
        self.assertIn(b'LAP-101', response.data)

    @patch('requests.get')
    def test_products_index_exception(self, mock_get):
        mock_get.side_effect = Exception("Failed to load products list")
        
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Erro ao carregar produtos:'.encode('utf-8'), response.data)

    @patch('requests.post')
    def test_product_create_success(self, mock_post):
        mock_res = MagicMock()
        mock_res.status_code = 201
        mock_post.return_value = mock_res
        
        payload = {
            "name": "New Product",
            "sku": "NEW-123",
            "price": "50.00",
            "quantity": "5",
            "min_quantity": "1",
            "supplier_id": "1",
            "category_ids": ["1", "2"]
        }
        
        response = self.app.post('/products/create', data=payload)
        self.assertEqual(response.status_code, 302)
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_product_create_failure(self, mock_post):
        mock_res = MagicMock()
        mock_res.status_code = 400
        mock_res.json.return_value = {"detail": "SKU already exists"}
        mock_post.return_value = mock_res
        
        payload = {"name": "New Product", "sku": "DUPE-SKU", "price": "10"}
        response = self.app.post('/products/create', data=payload)
        self.assertEqual(response.status_code, 302)
        mock_post.assert_called_once()

    @patch('requests.put')
    def test_product_update_success(self, mock_put):
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_put.return_value = mock_res
        
        payload = {
            "name": "Updated Product",
            "sku": "UPD-123",
            "price": "60.00",
            "quantity": "10",
            "min_quantity": "2",
            "supplier_id": "1",
            "category_ids": ["1"]
        }
        
        response = self.app.post('/products/update/1', data=payload)
        self.assertEqual(response.status_code, 302)
        mock_put.assert_called_once()

    @patch('requests.put')
    def test_product_update_failure(self, mock_put):
        mock_res = MagicMock()
        mock_res.status_code = 404
        mock_res.json.return_value = {"detail": "Product not found"}
        mock_put.return_value = mock_res
        
        payload = {"name": "Updated Product", "sku": "UPD-123", "price": "60.00"}
        response = self.app.post('/products/update/999', data=payload)
        self.assertEqual(response.status_code, 302)

    @patch('requests.delete')
    def test_product_delete_success(self, mock_delete):
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_delete.return_value = mock_res
        
        response = self.app.post('/products/delete/1')
        self.assertEqual(response.status_code, 302)
        mock_delete.assert_called_once()

    @patch('requests.post')
    def test_product_movement_success(self, mock_post):
        mock_res = MagicMock()
        mock_res.status_code = 201
        mock_post.return_value = mock_res
        
        payload = {
            "product_id": "1",
            "movement_type": "IN",
            "quantity": "10",
            "reason": "Restock"
        }
        
        response = self.app.post('/products/movement', data=payload)
        self.assertEqual(response.status_code, 302)
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_product_movement_failure(self, mock_post):
        mock_res = MagicMock()
        mock_res.status_code = 400
        mock_res.json.return_value = {"detail": "Insufficient stock"}
        mock_post.return_value = mock_res
        
        payload = {"product_id": "1", "movement_type": "OUT", "quantity": "100"}
        response = self.app.post('/products/movement', data=payload)
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
