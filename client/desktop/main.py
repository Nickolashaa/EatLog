import sys
from pathlib import Path

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMessageBox

from src.services.api.client import health_check
from src.services.profile import ProfileService
from src.widgets.profile_setup import ProfileSetupDialog
from src.widgets.window import EatLogWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Cantarell", 11))

    style_path = Path(__file__).parent / "src" / "widgets" / "style.qss"
    app.setStyleSheet(style_path.read_text())

    if not health_check():
        QMessageBox.critical(
            None,
            "Нет соединения",
            "Ведутся технические работы. Попробуйте позже.",
        )
        sys.exit(1)

    if not ProfileService.exists():
        dialog = ProfileSetupDialog()
        if dialog.exec() != ProfileSetupDialog.DialogCode.Accepted:
            sys.exit(0)

    window = EatLogWindow()
    window.show()
    sys.exit(app.exec())
