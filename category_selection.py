# ui/category_selection_widget.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QToolButton, QApplication, QHBoxLayout, QFrame
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize, pyqtSignal

class CategorySelectionWidget(QWidget):
    category_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("A la carte")
        self.setStyleSheet("background-color: #EFEFEF;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # HEADER
        header = QWidget()
        header.setStyleSheet("background-color: #FFFFFF;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)

        title = QLabel("A la carte")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold; color: #000000;")
        header_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)

        logo = QLabel()
        logo.setPixmap(QPixmap("assets/Logo.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        header_layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addWidget(header)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Plain)
        divider.setStyleSheet("color: #888888;")
        main_layout.addWidget(divider)

        # GRID OF BUTTONS
        grid = QGridLayout()
        grid.setContentsMargins(20, 20, 20, 20)
        grid.setSpacing(20)

        categories = [
            ("Burgers", "burger.png"),
            ("Taco's", "taco.png"),
            ("Salades", "salade.png"),
            ("Friet & sauzen", "fs.png"),
            ("Dranken", "dranken.png"),
            ("Desserts", "dessert.png"),
            ("Ontbijt (tot 11:00 uur)", "ontbijt.png"),
            ("Top 10 favorieten", "top10.png")
        ]

        row, col = 0, 0
        for name, filename in categories:
            btn = QToolButton()
            btn.setText(name)
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setFixedSize(150, 180)
            btn.setStyleSheet(f"""
                QToolButton {{
                    background-image: url("assets/{filename}");
                    background-position: center;
                    background-repeat: no-repeat;
                    background-size: cover;
                    border-radius: 75px;
                    color: #000;
                    font-size: 14px;
                    font-weight: bold;
                    padding-top: 150px;
                }}
                QToolButton:hover {{
                    background-color: #DDDDDD;
                }}
            """)
            btn.clicked.connect(lambda _, c=name: self.category_selected.emit(c))
            grid.addWidget(btn, row, col)
            col = (col + 1) % 2
            if col == 0:
                row += 1

        main_layout.addLayout(grid)
        self.resize(440, 650)

if __name__ == "__main__":
    app = QApplication([])
    widget = CategorySelectionWidget()
    widget.show()
    app.exec()