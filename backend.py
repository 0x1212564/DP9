from models import Product, Order


class OrderManager:
    def __init__(self):
        self.products = [
            Product(1, "Classic Burger", 5.99, "Juicy beef patty with lettuce, tomato, and house sauce", "burgers", 10),
            Product(2, "Cheese Burger", 6.99, "Classic burger topped with melted cheddar cheese", "burgers", 12),
            Product(3, "Street Taco", 3.99, "Authentic corn tortilla with seasoned beef and cilantro", "tacos", 15),
            Product(4, "Fish Taco", 4.99, "Crispy fish taco with cabbage slaw and lime crema", "tacos", 8),
            Product(5, "Caesar Salad", 4.99, "Crisp romaine, parmesan, croutons with caesar dressing", "salads", 7),
            Product(6, "Garden Salad", 4.49, "Mixed greens with fresh vegetables and vinaigrette", "salads", 5),
            Product(7, "Classic Fries", 2.99, "Golden crispy fries with sea salt", "fries", 20),
            Product(8, "Loaded Fries", 4.99, "Fries topped with cheese, bacon, and green onions", "fries", 15),
            Product(9, "Fountain Drink", 1.99, "Choice of soda or iced tea", "drinks", 18),
            Product(10, "Milkshake", 3.99, "Creamy vanilla or chocolate shake with whipped cream", "drinks", 12),
            Product(11, "Chocolate Cake", 4.99, "Rich chocolate layer cake with fudge frosting", "desserts", 9),
            Product(12, "Ice Cream Sundae", 3.99, "Vanilla ice cream with choice of toppings", "desserts", 8)
        ]
        self.current_order = Order()

    def fetch_products(self):
        """Return all products"""
        return self.products

    def fetch_products_by_category(self, category):
        """Return products filtered by category"""
        return [p for p in self.products if p.category == category]

    def get_categories(self):
        """Return unique categories"""
        return sorted(set(p.category for p in self.products))

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