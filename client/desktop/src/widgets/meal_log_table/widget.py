from datetime import date, datetime, timezone
from typing import cast

from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import (
    QDateEdit,
    QMessageBox,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ...services.meal_log import MealLogApiService, MealLogTableRow
from ...services.profile import ProfileService
from ...utils.worker import Worker
from ..header import Header
from ..table_utils import btn_cell, make_table, readonly
from .types import COLUMNS, FIXED_COLS


class MealLogTableWidget(QWidget):
    entry_deleted = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._rows: list[MealLogTableRow] = []
        self._init_ui()
        self._load()

    def _init_ui(self) -> None:
        self.header = Header(parent=self, text="Журнал")

        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(lambda _: self._load())

        self.table = make_table(self, COLUMNS, FIXED_COLS)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)
        layout.addWidget(self.header)
        layout.addWidget(self.date_edit)
        layout.addWidget(self.table, 1)

        self.setObjectName("MealLogTable")

    def showEvent(self, event: QShowEvent | None) -> None:
        super().showEvent(event)
        self._load()

    def _selected_date(self) -> date:
        qd = self.date_edit.date()
        return (
            datetime(
                year=qd.year(), month=qd.month(), day=qd.day(), hour=datetime.now().hour
            )
            .astimezone(timezone.utc)
            .date()
        )

    def _load(self) -> None:
        if not ProfileService.exists():
            return
        user_id = ProfileService.load()["uuid"]
        self._load_worker = Worker(
            MealLogApiService.get_table_list,
            user_id=user_id,
            date_filter=self._selected_date(),
        )
        self._load_worker.finished.connect(self._on_loaded)
        self._load_worker.failed.connect(self._on_error)
        self._load_worker.start()

    def _on_loaded(self, data: object) -> None:
        self._rows = cast(list[MealLogTableRow], data)
        self.table.setRowCount(len(self._rows))
        for row, r in enumerate(self._rows):
            self.table.setItem(row, 0, readonly(str(r["log_id"])))
            self.table.setItem(row, 1, readonly(r["meal_title"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(r["grams"])))
            self.table.setItem(row, 3, readonly(str(r["calories"])))
            self.table.setItem(row, 4, readonly(str(r["protein"])))
            self.table.setItem(row, 5, readonly(str(r["fat"])))
            self.table.setItem(row, 6, readonly(str(r["carbohydrate"])))
            self.table.setCellWidget(
                row,
                7,
                btn_cell(
                    lambda checked, i=row: self._on_save(i),
                    lambda checked, i=row: self._on_delete(i),
                ),
            )

    def _on_save(self, row: int) -> None:
        if row >= len(self._rows):
            return
        log_row = self._rows[row]
        grams_item = self.table.item(row, 2)
        if grams_item is None:
            return

        try:
            grams = float(grams_item.text().strip().replace(",", "."))
        except ValueError:
            return

        user_id = ProfileService.load()["uuid"]
        self._save_worker = Worker(
            MealLogApiService.update,
            log_id=log_row["log_id"],
            meal_id=log_row["meal_id"],
            grams=grams,
            user_id=user_id,
        )
        self._save_worker.finished.connect(lambda _: self._load())
        self._save_worker.failed.connect(self._on_error)
        self._save_worker.start()

    def _on_delete(self, row: int) -> None:
        if row >= len(self._rows):
            return
        log_id = self._rows[row]["log_id"]
        self._delete_worker = Worker(MealLogApiService.delete, log_id)
        self._delete_worker.finished.connect(self._on_deleted)
        self._delete_worker.failed.connect(self._on_error)
        self._delete_worker.start()

    def _on_deleted(self, _: object) -> None:
        self._load()
        self.entry_deleted.emit()

    def _on_error(self, msg: str) -> None:
        QMessageBox.warning(self, "Ошибка", msg)
