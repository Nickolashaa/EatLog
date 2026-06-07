from typing import cast

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QMessageBox, QVBoxLayout, QWidget

from ..services.profile import Profile, ProfileBase, ProfileService
from ..services.users import UserApiService
from ..utils.worker import Worker
from .profile_form import ProfileForm


class ProfileSetupDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.setWindowTitle("Добро пожаловать")
        self.setFixedWidth(420)
        self.setModal(True)
        self._init_ui()

    def _init_ui(self) -> None:
        title = QLabel("Добро пожаловать в EatLog!")
        title.setObjectName("WelcomeTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel(
            "Заполните профиль — это нужно для расчёта\nвашей дневной нормы КБЖУ."
        )
        subtitle.setObjectName("WelcomeLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._form = ProfileForm(button_text="Сохранить и начать")
        self._form.saved.connect(self._on_saved)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(12)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(self._form)

    def _on_saved(self, profile: object) -> None:
        p = cast(ProfileBase, profile)
        self._form.save_btn.setEnabled(False)
        self._worker = Worker(UserApiService.create, p)
        self._worker.finished.connect(lambda uuid: self._finish(p, str(uuid)))
        self._worker.failed.connect(self._on_error)
        self._worker.start()

    def _finish(self, base: ProfileBase, uuid: str) -> None:
        full: Profile = {**base, "uuid": uuid}
        ProfileService.save(full)
        self.accept()

    def _on_error(self, msg: str) -> None:
        self._form.save_btn.setEnabled(True)
        QMessageBox.warning(self, "Ошибка", f"Не удалось создать профиль:\n{msg}")
