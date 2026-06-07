from typing import cast

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from ..services.profile import Kbzhu, Profile, ProfileBase, ProfileService
from ..services.users import UserApiService
from ..utils.worker import Worker
from .header import Header
from .profile_form import ProfileForm

_KBZHU_ROWS: list[tuple[str, str, str]] = [
    ("calories", "Калории", "ккал"),
    ("protein", "Белки", "г"),
    ("fat", "Жиры", "г"),
    ("carbohydrate", "Углеводы", "г"),
]


class SettingsWidget(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._val_labels: dict[str, QLabel] = {}
        self._init_ui()
        self._try_load_profile()

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

        for row_idx, (key, label_text, unit) in enumerate(_KBZHU_ROWS):
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

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(28, 28, 28, 28)
        right_layout.setSpacing(24)
        right_layout.addWidget(kbzhu_title)
        right_layout.addLayout(grid)
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
        if ProfileService.exists():
            profile = ProfileService.load()
            self.profile_form.load(profile)
            self._update_kbzhu(ProfileService.calculate(profile))

    def showEvent(self, event: QShowEvent | None) -> None:
        super().showEvent(event)
        self._try_load_profile()

    def _on_profile_saved(self, profile: object) -> None:
        p = cast(ProfileBase, profile)
        if not ProfileService.exists():
            return
        uuid = ProfileService.load()["uuid"]
        self.profile_form.save_btn.setEnabled(False)
        self._worker = Worker(UserApiService.update, uuid=uuid, profile=p)
        self._worker.finished.connect(lambda _: self._finish_save(p, uuid))
        self._worker.failed.connect(self._on_save_error)
        self._worker.start()

    def _finish_save(self, base: ProfileBase, uuid: str) -> None:
        full: Profile = {**base, "uuid": uuid}
        ProfileService.save(full)
        self.profile_form.save_btn.setEnabled(True)
        self._update_kbzhu(ProfileService.calculate(full))

    def _on_save_error(self, msg: str) -> None:
        self.profile_form.save_btn.setEnabled(True)
        QMessageBox.warning(self, "Ошибка", f"Не удалось обновить профиль:\n{msg}")

    def _update_kbzhu(self, kbzhu: Kbzhu) -> None:
        data = cast(dict[str, int], kbzhu)
        for key, lbl in self._val_labels.items():
            lbl.setText(str(data[key]))
