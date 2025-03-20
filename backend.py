from models import Product, Order


class OrderManager:
    def __init__(self):
        self.products = [
            Product(1, "Burger", 5.99, "A delicious beef burger with lettuce, tomato, and special sauce", "a la carte",
                    10),
            Product(2, "Pizza", 7.99, "Cheesy pepperoni pizza with a crispy crust", "a la carte", 15),
            Product(3, "Pasta", 6.99, "Creamy Alfredo pasta with garlic bread", "a la carte", 8),
            Product(4, "French Fries", 3.99, "Crispy golden fries with sea salt", "a la carte", 20),
            Product(5, "Salad", 4.99, "Fresh garden salad with vinaigrette", "a la carte", 5),
            Product(6, "Soda", 1.99, "Refreshing cola or lemon-lime soda", "a la carte", 18),
            Product(7, "Combo Meal 1", 10.99, "Burger, fries, and soda. Save €0.98 compared to buying separately!",
                    "combo", 12),
            Product(8, "Combo Meal 2", 12.99, "Pizza, salad, and drink. Save €1.98 compared to buying separately!",
                    "combo", 9),
            Product(9, "Family Combo", 19.99, "2 burgers, 2 fries, and 2 sodas. Great value for sharing!", "combo", 7)
        ]
        self.current_order = Order()

    def fetch_products(self):
        """Return all products"""
        return self.products

    def fetch_popular_products(self):
        """Return the most popular products based on popularity score"""
        return sorted(self.products, key=lambda x: x.popularity, reverse=True)[:5]

    def fetch_combo_meals(self):
        """Return all combo meal products"""
        return [p for p in self.products if p.category == 'combo']

    def fetch_a_la_carte(self):
        """Return all a la carte products"""
        return [p for p in self.products if p.category == 'a la carte']

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
            # Clear the cart after checkout
            order_items = self.current_order.get_item_count()
            self.current_order = Order()
            return f"Order confirmed! {order_items} items for €{order_total:.2f}"
        return "Your cart is empty!"