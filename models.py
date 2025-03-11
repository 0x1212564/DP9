class Product:
    def __init__(self, product_id, name, price, description, category, popularity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.popularity = popularity

class Order:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)

    def remove_product(self, product):
        self.items.remove(product)

    def total_price(self):
        return sum(item.price for item in self.items)
