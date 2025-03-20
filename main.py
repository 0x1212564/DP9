from PyQt6.QtWidgets import QApplication
from ui import MainWindow
from backend import OrderManager
import sys

# Initialize order manager
order_manager = OrderManager()


# Main function to run the application
def main():
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Create and show the main window
    window = MainWindow(order_manager)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()