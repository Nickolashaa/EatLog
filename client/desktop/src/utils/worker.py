import asyncio
import inspect
from collections.abc import Callable
from typing import Any

from PyQt6.QtCore import QThread, pyqtSignal


class Worker(QThread):
    finished = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        super().__init__()
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def run(self) -> None:
        try:
            result = self._fn(*self._args, **self._kwargs)
            if inspect.iscoroutine(result):
                result = asyncio.run(result)
            self.finished.emit(result)
        except Exception as e:
            self.failed.emit(str(e))
