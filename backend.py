from models import Product, Order

class OrderManager:
    def __init__(self):
        self.products = [
            Product(1, "Burger", 5.99, "A delicious beef burger", "a la carte", 10),
            Product(2, "Pizza", 7.99, "Cheesy pepperoni pizza", "a la carte", 15),
            Product(3, "Pasta", 6.99, "Creamy Alfredo pasta", "a la carte", 8),
            Product(4, "Combo Meal 1", 10.99, "Burger, fries, and soda", "combo", 12),
            Product(5, "Combo Meal 2", 12.99, "Pizza, salad, and drink", "combo", 9)
        ]
        self.current_order = Order()

    def fetch_products(self):
        return self.products

    def fetch_popular_products(self):
        return sorted(self.products, key=lambda x: x.popularity, reverse=True)[:5]

    def fetch_combo_meals(self):
        return [p for p in self.products if p.category == 'combo']

    def add_to_order(self, product):
        self.current_order.add_product(product)

    def remove_from_order(self, product):
        self.current_order.remove_product(product)

    def get_total(self):
        return self.current_order.total_price()

    def checkout(self):
        order_total = self.get_total()
        if order_total > 0:
            return f"Order confirmed! Total: €{order_total:.2f}"
        return "Your cart is empty!"