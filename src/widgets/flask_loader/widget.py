from PyQt6.QtCore import QRectF, Qt, QTimer
from PyQt6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPaintEvent, QPen
from PyQt6.QtWidgets import QWidget

from src.config import QSS_COLORS


class FlaskLoader(QWidget):
    def __init__(
        self,
        parent: QWidget | None,
        fill: int = 0,
        fill_color: str = QSS_COLORS["success"],
        border_width: int = 5,
        border_radius: int = 20,
        border_color: str = QSS_COLORS["border"],
        background_color: str = QSS_COLORS["bg_elevated"],
    ):
        super().__init__(parent=parent)
        self.border_width = border_width
        self.border_radius = border_radius
        if not (0 <= fill <= 100):
            raise ValueError(f"fill must be between 0 and 100, got {fill}")
        self.current_fill = fill
        self.target_fill = fill
        self.background_color = QColor(background_color)
        self.border_color = QColor(border_color)
        self.fill_color = QColor(fill_color)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def set_fill(self, fill: int) -> None:
        if not (0 <= fill <= 100):
            raise ValueError(f"fill must be between 0 and 100, got {fill}")
        self.target_fill = fill

    def _update_fill(self) -> None:
        if self.current_fill < self.target_fill:
            self.current_fill += 1
        else:
            self.current_fill -= 1

    def _tick(self) -> None:
        if self.target_fill == self.current_fill:
            return

        self._update_fill()
        self.update()

    def _calculate_main_rect(self) -> QRectF:
        return QRectF(
            0,
            0,
            self.width(),
            self.height(),
        )

    def _calculate_filled_rect(self) -> QRectF:
        return QRectF(
            0,
            self.height() - self.height() * self.current_fill // 100,
            self.width(),
            self.height(),
        )

    def _draw_background(self, p: QPainter, rect: QRectF) -> None:
        p.setBrush(self.background_color)
        p.drawRoundedRect(rect, self.border_radius, self.border_radius)

    def _draw_fill(self, p: QPainter, filled_rect: QRectF) -> None:
        if filled_rect.height() > 0:
            p.setBrush(self.fill_color)
            p.drawRect(filled_rect)

    def _draw_border(self, p: QPainter, rect: QRectF) -> None:
        p.setPen(QPen(QBrush(self.border_color), self.border_width))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(rect, self.border_radius, self.border_radius)

    def paintEvent(self, event: QPaintEvent | None) -> None:
        rect = self._calculate_main_rect()
        filled_rect = self._calculate_filled_rect()

        clip = QPainterPath()
        clip.addRoundedRect(rect, self.border_radius, self.border_radius)

        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setClipPath(clip)

        self._draw_background(p, rect)
        self._draw_fill(p, filled_rect)
        self._draw_border(p, rect)

        p.end()
