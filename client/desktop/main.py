import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices, QFont, QIcon
from PyQt6.QtWidgets import QApplication, QMessageBox

from src.config import ICON_PATH, RELEASES_URL
from src.utils.gql import health_check
from src.utils.profile import profile_exists
from src.utils.theme import theme
from src.utils.version import current_version, update_available
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

    latest = update_available()
    if latest is not None:
        box = QMessageBox(
            QMessageBox.Icon.Information,
            "Доступно обновление",
            f"Вышла новая версия EatLog — {latest} "
            f"(у вас {current_version()}).\n"
            "Для продолжения работы необходимо скачать свежую версию.",
        )
        box.addButton("Скачать", QMessageBox.ButtonRole.AcceptRole)
        box.exec()
        QDesktopServices.openUrl(QUrl(RELEASES_URL))
        sys.exit(0)

    if not profile_exists():
        dialog = ProfileSetupDialog()
        if dialog.exec() != ProfileSetupDialog.DialogCode.Accepted:
            sys.exit(0)

    window = EatLogWindow()
    window.show()
    sys.exit(app.exec())
