from datetime import date

from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDateEdit,
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..database.connection import session_maker
from ..services.meal_log import MealLogService, MealLogTableRow
from ..services.meal_log.types import MealLogUpdateParams
from .header import Header

_COLUMNS = ["ID", "Блюдо", "Граммы", "Калории", "Белки", "Жиры", "Углеводы", ""]
_FIXED_COLS = {0: 45, 2: 80, 3: 90, 4: 80, 5: 75, 6: 95, 7: 200}


def _readonly(text: str) -> QTableWidgetItem:
    item = QTableWidgetItem(text)
    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    return item


def _btn_cell(save_cb: object, del_cb: object) -> QWidget:
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(4, 4, 4, 4)
    layout.setSpacing(6)

    save_btn = QPushButton("Сохранить")
    save_btn.setObjectName("SaveBtn")
    del_btn = QPushButton("Удалить")
    del_btn.setObjectName("DeleteBtn")

    layout.addWidget(save_btn)
    layout.addWidget(del_btn)

    save_btn.clicked.connect(save_cb)  # type: ignore[arg-type]
    del_btn.clicked.connect(del_cb)  # type: ignore[arg-type]

    return container


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

        self.table = QTableWidget(0, len(_COLUMNS), self)
        self.table.setHorizontalHeaderLabels(_COLUMNS)

        h = self.table.horizontalHeader()
        assert h is not None
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        for col in _FIXED_COLS:
            h.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        for col, width in _FIXED_COLS.items():
            self.table.setColumnWidth(col, width)

        v = self.table.verticalHeader()
        assert v is not None
        v.setVisible(False)
        v.setDefaultSectionSize(40)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setShowGrid(False)

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
        return date(qd.year(), qd.month(), qd.day())

    def _load(self) -> None:
        with session_maker() as session:
            self._rows = MealLogService.get_table_list(
                session, date_filter=self._selected_date()
            )

        self.table.setRowCount(len(self._rows))
        for row, r in enumerate(self._rows):
            self.table.setItem(row, 0, _readonly(str(r["log_id"])))
            self.table.setItem(row, 1, _readonly(r["meal_title"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(r["grams"])))
            self.table.setItem(row, 3, _readonly(str(r["calories"])))
            self.table.setItem(row, 4, _readonly(str(r["protein"])))
            self.table.setItem(row, 5, _readonly(str(r["fat"])))
            self.table.setItem(row, 6, _readonly(str(r["carbohydrate"])))
            self.table.setCellWidget(
                row,
                7,
                _btn_cell(
                    lambda checked, i=row: self._on_save(i),
                    lambda checked, i=row: self._on_delete(i),
                ),
            )

    def _on_save(self, row: int) -> None:
        id_item = self.table.item(row, 0)
        grams_item = self.table.item(row, 2)
        if id_item is None or grams_item is None:
            return

        try:
            values: MealLogUpdateParams = {
                "grams": float(grams_item.text().strip().replace(",", "."))
            }
        except ValueError:
            return

        try:
            with session_maker() as session:
                MealLogService.update(session, int(id_item.text()), values)
                session.commit()
        except Exception:
            return

        self._load()

    def _on_delete(self, row: int) -> None:
        id_item = self.table.item(row, 0)
        if id_item is None:
            return

        try:
            with session_maker() as session:
                MealLogService.delete(session, int(id_item.text()))
                session.commit()
        except Exception:
            return

        self._load()
        self.entry_deleted.emit()
