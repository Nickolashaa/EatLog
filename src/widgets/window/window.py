from PyQt6.QtWidgets import QMainWindow, QTabWidget

from ...config import HEIGHT, TITLE, WIDTH
from ..daily_report import DailyReport
from ..utils import load_style


class EatLogWindow(QMainWindow):
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
        self.setStyleSheet(load_style(__file__))
