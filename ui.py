from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QListWidget, QMessageBox,
                             QGridLayout, QHBoxLayout, QTabWidget, QDialog, QListWidgetItem, QMenu)
from PyQt6.QtGui import QCursor, QAction


class ProductDetailsDialog(QDialog):
    """Dialog to show product details"""

    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle(f"{product.name} Details")
        self.setGeometry(200, 200, 400, 250)

        layout = QVBoxLayout()

        # Product details
        name_label = QLabel(f"<h2>{product.name}</h2>")
        layout.addWidget(name_label)

        price_label = QLabel(f"<b>Price:</b> €{product.price:.2f}")
        layout.addWidget(price_label)

        desc_label = QLabel(f"<b>Description:</b> {product.description}")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        category_label = QLabel(f"<b>Category:</b> {product.category}")
        layout.addWidget(category_label)

        # Add to cart button
        add_button = QPushButton("Add to Cart")
        add_button.clicked.connect(self.accept)
        layout.addWidget(add_button)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, order_manager):
        super().__init__()
        self.order_manager = order_manager
        self.setWindowTitle("Order Interface")
        self.setGeometry(100, 100, 900, 700)

        # Main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # Left side - Products
        product_widget = QWidget()
        product_layout = QVBoxLayout(product_widget)

        # Create tabs for different product views
        self.tab_widget = QTabWidget()

        # Tab 1: All Products
        self.all_products_widget = QWidget()
        self.all_products_layout = QVBoxLayout(self.all_products_widget)
        self.create_product_grid(self.all_products_layout, self.order_manager.fetch_products())
        self.tab_widget.addTab(self.all_products_widget, "All Products")

        # Tab 2: Popular Products
        self.popular_widget = QWidget()
        self.popular_layout = QVBoxLayout(self.popular_widget)
        self.create_product_grid(self.popular_layout, self.order_manager.fetch_popular_products())
        self.tab_widget.addTab(self.popular_widget, "Popular Items")

        # Tab 3: Combo Meals
        self.combo_widget = QWidget()
        self.combo_layout = QVBoxLayout(self.combo_widget)
        self.create_product_grid(self.combo_layout, self.order_manager.fetch_combo_meals())
        self.tab_widget.addTab(self.combo_widget, "Combo Meals")

        product_layout.addWidget(self.tab_widget)

        # Right side - Cart
        cart_widget = QWidget()
        cart_layout = QVBoxLayout(cart_widget)

        cart_title = QLabel("Your Cart")
        cart_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        cart_layout.addWidget(cart_title)

        self.cart_list = QListWidget()
        self.cart_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.cart_list.customContextMenuRequested.connect(self.show_context_menu)
        cart_layout.addWidget(self.cart_list)

        # Remove item button
        self.remove_button = QPushButton("Remove Selected Item")
        self.remove_button.clicked.connect(self.remove_selected_item)
        cart_layout.addWidget(self.remove_button)

        self.total_label = QLabel("Total: €0.00")
        self.total_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        cart_layout.addWidget(self.total_label)

        self.checkout_button = QPushButton("Checkout")
        self.checkout_button.clicked.connect(self.checkout)
        self.checkout_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        cart_layout.addWidget(self.checkout_button)

        # Set the main layout with appropriate sizing
        main_layout.addWidget(product_widget, 3)  # 3/4 of width
        main_layout.addWidget(cart_widget, 1)  # 1/4 of width

        self.setCentralWidget(main_widget)

    def create_product_grid(self, parent_layout, products):
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(10)
        grid_layout.setHorizontalSpacing(10)

        for i, product in enumerate(products):
            # Create a product card widget
            product_widget = QWidget()
            product_widget.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 10px;")
            product_layout = QVBoxLayout(product_widget)

            # Product name and price
            name_label = QLabel(f"<b>{product.name}</b>")
            product_layout.addWidget(name_label)

            price_label = QLabel(f"€{product.price:.2f}")
            product_layout.addWidget(price_label)

            # View details button
            details_button = QPushButton("View Details")
            details_button.clicked.connect(lambda checked, p=product: self.show_product_details(p))
            product_layout.addWidget(details_button)

            # Add to cart button
            add_button = QPushButton("Add to Cart")
            add_button.clicked.connect(lambda checked, p=product: self.add_to_cart(p))
            product_layout.addWidget(add_button)

            grid_layout.addWidget(product_widget, i // 3, i % 3)

        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)

        parent_layout.addWidget(grid_widget)
        parent_layout.addStretch()

    def show_product_details(self, product):
        dialog = ProductDetailsDialog(product, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.add_to_cart(product)

    def add_to_cart(self, product):
        self.order_manager.add_to_order(product)
        item = QListWidgetItem(f"{product.name} - €{product.price:.2f}")
        # Store the product object with the item
        item.setData(Qt.ItemDataRole.UserRole, product)
        self.cart_list.addItem(item)
        self.update_total()

    def show_context_menu(self, position):
        if self.cart_list.count() > 0 and self.cart_list.currentItem():
            context_menu = QMenu()
            remove_action = QAction("Remove Item", self)
            remove_action.triggered.connect(self.remove_selected_item)
            context_menu.addAction(remove_action)
            context_menu.exec(QCursor.pos())

    def remove_selected_item(self):
        current_item = self.cart_list.currentItem()
        if current_item:
            # Get the product object from the item's data
            product = current_item.data(Qt.ItemDataRole.UserRole)
            self.order_manager.remove_from_order(product)
            self.cart_list.takeItem(self.cart_list.row(current_item))
            self.update_total()

    def update_total(self):
        total = self.order_manager.get_total()
        self.total_label.setText(f"Total: €{total:.2f}")

    def checkout(self):
        message = self.order_manager.checkout()
        QMessageBox.information(self, "Order", message)
        self.cart_list.clear()
        self.update_total()