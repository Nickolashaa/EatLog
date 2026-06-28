import sys

from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMessageBox

from src.config import ICON_PATH
from src.utils.gql import health_check
from src.utils.profile import profile_exists
from src.utils.theme import theme
from src.widgets.profile_setup import ProfileSetupDialog
from src.widgets.window import EatLogWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON_PATH))
    app.setFont(QFont("Cantarell", 11))

    app.setStyleSheet(theme.stylesheet)

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
