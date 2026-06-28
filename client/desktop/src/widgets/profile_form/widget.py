from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...graphql.client import UserFields
from .types import GENDER_OPTIONS, GOAL_OPTIONS, ProfileFormValues


class ProfileForm(QWidget):
    saved = pyqtSignal(object)

    def __init__(
        self,
        parent: QWidget | None = None,
        button_text: str = "Сохранить",
    ) -> None:
        super().__init__(parent=parent)
        self._init_ui(button_text)

    def _init_ui(self, button_text: str) -> None:
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")

        self.gender_combo = QComboBox()
        for label, _ in GENDER_OPTIONS:
            self.gender_combo.addItem(label)

        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("70")
        self.weight_input.setValidator(QDoubleValidator(20.0, 300.0, 1))

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("175")
        self.height_input.setValidator(QDoubleValidator(100.0, 250.0, 1))

        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("25")
        self.age_input.setValidator(QIntValidator(10, 120))

        self.goal_combo = QComboBox()
        for label, _ in GOAL_OPTIONS:
            self.goal_combo.addItem(label)

        form = QFormLayout()
        form.setSpacing(14)
        form.setContentsMargins(0, 0, 0, 0)
        form.addRow("Имя:", self.name_input)
        form.addRow("Пол:", self.gender_combo)
        form.addRow("Вес (кг):", self.weight_input)
        form.addRow("Рост (см):", self.height_input)
        form.addRow("Возраст:", self.age_input)
        form.addRow("Цель:", self.goal_combo)

        self.save_btn = QPushButton(button_text)
        self.save_btn.clicked.connect(self._on_save)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        layout.addLayout(form)
        layout.addWidget(self.save_btn)

    def load(self, user: UserFields) -> None:
        self.name_input.setText(user.name)
        gender_idx = next(
            (i for i, (_, v) in enumerate(GENDER_OPTIONS) if v == user.gender),
            0,
        )
        self.gender_combo.setCurrentIndex(gender_idx)
        self.weight_input.setText(str(user.weight))
        self.height_input.setText(str(user.height))
        self.age_input.setText(str(user.age))
        goal_idx = next(
            (i for i, (_, v) in enumerate(GOAL_OPTIONS) if v == user.goal),
            0,
        )
        self.goal_combo.setCurrentIndex(goal_idx)

    def get_values(self) -> ProfileFormValues | None:
        name = self.name_input.text().strip()
        weight_text = self.weight_input.text().strip().replace(",", ".")
        height_text = self.height_input.text().strip().replace(",", ".")
        age_text = self.age_input.text().strip()

        if not (name and weight_text and height_text and age_text):
            return None

        try:
            weight = float(weight_text)
            height = float(height_text)
            age = int(age_text)
        except ValueError:
            return None

        gender = GENDER_OPTIONS[self.gender_combo.currentIndex()][1]
        goal = GOAL_OPTIONS[self.goal_combo.currentIndex()][1]

        return {
            "name": name,
            "gender": gender,
            "weight": weight,
            "height": height,
            "age": age,
            "goal": goal,
        }

    def _on_save(self) -> None:
        values = self.get_values()
        if values is not None:
            self.saved.emit(values)
