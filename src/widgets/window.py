from PyQt6.QtWidgets import QMainWindow, QTabWidget

from ..config import HEIGHT, TITLE, WIDTH
from .daily_report import DailyReport


class EatLog(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(TITLE)
        self.resize(WIDTH, HEIGHT)

        self.tabs = QTabWidget()
        self.tabs.addTab(
            DailyReport(parent=self),
            "Главная",
        )

        self.setCentralWidget(self.tabs)
