from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QTableWidgetItem, QWidget


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
