from PyQt6.QtWidgets import QMainWindow

from .config import HEIGHT, TITLE, WIDTH


class EatLog(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(TITLE)
        self.resize(WIDTH, HEIGHT)
