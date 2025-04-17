from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel
import requests

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Товары")

        layout = QVBoxLayout()

        self.input_id = QLineEdit(self)
        self.input_id.setPlaceholderText("ID товара (для удаления/обновления)")

        self.input_name = QLineEdit(self)
        self.input_name.setPlaceholderText("Название товара")

        self.input_price = QLineEdit(self)
        self.input_price.setPlaceholderText("Цена товара")

        self.input_quantity = QLineEdit(self)
        self.input_quantity.setPlaceholderText("Количество")

        self.btn_add = QPushButton("Добавить товар", self)
        self.btn_add.clicked.connect(self.add_product)

        self.btn_get = QPushButton("Показать товары", self)
        self.btn_get.clicked.connect(self.get_products)

        self.btn_delete = QPushButton("Удалить товар по ID", self)
        self.btn_delete.clicked.connect(self.delete_product)

        self.btn_update = QPushButton("Обновить товар по ID", self)
        self.btn_update.clicked.connect(self.update_product)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)

        layout.addWidget(self.input_id)
        layout.addWidget(self.input_name)
        layout.addWidget(self.input_price)
        layout.addWidget(self.input_quantity)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_update)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_get)
        layout.addWidget(self.output)

        self.setLayout(layout)
        self.resize(350, 500)

    def add_product(self):
        name = self.input_name.text().strip()
        price = self.input_price.text().strip()
        quantity = self.input_quantity.text().strip()

        if name and price and quantity:
            try:
                response = requests.post("http://localhost:5000/add_product", json={
                    "name": name,
                    "price": float(price),
                    "quantity": int(quantity)
                })
                result = response.json()
                if "error" in result:
                    self.output.append(f"Ошибка: {result['error']}")
                else:
                    self.output.append(result["message"])
            except Exception as e:
                self.output.append(f"Ошибка при подключении к серверу: {e}")
        else:
            self.output.append("Ошибка: Заполните все поля для добавления.")

    def get_products(self):
        try:
            response = requests.get("http://localhost:5000/get_products")
            products = response.json()

            self.output.clear()
            for product in products:
                self.output.append(f"{product['id']}. {product['name']} - {product['price']} руб. (x{product['quantity']})")
        except Exception as e:
            self.output.append(f"Ошибка при получении товаров: {e}")

    def delete_product(self):
        product_id = self.input_id.text().strip()

        if product_id:
            try:
                response = requests.delete(f"http://localhost:5000/delete_product/{product_id}")
                result = response.json()
                if "error" in result:
                    self.output.append(f"Ошибка: {result['error']}")
                else:
                    self.output.append(result["message"])
            except Exception as e:
                self.output.append(f"Ошибка при удалении товара: {e}")
        else:
            self.output.append("Введите ID для удаления.")

    def update_product(self):
        product_id = self.input_id.text().strip()
        name = self.input_name.text().strip()
        price = self.input_price.text().strip()
        quantity = self.input_quantity.text().strip()

        if product_id and name and price and quantity:
            try:
                response = requests.put(f"http://localhost:5000/update_product/{product_id}", json={
                    "name": name,
                    "price": float(price),
                    "quantity": int(quantity)
                })
                result = response.json()
                if "error" in result:
                    self.output.append(f"Ошибка: {result['error']}")
                else:
                    self.output.append(result["message"])
            except Exception as e:
                self.output.append(f"Ошибка при обновлении товара: {e}")
        else:
            self.output.append("Заполните ID, название, цену и количество для обновления.")

if __name__ == '__main__':
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()
