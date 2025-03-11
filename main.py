from PyQt5.QtWidgets import QApplication
from ui import MainWindow
from backend import OrderManager
import sys

# Initialize order manager
order_manager = OrderManager()

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = MainWindow(order_manager)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
