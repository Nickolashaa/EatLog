import sys

from PyQt6.QtWidgets import QApplication

from src.widgets.window import EatLogWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EatLogWindow()
    window.show()
    sys.exit(app.exec())
