from models import Product, Order
from db_wrapper import DatabaseWrapper


class OrderManager:
    def __init__(self):
        self.db = DatabaseWrapper()
        # Setup database and insert initial products if needed
        self.db.setup_database()
        self.db.insert_initial_products()
        # Initialize empty order
        self.current_order = Order()

    def fetch_products(self):
        """Return all products"""
        return self.db.get_all_products()

    def fetch_products_by_category(self, category):
        """Return products filtered by category"""
        return self.db.get_products_by_category(category)

    def get_categories(self):
        """Return unique categories"""
        return self.db.get_categories()

    def fetch_popular_products(self):
        """Return the most popular products based on popularity score"""
        return self.db.get_popular_products(5)

    def fetch_combo_meals(self):
        """Return all combo meal products"""
        return self.db.get_products_by_category('combo')

    def fetch_a_la_carte(self):
        """Return all a la carte products"""
        return self.db.get_products_by_category('a la carte')

    def add_to_order(self, product):
        """Add a product to the current order"""
        self.current_order.add_product(product)

    def remove_from_order(self, product):
        """Remove a product from the current order"""
        self.current_order.remove_product(product)

    def get_total(self):
        """Calculate the total price of the current order"""
        return self.current_order.total_price()

    def checkout(self):
        """Process the checkout and return confirmation message"""
        order_total = self.get_total()
        if order_total > 0:
            # Save order to database
            order_id = self.db.save_order(self.current_order)
            order_items = self.current_order.get_item_count()
            # Clear the cart after checkout
            self.current_order = Order()
            return f"Order #{order_id} confirmed! {order_items} items for €{order_total:.2f}"
        return "Your cart is empty!"