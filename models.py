class Product:
    def __init__(self, product_id, name, price, description, category, popularity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.popularity = popularity


    def __str__(self):
        return f"{self.name} (€{self.price:.2f})"

    def __eq__(self, other):
        if not isinstance(other, Product):
            return False
        return self.product_id == other.product_id


class Order:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        """Add a product to the order"""
        self.items.append(product)

    def remove_product(self, product):
        """Remove a product from the order by matching product_id"""
        # Find the index of the first matching product
        for i, item in enumerate(self.items):
            if item.product_id == product.product_id:
                self.items.pop(i)
                break

    def total_price(self):
        """Calculate the total price of all items in the order"""
        return sum(item.price for item in self.items)

    def get_item_count(self):
        """Return the number of items in the order"""
        return len(self.items)

    def clear(self):
        """Remove all items from the order"""
        self.items = []