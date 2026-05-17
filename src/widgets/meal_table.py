from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..database.connection import session_maker
from ..services.meals import MealService
from ..services.meals.types import MealUpdateParams
from .header import Header

_COLUMNS = ["ID", "Название", "Калории", "Белки", "Жиры", "Углеводы", ""]
_FIXED_COLS = {0: 50, 2: 90, 3: 90, 4: 90, 5: 90, 6: 210}


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
        layout.addWidget(self.search_input)
        layout.addWidget(self.table, 1)

        self.setObjectName("MealTable")

    def showEvent(self, event: QShowEvent | None) -> None:
        super().showEvent(event)
        self._load(self.search_input.text().strip())

    def _load(self, query: str = "") -> None:
        with session_maker() as session:
            meals = MealService.get_list(session, query)
        self.table.setRowCount(len(meals))
        for row, meal in enumerate(meals):
            self.table.setItem(row, 0, _readonly(str(meal.id)))
            self.table.setItem(row, 1, QTableWidgetItem(meal.title))
            self.table.setItem(row, 2, QTableWidgetItem(str(meal.calories)))
            self.table.setItem(row, 3, QTableWidgetItem(str(meal.protein)))
            self.table.setItem(row, 4, QTableWidgetItem(str(meal.fat)))
            self.table.setItem(row, 5, QTableWidgetItem(str(meal.carbohydrate)))
            self.table.setCellWidget(
                row,
                6,
                _btn_cell(
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
            values: MealUpdateParams = {
                "title": title,
                "calories": float(cell(2).replace(",", ".")),
                "protein": float(cell(3).replace(",", ".")),
                "fat": float(cell(4).replace(",", ".")),
                "carbohydrate": float(cell(5).replace(",", ".")),
            }
        except ValueError:
            return

        try:
            with session_maker() as session:
                MealService.update(session, int(id_item.text()), values)
                session.commit()
        except Exception:
            return

    def _on_delete(self, row: int) -> None:
        id_item = self.table.item(row, 0)
        if id_item is None:
            return

        try:
            with session_maker() as session:
                MealService.delete(session, int(id_item.text()))
                session.commit()
        except Exception:
            return

        self._load(self.search_input.text().strip())
        self.meal_deleted.emit()
