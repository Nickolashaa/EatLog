import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from src.widgets.window import EatLogWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Cantarell", 11))
    window = EatLogWindow()
    window.show()
    sys.exit(app.exec())
