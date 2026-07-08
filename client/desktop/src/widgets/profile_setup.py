from typing import cast
from uuid import UUID

from gql.client import (
    CreateUserCreateUser,
    CreateUserInput,
    GetUserUserObjectNotFoundError,
    GetUserUserUser,
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..config import BOT_USERNAME
from ..utils.gql import client
from ..utils.profile import set_uuid
from ..utils.worker import Worker
from .profile_form import ProfileForm
from .profile_form.types import ProfileFormValues


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

        self.register_switch = QPushButton("Регистрация")
        self.register_switch.setObjectName("SwitchBtn")
        self.register_switch.setCheckable(True)
        self.register_switch.setChecked(True)

        self.login_switch = QPushButton("Вход")
        self.login_switch.setObjectName("SwitchBtn")
        self.login_switch.setCheckable(True)

        switch_group = QButtonGroup(self)
        switch_group.setExclusive(True)
        switch_group.addButton(self.register_switch, 0)
        switch_group.addButton(self.login_switch, 1)
        switch_group.idClicked.connect(self._on_switch)

        switch_row = QWidget()
        switch_layout = QHBoxLayout(switch_row)
        switch_layout.setContentsMargins(0, 0, 0, 0)
        switch_layout.setSpacing(0)
        switch_layout.addWidget(self.register_switch)
        switch_layout.addWidget(self.login_switch)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_register_page())
        self.stack.addWidget(self._build_login_page())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)
        layout.addWidget(title)
        layout.addWidget(switch_row)
        layout.addWidget(self.stack)

    def _build_register_page(self) -> QWidget:
        page = QWidget()

        subtitle = QLabel(
            "Заполните профиль — это нужно для расчёта\nвашей дневной нормы КБЖУ."
        )
        subtitle.setObjectName("WelcomeLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._form = ProfileForm(button_text="Сохранить и начать")
        self._form.saved.connect(self._on_saved)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(self._form)
        return page

    def _build_login_page(self) -> QWidget:
        page = QWidget()

        subtitle = QLabel("Введите свой UUID, чтобы войти в существующий аккаунт.")
        subtitle.setObjectName("WelcomeLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.uuid_input = QLineEdit()
        self.uuid_input.setPlaceholderText("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

        self.request_btn = QPushButton("Запросить UUID из Telegram")
        self.request_btn.setObjectName("TelegramBtn")
        self.request_btn.clicked.connect(self._on_request_uuid)

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self._on_login)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(self.uuid_input)
        layout.addWidget(self.request_btn)
        layout.addWidget(self.login_btn)
        return page

    def _on_switch(self, index: int) -> None:
        self.stack.setCurrentIndex(index)

    def _on_request_uuid(self) -> None:
        url = QUrl(f"https://t.me/{BOT_USERNAME}")
        QDesktopServices.openUrl(url)

    def _on_login(self) -> None:
        text = self.uuid_input.text().strip()
        try:
            uuid = UUID(text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректный UUID.")
            return
        self.login_btn.setEnabled(False)
        self._worker = Worker(client.get_user, uuid)
        self._worker.finished.connect(self._finish_login)
        self._worker.failed.connect(self._on_login_error)
        self._worker.start()

    def _finish_login(self, result: object) -> None:
        user = cast(GetUserUserUser | GetUserUserObjectNotFoundError, result)
        if not isinstance(user, GetUserUserUser):
            self._on_login_error("пользователь не найден")
            return
        set_uuid(str(user.id))
        self.accept()

    def _on_login_error(self, msg: str) -> None:
        self.login_btn.setEnabled(True)
        QMessageBox.warning(
            self,
            "Ошибка",
            f"Не удалось войти. Проверьте UUID:\n{msg}",
        )

    def _on_saved(self, profile: object) -> None:
        values = cast(ProfileFormValues, profile)
        self._form.save_btn.setEnabled(False)
        input_ = CreateUserInput(
            name=values["name"],
            gender=values["gender"],
            weight=values["weight"],
            height=values["height"],
            age=values["age"],
            goal=values["goal"],
            hardMod=False,
        )
        self._worker = Worker(client.create_user, input_)
        self._worker.finished.connect(self._finish)
        self._worker.failed.connect(self._on_error)
        self._worker.start()

    def _finish(self, result: object) -> None:
        user = cast(CreateUserCreateUser, result)
        set_uuid(str(user.id))
        self.accept()

    def _on_error(self, msg: str) -> None:
        self._form.save_btn.setEnabled(True)
        QMessageBox.warning(self, "Ошибка", f"Не удалось создать профиль:\n{msg}")
