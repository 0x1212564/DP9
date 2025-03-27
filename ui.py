# Update imports to include QToolButton and QSize
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QListWidget, QMessageBox,
                            QGridLayout, QHBoxLayout, QTabWidget, QDialog, QListWidgetItem, QMenu, QScrollArea, QToolButton)
from PyQt6.QtGui import QCursor, QAction, QIcon, QPixmap


class ProductDetailsDialog(QDialog):
    """Dialog to show product details"""

    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product = product
        self.setWindowTitle(f"{product.name} Details")
        self.setGeometry(200, 200, 400, 250)

        layout = QVBoxLayout()

        """ Product details"""
        name_label = QLabel(f"<h2>{product.name}</h2>")
        layout.addWidget(name_label)

        price_label = QLabel(f"<b>Price:</b> €{product.price:.2f}")
        layout.addWidget(price_label)

        desc_label = QLabel(f"<b>Description:</b> {product.description}")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        category_label = QLabel(f"<b>Category:</b> {product.category}")
        layout.addWidget(category_label)

        """Add to cart button"""
        add_button = QPushButton("Add to Cart")
        add_button.clicked.connect(self.accept)
        layout.addWidget(add_button)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, order_manager):
        super().__init__()
        self.order_manager = order_manager
        self.setWindowTitle("Order Interface")
        self.setGeometry(100, 100, 1200, 800)

        # Replace emoji icons with image filenames
        self.category_images = {
            "popular": "top10.png",
            "burgers": "burger.png",
            "tacos": "taco.png",
            "salads": "salade.png",
            "fries": "fs.png",
            "drinks": "dranken.png",
            "desserts": "dessert.png"
        }

        """Main layout"""
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        """Left side - Categories and Products"""
        left_widget = QWidget()
        left_layout = QHBoxLayout(left_widget)  # Changed to HBoxLayout

        """Categories section - Now on the left"""
        categories_widget = QWidget()
        categories_layout = QVBoxLayout(categories_widget)  # Changed to VBoxLayout
        categories_layout.setSpacing(10)

        """Create category buttons with images instead of emojis"""
        for category, image_file in self.category_images.items():
            # Use QToolButton which supports text under icon
            category_button = QToolButton()
            category_button.setMinimumSize(100, 100)
            
            # Set icon from image file
            icon = QIcon(f"assets/{image_file}")
            category_button.setIcon(icon)
            category_button.setIconSize(QSize(60, 60))
            
            # Set text below icon
            category_button.setText(category.capitalize())
            category_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            
            category_button.setStyleSheet("""
                QToolButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 14px;
                }
                QToolButton:hover {
                    background-color: rgba(240, 240, 240, 0.5);
                }
                QToolButton:pressed {
                    background-color: rgba(224, 224, 224, 0.7);
                }
            """)
            category_button.clicked.connect(lambda checked, cat=category: self.show_category_products(cat))
            categories_layout.addWidget(category_button)

        """Products section - Now on the right of categories"""
        products_container = QWidget()
        products_container_layout = QVBoxLayout(products_container)
        
        self.products_widget = QWidget()
        self.products_layout = QVBoxLayout(self.products_widget)

        scroll = QScrollArea()
        scroll.setWidget(self.products_widget)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        products_container_layout.addWidget(scroll)

        """Add both sections to the left layout"""
        left_layout.addWidget(categories_widget, 1)  # Categories take 1 part
        left_layout.addWidget(products_container, 4)  # Products take 4 parts

        """Right side - Cart"""
        cart_widget = QWidget()
        cart_layout = QVBoxLayout(cart_widget)

        cart_title = QLabel("Your Cart")
        cart_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        cart_layout.addWidget(cart_title)

        self.cart_list = QListWidget()
        self.cart_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.cart_list.customContextMenuRequested.connect(self.show_context_menu)
        cart_layout.addWidget(self.cart_list)

        """Remove item button"""
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

        """Set the main layout with appropriate sizing"""
        main_layout.addWidget(left_widget, 3)
        main_layout.addWidget(cart_widget, 1)

        self.setCentralWidget(main_widget)
        
        """Show popular items by default"""
        self.show_category_products("popular")

    def show_category_products(self, category):
        """Clear existing products"""
        for i in reversed(range(self.products_layout.count())):
            item = self.products_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)
            else:
                self.products_layout.removeItem(item)

        """Get products for the selected category"""
        if category == "popular":
            products = self.order_manager.fetch_popular_products()
        else:
            products = self.order_manager.fetch_products_by_category(category)

        """Create product grid"""
        self.create_product_grid(self.products_layout, products)

    def create_product_grid(self, parent_layout, products):
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(10)
        grid_layout.setHorizontalSpacing(10)

        for i, product in enumerate(products):
            """Create a product card widget"""
            product_widget = QWidget()
            product_layout = QVBoxLayout(product_widget)

            """Product name and price"""
            name_label = QLabel(f"<b>{product.name}</b>")
            product_layout.addWidget(name_label)

            price_label = QLabel(f"€{product.price:.2f}")
            product_layout.addWidget(price_label)

            """View details button"""
            details_button = QPushButton("View Details")
            details_button.clicked.connect(lambda checked, p=product: self.show_product_details(p))
            product_layout.addWidget(details_button)

            """Add to cart button"""
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
        """Store the product object with the item"""
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
            """Get the product object from the item's data"""
            product = current_item.data(Qt.ItemDataRole.UserRole)
            self.order_manager.remove_from_order(product)
            self.cart_list.takeItem(self.cart_list.row(current_item))
            self.update_total()

    def update_total(self):
        total = self.order_manager.get_total()
        self.total_label.setText(f"Total: €{total:.2f}")

    def checkout(self):
        """Popup window for payment method selection"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Payment Method")
        dialog.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        label = QLabel("Choose a payment method:")
        layout.addWidget(label)

        button_layout = QHBoxLayout()

        card_button = QPushButton("Card")
        card_button.clicked.connect(lambda: self.process_payment(dialog, "Card"))
        button_layout.addWidget(card_button)

        cash_button = QPushButton("Cash")
        cash_button.clicked.connect(lambda: self.process_payment(dialog, "Cash"))
        button_layout.addWidget(cash_button)

        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        dialog.exec()

    def process_payment(self, dialog, method):
        message = self.order_manager.checkout()
        dialog.accept()  # Close the payment dialog
        QMessageBox.information(self, "Order", message)
        self.cart_list.clear()
        self.update_total()