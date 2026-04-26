from pathlib import Path

from ..config import QSS_COLORS


def load_style(widget_file_path: str) -> str:
    style = (Path(widget_file_path).parent / "style.qss").read_text()
    result = str()

    for line in style.split("\n"):
        index = line.find("@")
        if index != -1:
            var = line[index + 1 :].replace(";", "").strip()
            line = f"{line[:index]}{QSS_COLORS[var]};\n"
        result += line

    return result
