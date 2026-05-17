import sys
from pathlib import Path

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from src.widgets.window import EatLogWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Cantarell", 11))

    style_path = Path(__file__).parent / "src" / "widgets" / "style.qss"
    app.setStyleSheet(style_path.read_text())

    window = EatLogWindow()
    window.show()
    sys.exit(app.exec())
