from typing import cast

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QWidget

from ..services.profile import Profile, ProfileService
from .profile_form import ProfileForm


class ProfileSetupDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.setWindowTitle("Добро пожаловать")
        self.setFixedWidth(420)
        self.setModal(True)
        self._init_ui()

    def _init_ui(self) -> None:
        welcome = QLabel(
            "Заполните профиль — это нужно для расчёта\nвашей дневной нормы КБЖУ."
        )
        welcome.setObjectName("WelcomeLabel")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form = ProfileForm(button_text="Сохранить и начать")
        form.saved.connect(self._on_saved)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(20)
        layout.addWidget(welcome)
        layout.addWidget(form)

    def _on_saved(self, profile: object) -> None:
        ProfileService.save(cast(Profile, profile))
        self.accept()
