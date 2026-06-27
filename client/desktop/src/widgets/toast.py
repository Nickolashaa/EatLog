from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QLabel, QWidget


def show_toast(
    parent: QWidget, message: str, *, success: bool = True, duration_ms: int = 2500
) -> None:
    """Show a transient, auto-dismissing notification at the bottom of the window."""
    window = parent.window()
    if window is None:
        return

    toast = QLabel(message, window)
    toast.setObjectName("ToastSuccess" if success else "ToastError")
    toast.setAlignment(Qt.AlignmentFlag.AlignCenter)
    toast.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    toast.adjustSize()

    x = (window.width() - toast.width()) // 2
    y = window.height() - toast.height() - 32
    toast.move(max(0, x), max(0, y))

    toast.show()
    toast.raise_()

    QTimer.singleShot(duration_ms, toast.deleteLater)
