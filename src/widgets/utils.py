from pathlib import Path

from ..config import QSS_COLORS


def load_style(widget_file_path: str) -> str:
    style = (Path(widget_file_path).parent / "style.qss").read_text()

    for key, value in QSS_COLORS.items():
        style = style.replace(key, value)

    return style
