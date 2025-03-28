import mysql.connector
from models import Product

class DatabaseWrapper:
    """MySQL database wrapper for the ordering system"""
    
    def __init__(self, host="localhost", user="root", password="", database="dp9_restaurant"):
        """Initialize database connection"""
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish connection to the database"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            return False
            
    def disconnect(self):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            
    def setup_database(self):
        """Create tables if they don't exist"""
        try:
            self.connect()
            
            # Create products table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    description TEXT,
                    category VARCHAR(50),
                    popularity INT DEFAULT 0
                )
            """)
            
            # Create orders table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    order_id INT PRIMARY KEY AUTO_INCREMENT,
                    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_price DECIMAL(10, 2),
                    status VARCHAR(20) DEFAULT 'pending'
                )
            """)
            
            # Create order_items table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    item_id INT PRIMARY KEY AUTO_INCREMENT,
                    order_id INT,
                    product_id INT,
                    quantity INT DEFAULT 1,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            """)
            
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error setting up database: {err}")
            return False
        finally:
            self.disconnect()
            
    def insert_initial_products(self):
        """Insert initial products if the products table is empty"""
        try:
            self.connect()
            
            # Check if products table is empty
            self.cursor.execute("SELECT COUNT(*) as count FROM products")
            result = self.cursor.fetchone()
            
            if result['count'] == 0:
                # Insert initial products
                products = [
                    (1, "Classic Burger", 5.99, "Juicy beef patty with lettuce, tomato, and house sauce", "burgers", 10),
                    (2, "Cheese Burger", 6.99, "Classic burger topped with melted cheddar cheese", "burgers", 12),
                    (3, "Street Taco", 3.99, "Authentic corn tortilla with seasoned beef and cilantro", "tacos", 15),
                    (4, "Fish Taco", 4.99, "Crispy fish taco with cabbage slaw and lime crema", "tacos", 8),
                    (5, "Caesar Salad", 4.99, "Crisp romaine, parmesan, croutons with caesar dressing", "salads", 7),
                    (6, "Garden Salad", 4.49, "Mixed greens with fresh vegetables and vinaigrette", "salads", 5),
                    (7, "Classic Fries", 2.99, "Golden crispy fries with sea salt", "fries", 20),
                    (8, "Loaded Fries", 4.99, "Fries topped with cheese, bacon, and green onions", "fries", 15),
                    (9, "Fountain Drink", 1.99, "Choice of soda or iced tea", "drinks", 18),
                    (10, "Milkshake", 3.99, "Creamy vanilla or chocolate shake with whipped cream", "drinks", 12),
                    (11, "Chocolate Cake", 4.99, "Rich chocolate layer cake with fudge frosting", "desserts", 9),
                    (12, "Ice Cream Sundae", 3.99, "Vanilla ice cream with choice of toppings", "desserts", 8)
                ]
                
                insert_query = """
                    INSERT INTO products (product_id, name, price, description, category, popularity)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                self.cursor.executemany(insert_query, products)
                self.connection.commit()
                return True
            return True
        except mysql.connector.Error as err:
            print(f"Error inserting initial products: {err}")
            return False
        finally:
            self.disconnect()
            
    def get_all_products(self):
        """Fetch all products from the database"""
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM products")
            products_data = self.cursor.fetchall()
            
            products = []
            for p in products_data:
                product = Product(
                    p['product_id'],
                    p['name'],
                    float(p['price']),
                    p['description'],
                    p['category'],
                    p['popularity']
                )
                products.append(product)
                
            return products
        except mysql.connector.Error as err:
            print(f"Error fetching products: {err}")
            return []
        finally:
            self.disconnect()
            
    def get_products_by_category(self, category):
        """Fetch products filtered by category"""
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM products WHERE category = %s", (category,))
            products_data = self.cursor.fetchall()
            
            products = []
            for p in products_data:
                product = Product(
                    p['product_id'],
                    p['name'],
                    float(p['price']),
                    p['description'],
                    p['category'],
                    p['popularity']
                )
                products.append(product)
                
            return products
        except mysql.connector.Error as err:
            print(f"Error fetching products by category: {err}")
            return []
        finally:
            self.disconnect()
            
    def get_popular_products(self, limit=5):
        """Fetch most popular products"""
        try:
            self.connect()
            self.cursor.execute("SELECT * FROM products ORDER BY popularity DESC LIMIT %s", (limit,))
            products_data = self.cursor.fetchall()
            
            products = []
            for p in products_data:
                product = Product(
                    p['product_id'],
                    p['name'],
                    float(p['price']),
                    p['description'],
                    p['category'],
                    p['popularity']
                )
                products.append(product)
                
            return products
        except mysql.connector.Error as err:
            print(f"Error fetching popular products: {err}")
            return []
        finally:
            self.disconnect()
            
    def get_categories(self):
        """Fetch all unique categories"""
        try:
            self.connect()
            self.cursor.execute("SELECT DISTINCT category FROM products ORDER BY category")
            categories = [row['category'] for row in self.cursor.fetchall()]
            return categories
        except mysql.connector.Error as err:
            print(f"Error fetching categories: {err}")
            return []
        finally:
            self.disconnect()
            
    def save_order(self, order):
        """Save an order to the database"""
        try:
            self.connect()
            
            # Insert order
            self.cursor.execute(
                "INSERT INTO orders (total_price) VALUES (%s)",
                (order.total_price(),)
            )
            
            order_id = self.cursor.lastrowid
            
            # Insert order items
            for item in order.items:
                self.cursor.execute(
                    "INSERT INTO order_items (order_id, product_id) VALUES (%s, %s)",
                    (order_id, item.product_id)
                )
                
            self.connection.commit()
            return order_id
        except mysql.connector.Error as err:
            print(f"Error saving order: {err}")
            if self.connection:
                self.connection.rollback()
            return None
        finally:
            self.disconnect()