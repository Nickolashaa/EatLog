from datetime import datetime
from typing import cast
from uuid import UUID

from PyQt6.QtCore import Qt, QTime, QTimer, QUrl
from PyQt6.QtGui import QDesktopServices, QHideEvent, QShowEvent
from PyQt6.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from ...config import BOT_USERNAME
from ...graphql.client import (
    GetUser,
    GetUserUserUser,
    UpdateUser,
    UpdateUserInput,
    UpdateUserUpdateUserUser,
    UserFields,
)
from ...utils.gql import client
from ...utils.profile import Kbzhu, calculate_kbzhu, get_uuid, profile_exists
from ...utils.worker import Worker
from ..header import Header
from ..profile_form import ProfileForm
from ..profile_form.types import ProfileFormValues
from ..spinner import Spinner
from .types import KBZHU_ROWS


class SettingsWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._val_labels: dict[str, QLabel] = {}
        self._telegram_linked = False
        self._user: UserFields | None = None
        self._init_ui()
        self._try_load_profile()
        self._telegram_timer = QTimer(self)
        self._telegram_timer.setInterval(3000)
        self._telegram_timer.timeout.connect(self._sync_telegram)
        self._refresh_telegram_ui()

    def _init_ui(self) -> None:
        self.header = Header(parent=self, text="Настройки")

        left_panel = QWidget()
        left_panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        left_panel.setObjectName("SettingsPanel")

        profile_title = QLabel("Профиль")
        profile_title.setObjectName("SectionTitle")

        self.profile_form = ProfileForm(button_text="Обновить")
        self.profile_form.saved.connect(self._on_profile_saved)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(28, 28, 28, 28)
        left_layout.setSpacing(22)
        left_layout.addWidget(profile_title)
        left_layout.addWidget(self.profile_form)
        left_layout.addStretch()

        right_panel = QWidget()
        right_panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        right_panel.setObjectName("SettingsPanel")

        kbzhu_title = QLabel("Норма на день")
        kbzhu_title.setObjectName("SectionTitle")

        grid = QGridLayout()
        grid.setSpacing(16)
        grid.setContentsMargins(0, 0, 0, 0)

        for row_idx, (key, label_text, unit) in enumerate(KBZHU_ROWS):
            name_lbl = QLabel(label_text)
            name_lbl.setObjectName("KbzhuName")

            val_lbl = QLabel("—")
            val_lbl.setObjectName("KbzhuValue")
            val_lbl.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self._val_labels[key] = val_lbl

            unit_lbl = QLabel(unit)
            unit_lbl.setObjectName("KbzhuUnit")

            grid.addWidget(name_lbl, row_idx, 0)
            grid.addWidget(val_lbl, row_idx, 1)
            grid.addWidget(unit_lbl, row_idx, 2)

        grid.setColumnStretch(1, 1)

        self.notifications_section = QWidget()

        notifications_title = QLabel("Уведомления")
        notifications_title.setObjectName("SectionTitle")

        self.notifications_check = QCheckBox("Получать уведомления")
        self.notifications_check.toggled.connect(self._on_notifications_toggled)

        self.notification_time_edit = QTimeEdit()
        self.notification_time_edit.setDisplayFormat("HH:mm")
        self.notification_time_edit.setTime(QTime(21, 0))
        self.notification_time_edit.setMaximumWidth(130)
        self.notification_time_edit.hide()

        self.hard_mod_check = QCheckBox("Режим повышенной жестокости")
        self.hard_mod_check.hide()

        self.notifications_save_btn = QPushButton("Сохранить")
        self.notifications_save_btn.clicked.connect(self._on_save_notifications)

        notifications_layout = QVBoxLayout(self.notifications_section)
        notifications_layout.setSpacing(12)
        notifications_layout.setContentsMargins(0, 0, 0, 0)
        notifications_layout.addWidget(notifications_title)
        notifications_layout.addWidget(self.notifications_check)
        notifications_layout.addWidget(
            self.notification_time_edit, alignment=Qt.AlignmentFlag.AlignLeft
        )
        notifications_layout.addWidget(self.hard_mod_check)
        notifications_layout.addWidget(self.notifications_save_btn)

        self.notifications_section.hide()

        self.telegram_title = QLabel("Telegram")
        self.telegram_title.setObjectName("SectionTitle")

        self.telegram_hint = QLabel(
            "Привяжите Telegram, чтобы не потерять свои данные при "
            "переустановке и получить доступ к дополнительным функциям бота."
        )
        self.telegram_hint.setObjectName("TelegramHint")
        self.telegram_hint.setWordWrap(True)

        self.telegram_btn = QPushButton("Привязать Telegram")
        self.telegram_btn.setObjectName("TelegramBtn")
        self.telegram_btn.clicked.connect(self._on_link_telegram)

        self.telegram_spinner = Spinner(parent=self)
        self.telegram_spinner.hide()

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(28, 28, 28, 28)
        right_layout.setSpacing(24)
        right_layout.addWidget(kbzhu_title)
        right_layout.addLayout(grid)
        right_layout.addSpacing(8)
        right_layout.addWidget(self.notifications_section)
        right_layout.addSpacing(8)
        right_layout.addWidget(self.telegram_title)
        right_layout.addWidget(self.telegram_hint)
        right_layout.addWidget(self.telegram_btn)
        right_layout.addWidget(
            self.telegram_spinner, alignment=Qt.AlignmentFlag.AlignLeft
        )
        right_layout.addStretch()

        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        content_layout.addWidget(left_panel, 1)
        content_layout.addWidget(right_panel, 1)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.addWidget(self.header)
        main_layout.addWidget(content, 1)

        self.setObjectName("SettingsWidget")

    def _try_load_profile(self) -> None:
        if not profile_exists():
            return
        self._profile_worker = Worker(client.get_user, UUID(get_uuid()))
        self._profile_worker.finished.connect(self._on_profile_loaded)
        self._profile_worker.start()

    def _on_profile_loaded(self, result: object) -> None:
        user = cast(GetUser, result).user
        if not isinstance(user, GetUserUserUser):
            return
        self._user = user
        self.profile_form.load(user)
        self._update_kbzhu(self._kbzhu(user))
        self._load_notifications(user)

    def _kbzhu(self, user: UserFields) -> Kbzhu:
        return calculate_kbzhu(
            gender=user.gender,
            weight=user.weight,
            height=user.height,
            age=user.age,
            goal=user.goal,
        )

    def _load_notifications(self, user: UserFields) -> None:
        nt = user.notification_time
        if nt:
            local = nt.astimezone()
            self.notification_time_edit.setTime(QTime(local.hour, local.minute))
        self.notifications_check.setChecked(nt is not None)
        self.notification_time_edit.setVisible(nt is not None)
        self.hard_mod_check.setVisible(nt is not None)
        self.hard_mod_check.setChecked(user.hard_mod)

    def _on_notifications_toggled(self, checked: bool) -> None:
        self.notification_time_edit.setVisible(checked)
        self.hard_mod_check.setVisible(checked)

    def _on_save_notifications(self) -> None:
        if not profile_exists():
            return
        if self.notifications_check.isChecked():
            t = self.notification_time_edit.time()
            notification_time: datetime | None = (
                datetime.now()
                .astimezone()
                .replace(hour=t.hour(), minute=t.minute(), second=0, microsecond=0)
            )
        else:
            notification_time = None
        hard_mod = self.hard_mod_check.isChecked()
        self.notifications_save_btn.setEnabled(False)
        self._notifications_worker = Worker(
            client.update_user,
            id=UUID(get_uuid()),
            input=UpdateUserInput(notificationTime=notification_time, hardMod=hard_mod),
        )
        self._notifications_worker.finished.connect(
            lambda _: self._finish_notifications_save(notification_time, hard_mod)
        )
        self._notifications_worker.failed.connect(self._on_notifications_error)
        self._notifications_worker.start()

    def _finish_notifications_save(
        self, notification_time: datetime | None, hard_mod: bool
    ) -> None:
        self.notifications_save_btn.setEnabled(True)
        if self._user is not None:
            self._user.notification_time = notification_time
            self._user.hard_mod = hard_mod

    def _on_notifications_error(self, msg: str) -> None:
        self.notifications_save_btn.setEnabled(True)
        QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить уведомления:\n{msg}")

    def showEvent(self, event: QShowEvent | None) -> None:
        super().showEvent(event)
        self._try_load_profile()
        self._refresh_telegram_ui()
        self._sync_telegram()

    def hideEvent(self, event: QHideEvent | None) -> None:
        super().hideEvent(event)
        self._telegram_timer.stop()
        self.telegram_spinner.stop()

    def _on_profile_saved(self, profile: object) -> None:
        values = cast(ProfileFormValues, profile)
        if not profile_exists():
            return
        self.profile_form.save_btn.setEnabled(False)
        self._worker = Worker(
            client.update_user,
            id=UUID(get_uuid()),
            input=UpdateUserInput(
                name=values["name"],
                gender=values["gender"],
                weight=values["weight"],
                height=values["height"],
                age=values["age"],
                goal=values["goal"],
            ),
        )
        self._worker.finished.connect(self._finish_save)
        self._worker.failed.connect(self._on_save_error)
        self._worker.start()

    def _finish_save(self, result: object) -> None:
        self.profile_form.save_btn.setEnabled(True)
        user = cast(UpdateUser, result).update_user
        if not isinstance(user, UpdateUserUpdateUserUser):
            self._on_save_error(user.message)
            return
        self._user = user
        self._update_kbzhu(self._kbzhu(user))

    def _on_save_error(self, msg: str) -> None:
        self.profile_form.save_btn.setEnabled(True)
        QMessageBox.warning(self, "Ошибка", f"Не удалось обновить профиль:\n{msg}")

    def _on_link_telegram(self) -> None:
        if not profile_exists():
            QMessageBox.warning(
                self,
                "Профиль не найден",
                "Сначала заполните профиль, чтобы привязать Telegram.",
            )
            return
        uuid = get_uuid()
        url = QUrl(f"https://t.me/{BOT_USERNAME}?start={uuid}")
        QDesktopServices.openUrl(url)
        if not self._telegram_timer.isActive():
            self._telegram_timer.start()
        self._refresh_telegram_ui()
        self._sync_telegram()

    def _refresh_telegram_ui(self) -> None:
        linked = self._telegram_linked
        polling = self._telegram_timer.isActive()
        self.notifications_section.setVisible(linked)
        self.telegram_title.setVisible(not linked)
        self.telegram_hint.setVisible(not linked)
        self.telegram_btn.setVisible(not linked and not polling)
        self.telegram_spinner.setVisible(not linked and polling)
        if not linked and polling:
            self.telegram_spinner.start()
        else:
            self.telegram_spinner.stop()
        if linked:
            self._telegram_timer.stop()

    def _sync_telegram(self) -> None:
        if self._telegram_linked or not profile_exists():
            self._telegram_timer.stop()
            return
        self._telegram_worker = Worker(client.get_user, UUID(get_uuid()))
        self._telegram_worker.finished.connect(self._on_telegram_checked)
        self._telegram_worker.start()

    def _on_telegram_checked(self, result: object) -> None:
        user = cast(GetUser, result).user
        if not isinstance(user, GetUserUserUser) or user.telegram_id is None:
            return
        self._telegram_linked = True
        self._refresh_telegram_ui()

    def _update_kbzhu(self, kbzhu: Kbzhu) -> None:
        data = cast(dict[str, int], kbzhu)
        for key, lbl in self._val_labels.items():
            lbl.setText(str(data[key]))
