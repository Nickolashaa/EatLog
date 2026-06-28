import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMessageBox

from src.utils.gql import health_check
from src.utils.profile import profile_exists
from src.widgets.profile_setup import ProfileSetupDialog
from src.widgets.style import STYLE
from src.widgets.window import EatLogWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Cantarell", 11))

    app.setStyleSheet(STYLE)

    if not health_check():
        QMessageBox.critical(
            None,
            "Нет соединения",
            "Ведутся технические работы. Попробуйте позже.",
        )
        sys.exit(1)

    if not profile_exists():
        dialog = ProfileSetupDialog()
        if dialog.exec() != ProfileSetupDialog.DialogCode.Accepted:
            sys.exit(0)

    window = EatLogWindow()
    window.show()
    sys.exit(app.exec())
