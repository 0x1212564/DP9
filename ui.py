from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QListWidget, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self, order_manager):
        super().__init__()
        self.order_manager = order_manager
        self.setWindowTitle("Bestelinterface")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        self.label = QLabel("Welkom bij Lake Side Mania Bestelinterface")
        layout.addWidget(self.label)

        self.product_list = QListWidget()
        layout.addWidget(self.product_list)
        self.load_products()

        self.checkout_button = QPushButton("Afrekenen")
        self.checkout_button.clicked.connect(self.checkout)
        layout.addWidget(self.checkout_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_products(self):
        products = self.order_manager.fetch_products()
        for product in products:
            self.product_list.addItem(f"{product.name} - €{product.price:.2f}")

    def checkout(self):
        message = self.order_manager.checkout()
        QMessageBox.information(self, "Bestelling", message)
