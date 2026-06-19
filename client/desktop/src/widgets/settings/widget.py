from typing import cast

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QDesktopServices, QHideEvent, QShowEvent
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ...config import BOT_USERNAME
from ...services.profile import Kbzhu, Profile, ProfileBase, ProfileService
from ...services.users import UserApiService
from ...utils.worker import Worker
from ..header import Header
from ..profile_form import ProfileForm
from ..spinner import Spinner
from .types import KBZHU_ROWS


class SettingsWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._val_labels: dict[str, QLabel] = {}
        self._telegram_linked = False
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
        if not ProfileService.exists():
            return
        self._profile_worker = Worker(ProfileService.load)
        self._profile_worker.finished.connect(self._on_profile_loaded)
        self._profile_worker.start()

    def _on_profile_loaded(self, profile: object) -> None:
        p = cast(Profile, profile)
        self.profile_form.load(p)
        self._update_kbzhu(ProfileService.calculate(p))

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
        p = cast(ProfileBase, profile)
        if not ProfileService.exists():
            return
        uuid = ProfileService.uuid()
        self.profile_form.save_btn.setEnabled(False)
        self._worker = Worker(UserApiService.update, uuid=uuid, profile=p)
        self._worker.finished.connect(lambda _: self._finish_save(p, uuid))
        self._worker.failed.connect(self._on_save_error)
        self._worker.start()

    def _finish_save(self, base: ProfileBase, uuid: str) -> None:
        full: Profile = {**base, "uuid": uuid}
        ProfileService.set_cache(full)
        self.profile_form.save_btn.setEnabled(True)
        self._update_kbzhu(ProfileService.calculate(full))

    def _on_save_error(self, msg: str) -> None:
        self.profile_form.save_btn.setEnabled(True)
        QMessageBox.warning(self, "Ошибка", f"Не удалось обновить профиль:\n{msg}")

    def _on_link_telegram(self) -> None:
        if not ProfileService.exists():
            QMessageBox.warning(
                self,
                "Профиль не найден",
                "Сначала заполните профиль, чтобы привязать Telegram.",
            )
            return
        uuid = ProfileService.uuid()
        url = QUrl(f"https://t.me/{BOT_USERNAME}?start=reg_{uuid}")
        QDesktopServices.openUrl(url)
        if not self._telegram_timer.isActive():
            self._telegram_timer.start()
        self._refresh_telegram_ui()
        self._sync_telegram()

    def _refresh_telegram_ui(self) -> None:
        linked = self._telegram_linked
        polling = self._telegram_timer.isActive()
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
        if self._telegram_linked or not ProfileService.exists():
            self._telegram_timer.stop()
            return
        uuid = ProfileService.uuid()
        self._telegram_worker = Worker(UserApiService.get_telegram_id, uuid)
        self._telegram_worker.finished.connect(self._on_telegram_checked)
        self._telegram_worker.start()

    def _on_telegram_checked(self, telegram_id: object) -> None:
        if telegram_id is None:
            return
        self._telegram_linked = True
        self._refresh_telegram_ui()

    def _update_kbzhu(self, kbzhu: Kbzhu) -> None:
        data = cast(dict[str, int], kbzhu)
        for key, lbl in self._val_labels.items():
            lbl.setText(str(data[key]))
