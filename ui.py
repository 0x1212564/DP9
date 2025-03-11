from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QListWidget, QMessageBox, \
    QGridLayout, QHBoxLayout


class MainWindow(QMainWindow):
    def __init__(self, order_manager):
        super().__init__()
        self.order_manager = order_manager
        self.setWindowTitle("Bestelinterface")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()
        product_layout = QGridLayout()

        self.product_buttons = []
        self.load_products(product_layout)
        main_layout.addLayout(product_layout)

        cart_layout = QVBoxLayout()
        self.cart_list = QListWidget()
        cart_layout.addWidget(self.cart_list)

        self.total_label = QLabel("Totaal: €0.00")
        cart_layout.addWidget(self.total_label)

        self.checkout_button = QPushButton("Afrekenen")
        self.checkout_button.clicked.connect(self.checkout)
        cart_layout.addWidget(self.checkout_button)

        layout = QHBoxLayout()
        layout.addLayout(main_layout)
        layout.addLayout(cart_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_products(self, layout):
        products = self.order_manager.fetch_products()
        button_width = 150
        button_height = 50
        for i, product in enumerate(products):
            button = QPushButton(f"{product.name}\n€{product.price:.2f}")
            button.clicked.connect(self.create_add_to_cart_handler(product))
            button.setFixedSize(button_width, button_height)
            layout.addWidget(button, i // 3, i % 3)
            layout.setAlignment(Qt.AlignTop)
            self.product_buttons.append(button)

    def create_add_to_cart_handler(self, product):
        return lambda: self.add_to_cart(product)

    def add_to_cart(self, product):
        self.order_manager.add_to_order(product)
        self.cart_list.addItem(f"{product.name} - €{product.price:.2f}")
        self.update_total()

    def update_total(self):
        total = self.order_manager.get_total()
        self.total_label.setText(f"Totaal: €{total:.2f}")

    def checkout(self):
        message = self.order_manager.checkout()
        QMessageBox.information(self, "Bestelling", message)
        self.cart_list.clear()
        self.update_total()
