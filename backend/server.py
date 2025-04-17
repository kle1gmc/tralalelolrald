from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Подключение к базе данных
DB_CONFIG = {
    'dbname': 'db1',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

# Инициализация базы данных
def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
    conn.commit()
    conn.close()

init_db()

# Добавление товара
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")

    if not name or not price or not quantity:
        return jsonify({"error": "Все поля обязательны"}), 400

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)"),
                (name, float(price), int(quantity))
            )
        conn.commit()
        conn.close()
        return jsonify({"message": f"Товар '{name}' добавлен."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Получение списка товаров
@app.route('/get_products', methods=['GET'])
def get_products():
    conn = psycopg2.connect(**DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM products")
        products = cur.fetchall()
    conn.close()
    return jsonify([{"id": p[0], "name": p[1], "price": p[2], "quantity": p[3]} for p in products])

# Удаление товара по ID
@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Товар с ID {product_id} удалён."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Обновление товара по ID
@app.route('/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")

    if not name or not price or not quantity:
        return jsonify({"error": "Все поля обязательны"}), 400

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE products
                SET name = %s, price = %s, quantity = %s
                WHERE id = %s
                """,
                (name, float(price), int(quantity), product_id)
            )
        conn.commit()
        conn.close()
        return jsonify({"message": f"Товар с ID {product_id} обновлён."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
