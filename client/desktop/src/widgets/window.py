from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QTabWidget, QWidget

from ..config import HEIGHT, TITLE, WIDTH
from .daily_report import DailyReport
from .meal_log_table import MealLogTableWidget
from .meal_search import MealSearch
from .meal_table import MealTableWidget
from .settings import SettingsWidget


class EatLogWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(TITLE)
        self.resize(WIDTH, HEIGHT)

        meal_search = MealSearch()
        daily_report = DailyReport(parent=self)

        meal_search.meal_added.connect(daily_report.refresh)

        home_widget = QWidget()
        home_layout = QHBoxLayout(home_widget)
        home_layout.setContentsMargins(0, 0, 0, 0)
        home_layout.setSpacing(0)
        home_layout.addWidget(meal_search, 1)
        home_layout.addWidget(daily_report, 1)

        meal_log_table = MealLogTableWidget()
        meal_table = MealTableWidget()

        meal_log_table.entry_deleted.connect(daily_report.refresh)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        tab_bar = self.tabs.tabBar()
        if tab_bar is not None:
            tab_bar.setExpanding(True)
        self.tabs.addTab(home_widget, "🏠  Главная")
        self.tabs.addTab(meal_table, "🍽  Блюда")
        self.tabs.addTab(meal_log_table, "📖  Журнал")
        self.tabs.addTab(SettingsWidget(), "⚙  Настройки")

        self.setCentralWidget(self.tabs)
