from PyQt6.QtCore import QObject, QSettings, pyqtSignal
from PyQt6.QtWidgets import QApplication

from ..config import THEMES
from ..widgets.style import build_style

_DEFAULT = "dark"


class _ThemeManager(QObject):
    changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        name = str(QSettings("EatLog", "EatLog").value("theme", _DEFAULT))
        self._name = name if name in THEMES else _DEFAULT

    @property
    def name(self) -> str:
        return self._name

    @property
    def colors(self) -> dict[str, str]:
        return THEMES[self._name]

    @property
    def stylesheet(self) -> str:
        return build_style(self.colors)

    def set(self, name: str) -> None:
        if name not in THEMES or name == self._name:
            return
        self._name = name
        QSettings("EatLog", "EatLog").setValue("theme", name)
        app = QApplication.instance()
        if isinstance(app, QApplication):
            app.setStyleSheet(self.stylesheet)
        self.changed.emit()

    def toggle(self) -> None:
        self.set("light" if self._name == "dark" else "dark")


theme = _ThemeManager()
