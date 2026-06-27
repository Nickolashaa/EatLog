from typing import cast

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import (
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from ...graphql.client import MealFilters, Meals
from ...utils.gql import client
from ...utils.worker import Worker
from ..header import Header
from ..table_utils import make_table, readonly
from .types import COLUMNS, FIXED_COLS


class MealTableWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._init_ui()
        self._load()

    def _init_ui(self) -> None:
        self.header = Header(parent=self, text="Блюда")

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Поиск...")
        self.search_input.textChanged.connect(lambda text: self._load(text.strip()))

        self.table = make_table(self, COLUMNS, FIXED_COLS)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        layout.addWidget(self.header)
        layout.addWidget(self.search_input)
        layout.addWidget(self.table, 1)

        self.setObjectName("MealTable")

    def showEvent(self, event: QShowEvent | None) -> None:
        super().showEvent(event)
        self._load(self.search_input.text().strip())

    def _load(self, query: str = "") -> None:
        self._load_worker = Worker(
            client.meals, filter_=MealFilters(searchQuery=query), limit=1000
        )
        self._load_worker.finished.connect(self._on_loaded)
        self._load_worker.failed.connect(self._on_error)
        self._load_worker.start()

    def _on_loaded(self, data: object) -> None:
        meals = cast(Meals, data).meals
        self.table.setRowCount(len(meals))
        for row, meal in enumerate(meals):
            self.table.setItem(row, 0, readonly(str(meal.id)))
            self.table.setItem(row, 1, readonly(meal.title))
            self.table.setItem(row, 2, readonly(str(meal.calories)))
            self.table.setItem(row, 3, readonly(str(meal.protein)))
            self.table.setItem(row, 4, readonly(str(meal.fat)))
            self.table.setItem(row, 5, readonly(str(meal.carbohydrate)))

    def _on_error(self, msg: str) -> None:
        QMessageBox.warning(self, "Ошибка", msg)
