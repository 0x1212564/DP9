from PyQt6.QtWidgets import QApplication, QStyleFactory
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from ui import MainWindow
from backend import OrderManager
import sys

# Initialize order manager
order_manager = OrderManager()


# Main function to run the application
def main():
    app = QApplication(sys.argv)
    
    # Set application style to white theme
    app.setStyle("Fusion")
    
    # Create a white palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(0, 0, 0))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(200, 200, 200))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
    
    app.setPalette(palette)

    # Create and show the main window
    window = MainWindow(order_manager)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()