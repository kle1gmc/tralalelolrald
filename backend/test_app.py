import unittest
from backend.server import app
import json
from psycopg2 import connect

class ProductAPITest(unittest.TestCase):

    def setUp(self):
        # Настроим тестовое окружение
        self.app = app.test_client()
        self.app.testing = True

        # Подключение к тестовой базе данных
        self.conn = connect(dbname='db1', user='postgres', password='123', host='localhost', port='5432')
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS products")
            cur.execute("""
                CREATE TABLE products (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL
                )
            """)
        self.conn.commit()

    def tearDown(self):
        # Очищаем тестовую базу данных
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS products")
        self.conn.commit()
        self.conn.close()

    def test_add_product(self):
        # Тестируем добавление товара
        product_data = {
            "name": "Ноутбук",
            "price": 159999,
            "quantity": 1
        }

        response = self.app.post('/add_product', data=json.dumps(product_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Товар 'Ноутбук' добавлен.", response.get_json()['message'])

    def test_add_product_missing_field(self):
        # Тестируем добавление товара с отсутствующим полем
        product_data = {
            "name": "Ноутбук",
            "price": 159999
        }

        response = self.app.post('/add_product', data=json.dumps(product_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Все поля обязательны", response.get_json()['error'])

    def test_get_products(self):
        # Тестируем получение списка товаров
        product_data = {
            "name": "Ноутбук",
            "price": 159999,
            "quantity": 1
        }

        # Добавляем товар в базу данных
        self.app.post('/add_product', data=json.dumps(product_data), content_type='application/json')

        # Получаем список товаров
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)

        products = response.get_json()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]['name'], "Ноутбук")
        self.assertEqual(products[0]['price'], 159999)
        self.assertEqual(products[0]['quantity'], 1)

if __name__ == '__main__':
    unittest.main()
