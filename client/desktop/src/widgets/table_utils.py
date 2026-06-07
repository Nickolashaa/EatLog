from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)


def readonly(text: str) -> QTableWidgetItem:
    item = QTableWidgetItem(text)
    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    return item


def btn_cell(save_cb: object, del_cb: object) -> QWidget:
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


def make_table(
    parent: QWidget,
    columns: list[str],
    fixed_cols: dict[int, int],
) -> QTableWidget:
    table = QTableWidget(0, len(columns), parent)
    table.setHorizontalHeaderLabels(columns)

    h = table.horizontalHeader()
    assert h is not None
    h.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
    for col, width in fixed_cols.items():
        h.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(col, width)

    v = table.verticalHeader()
    assert v is not None
    v.setVisible(False)
    v.setDefaultSectionSize(40)

    table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
    table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
    table.setShowGrid(False)
    return table
