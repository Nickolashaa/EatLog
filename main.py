import sys

from PyQt6.QtWidgets import QApplication

from src.main import EatLog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EatLog()
    window.show()
    sys.exit(app.exec())
