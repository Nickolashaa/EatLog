from PyQt6.QtCore import QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QPaintEvent, QPen
from PyQt6.QtWidgets import QWidget

from ..config import QSS_COLORS


class Spinner(QWidget):
    def __init__(
        self,
        parent: QWidget | None = None,
        size: int = 28,
        line_width: int = 3,
        color: str = QSS_COLORS["primary"],
        span: int = 280,
    ) -> None:
        super().__init__(parent=parent)
        self._size = size
        self._line_width = line_width
        self._color = QColor(color)
        self._span = span
        self._angle = 0
        self.setFixedSize(size, size)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)

    def start(self) -> None:
        if not self._timer.isActive():
            self._timer.start(20)

    def stop(self) -> None:
        self._timer.stop()

    def _tick(self) -> None:
        self._angle = (self._angle + 8) % 360
        self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        margin = self._line_width
        rect = QRectF(
            margin,
            margin,
            self._size - 2 * margin,
            self._size - 2 * margin,
        )
        pen = QPen(self._color, self._line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(pen)
        p.drawArc(rect, -self._angle * 16, self._span * 16)
        p.end()
