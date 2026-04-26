from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from ..flask_loader import FlaskLoader
from ..header import Header
from ..utils import load_style


class DailyReport(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.init_ui()

    def init_ui(self) -> None:
        self.header = Header(parent=self, text="Ежедневный отчет")

        self.mid_layout = QHBoxLayout()
        self.protein_flask = FlaskLoader(self)
        self.fat_flask = FlaskLoader(self)
        self.carbohydrate_flask = FlaskLoader(self)
        self.mid_layout.addWidget(self.protein_flask)
        self.mid_layout.addWidget(self.fat_flask)
        self.mid_layout.addWidget(self.carbohydrate_flask)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.header)
        self.main_layout.addLayout(self.mid_layout)
        self.setLayout(self.main_layout)

        self.setObjectName("DailyReport")
        self.setStyleSheet(load_style(__file__))
