from typing import Literal

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

from ..services.profile.types import ProfileBase

_GENDER_OPTIONS: list[tuple[str, Literal["male", "female"]]] = [
    ("Мужской", "male"),
    ("Женский", "female"),
]

_GOAL_OPTIONS: list[tuple[str, Literal["maintain", "lose", "gain"]]] = [
    ("Поддержание веса", "maintain"),
    ("Похудение", "lose"),
    ("Набор мышечной массы", "gain"),
]


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
        self.gender_combo = QComboBox()
        for label, _ in _GENDER_OPTIONS:
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
        for label, _ in _GOAL_OPTIONS:
            self.goal_combo.addItem(label)

        form = QFormLayout()
        form.setSpacing(14)
        form.setContentsMargins(0, 0, 0, 0)
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

    def load(self, profile: ProfileBase) -> None:
        gender_idx = next(
            (i for i, (_, v) in enumerate(_GENDER_OPTIONS) if v == profile["gender"]),
            0,
        )
        self.gender_combo.setCurrentIndex(gender_idx)
        self.weight_input.setText(str(profile["weight"]))
        self.height_input.setText(str(profile["height"]))
        self.age_input.setText(str(profile["age"]))
        goal_idx = next(
            (i for i, (_, v) in enumerate(_GOAL_OPTIONS) if v == profile["goal"]),
            0,
        )
        self.goal_combo.setCurrentIndex(goal_idx)

    def get_values(self) -> ProfileBase | None:
        weight_text = self.weight_input.text().strip().replace(",", ".")
        height_text = self.height_input.text().strip().replace(",", ".")
        age_text = self.age_input.text().strip()

        if not (weight_text and height_text and age_text):
            return None

        try:
            weight = float(weight_text)
            height = float(height_text)
            age = int(age_text)
        except ValueError:
            return None

        gender: Literal["male", "female"] = _GENDER_OPTIONS[
            self.gender_combo.currentIndex()
        ][1]
        goal: Literal["maintain", "lose", "gain"] = _GOAL_OPTIONS[
            self.goal_combo.currentIndex()
        ][1]

        return {
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
