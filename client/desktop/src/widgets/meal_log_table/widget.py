from datetime import date, datetime, timezone
from typing import cast
from uuid import UUID

from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import (
    QDateEdit,
    QMessageBox,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ...graphql.client import (
    MealLogFilter,
    MealLogs,
    MealLogsMealLogs,
    UpdateMealLogInput,
)
from ...utils.gql import client
from ...utils.nutrition import macros_for_log
from ...utils.profile import get_uuid, profile_exists
from ...utils.worker import Worker
from ..header import Header
from ..table_utils import btn_cell, make_table, readonly
from ..toast import show_toast
from .types import COLUMNS, FIXED_COLS


class MealLogTableWidget(QWidget):
    entry_deleted = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._logs: list[MealLogsMealLogs] = []
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
        if not profile_exists():
            return
        self._load_worker = Worker(
            client.meal_logs,
            filter_=MealLogFilter(
                userId=UUID(get_uuid()), dateFilter=self._selected_date()
            ),
            limit=1000,
        )
        self._load_worker.finished.connect(self._on_loaded)
        self._load_worker.failed.connect(self._on_error)
        self._load_worker.start()

    def _on_loaded(self, data: object) -> None:
        self._logs = cast(MealLogs, data).meal_logs
        self.table.setRowCount(len(self._logs))
        for row, log in enumerate(self._logs):
            macros = macros_for_log(log)
            self.table.setItem(row, 0, readonly(str(log.id)))
            self.table.setItem(row, 1, readonly(log.meal.title))
            self.table.setItem(row, 2, QTableWidgetItem(str(log.grams)))
            self.table.setItem(row, 3, readonly(str(round(macros["calories"], 1))))
            self.table.setItem(row, 4, readonly(str(round(macros["protein"], 1))))
            self.table.setItem(row, 5, readonly(str(round(macros["fat"], 1))))
            self.table.setItem(row, 6, readonly(str(round(macros["carbohydrate"], 1))))
            self.table.setCellWidget(
                row,
                7,
                btn_cell(
                    lambda checked, i=row: self._on_save(i),
                    lambda checked, i=row: self._on_delete(i),
                ),
            )

    def _on_save(self, row: int) -> None:
        if row >= len(self._logs):
            return
        log = self._logs[row]
        grams_item = self.table.item(row, 2)
        if grams_item is None:
            return

        try:
            grams = float(grams_item.text().strip().replace(",", "."))
        except ValueError:
            return

        self._save_worker = Worker(
            client.update_meal_log,
            id=log.id,
            input=UpdateMealLogInput(grams=grams),
        )
        self._save_worker.finished.connect(self._on_saved)
        self._save_worker.failed.connect(self._on_error)
        self._save_worker.start()

    def _on_saved(self, _: object) -> None:
        self._load()
        show_toast(self, "Изменения сохранены")

    def _on_delete(self, row: int) -> None:
        if row >= len(self._logs):
            return
        self._delete_worker = Worker(client.delete_meal_log, self._logs[row].id)
        self._delete_worker.finished.connect(self._on_deleted)
        self._delete_worker.failed.connect(self._on_error)
        self._delete_worker.start()

    def _on_deleted(self, _: object) -> None:
        self._load()
        self.entry_deleted.emit()
        show_toast(self, "Запись удалена")

    def _on_error(self, msg: str) -> None:
        QMessageBox.warning(self, "Ошибка", msg)
