from typing import cast

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import (
    QLineEdit,
    QMessageBox,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ...services.meals import MealApiService, MealData, MealInput
from ...utils.worker import Worker
from ..header import Header
from ..table_utils import btn_cell, make_table, readonly
from .types import COLUMNS, FIXED_COLS


class MealTableWidget(QWidget):
    meal_deleted = pyqtSignal()

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
        self._load_worker = Worker(MealApiService.get_list, search=query)
        self._load_worker.finished.connect(self._on_loaded)
        self._load_worker.failed.connect(self._on_error)
        self._load_worker.start()

    def _on_loaded(self, data: object) -> None:
        meals = cast(list[MealData], data)
        self.table.setRowCount(len(meals))
        for row, meal in enumerate(meals):
            self.table.setItem(row, 0, readonly(str(meal["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(meal["title"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(meal["calories"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(meal["protein"])))
            self.table.setItem(row, 4, QTableWidgetItem(str(meal["fat"])))
            self.table.setItem(row, 5, QTableWidgetItem(str(meal["carbohydrate"])))
            self.table.setCellWidget(
                row,
                6,
                btn_cell(
                    lambda checked, r=row: self._on_save(r),
                    lambda checked, r=row: self._on_delete(r),
                ),
            )

    def _on_save(self, row: int) -> None:
        id_item = self.table.item(row, 0)
        if id_item is None:
            return

        def cell(col: int) -> str:
            item = self.table.item(row, col)
            return item.text().strip() if item else ""

        title = cell(1)
        if not title:
            return

        try:
            data: MealInput = {
                "title": title,
                "calories": float(cell(2).replace(",", ".")),
                "protein": float(cell(3).replace(",", ".")),
                "fat": float(cell(4).replace(",", ".")),
                "carbohydrate": float(cell(5).replace(",", ".")),
            }
        except ValueError:
            return

        self._save_worker = Worker(
            MealApiService.update, meal_id=int(id_item.text()), data=data
        )
        self._save_worker.failed.connect(self._on_error)
        self._save_worker.start()

    def _on_delete(self, row: int) -> None:
        id_item = self.table.item(row, 0)
        if id_item is None:
            return

        meal_id = int(id_item.text())
        self._delete_worker = Worker(MealApiService.delete, meal_id)
        self._delete_worker.finished.connect(self._on_deleted)
        self._delete_worker.failed.connect(self._on_error)
        self._delete_worker.start()

    def _on_deleted(self, _: object) -> None:
        self._load(self.search_input.text().strip())
        self.meal_deleted.emit()

    def _on_error(self, msg: str) -> None:
        QMessageBox.warning(self, "Ошибка", msg)
