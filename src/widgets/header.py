from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget


class Header(QLabel):
    def __init__(self, parent: QWidget, text: str) -> None:
        super().__init__(text, parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName("Header")
