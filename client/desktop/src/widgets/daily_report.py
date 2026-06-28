from datetime import datetime, timezone
from typing import cast
from uuid import UUID

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..graphql.client import GetUser, GetUserUserUser, MealLogFilter, MealLogs
from ..utils.gql import client
from ..utils.nutrition import Macros, sum_macros
from ..utils.profile import Kbzhu, calculate_kbzhu, get_uuid, profile_exists
from ..utils.theme import theme
from ..utils.worker import Worker
from .flask_loader import FlaskLoader
from .header import Header


class DailyReport(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._init_ui()
        self.refresh()
        theme.changed.connect(self.refresh)

    def _init_ui(self) -> None:
        self.header = Header(parent=self, text="Ежедневный отчет")

        refresh_btn = QPushButton("Обновить", self)
        refresh_btn.setObjectName("RefreshBtn")
        refresh_btn.clicked.connect(self.refresh)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(10)
        header_row.addWidget(self.header, 1)
        header_row.addWidget(refresh_btn)

        self.protein_flask, self.protein_value_lbl, protein_col = self._flask_column(
            "Белки", "г"
        )
        self.fat_flask, self.fat_value_lbl, fat_col = self._flask_column("Жиры", "г")
        self.carbohydrate_flask, self.carbohydrate_value_lbl, carbohydrate_col = (
            self._flask_column("Углеводы", "г")
        )
        self.calories_flask, self.calories_value_lbl, calories_col = self._flask_column(
            "Калории", "ккал"
        )

        mid_layout = QHBoxLayout()
        mid_layout.setContentsMargins(12, 0, 12, 12)
        mid_layout.setSpacing(12)
        mid_layout.addWidget(protein_col)
        mid_layout.addWidget(fat_col)
        mid_layout.addWidget(carbohydrate_col)
        mid_layout.addWidget(calories_col)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 0)
        main_layout.setSpacing(0)
        main_layout.addLayout(header_row)
        main_layout.addLayout(mid_layout, 1)
        self.setLayout(main_layout)

        self.setObjectName("DailyReport")

    def _flask_column(
        self, name: str, unit: str
    ) -> tuple[FlaskLoader, QLabel, QWidget]:
        container = QWidget(self)

        name_lbl = QLabel(name, container)
        name_lbl.setObjectName("FlaskName")
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        value_lbl = QLabel("— / —", container)
        value_lbl.setObjectName("FlaskValue")
        value_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_lbl.setProperty("unit", unit)

        flask = FlaskLoader(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(4)
        layout.addWidget(name_lbl)
        layout.addWidget(value_lbl)
        layout.addWidget(flask, 1)

        return flask, value_lbl, container

    def refresh(self) -> None:
        if not profile_exists():
            return

        self._profile_worker = Worker(client.get_user, UUID(get_uuid()))
        self._profile_worker.finished.connect(self._on_user_loaded)
        self._profile_worker.failed.connect(self._on_error)
        self._profile_worker.start()

    def _on_user_loaded(self, result: object) -> None:
        user = cast(GetUser, result).user
        if not isinstance(user, GetUserUserUser):
            return
        kbzhu = calculate_kbzhu(
            gender=user.gender,
            weight=user.weight,
            height=user.height,
            age=user.age,
            goal=user.goal,
        )
        target_date = datetime.now().astimezone(timezone.utc).date()
        self._worker = Worker(
            client.meal_logs,
            filter_=MealLogFilter(userId=user.id, dateFilter=target_date),
            limit=1000,
        )
        self._worker.finished.connect(
            lambda result: self._update_display(
                sum_macros(cast(MealLogs, result).meal_logs), kbzhu
            )
        )
        self._worker.failed.connect(self._on_error)
        self._worker.start()

    def _update_display(self, totals: Macros, kbzhu: Kbzhu) -> None:
        def pct(actual: float, target: int) -> int:
            return min(100, round(actual * 100 / target)) if target > 0 else 0

        def color(actual: float, target: int) -> str:
            if target <= 0:
                return theme.colors["success"]
            ratio = actual / target
            if ratio <= 1.0:
                return theme.colors["success"]
            if ratio <= 1.2:
                return theme.colors["warning"]
            return theme.colors["error"]

        def fmt(actual: float, target: int, unit: str) -> str:
            a = round(actual, 1)
            actual_str = str(int(a)) if a == int(a) else str(a)
            return f"{actual_str} / {target} {unit}"

        self.protein_flask.set_fill(pct(totals["protein"], kbzhu["protein"]))
        self.protein_flask.set_fill_color(color(totals["protein"], kbzhu["protein"]))
        self.protein_value_lbl.setText(fmt(totals["protein"], kbzhu["protein"], "г"))

        self.fat_flask.set_fill(pct(totals["fat"], kbzhu["fat"]))
        self.fat_flask.set_fill_color(color(totals["fat"], kbzhu["fat"]))
        self.fat_value_lbl.setText(fmt(totals["fat"], kbzhu["fat"], "г"))

        self.carbohydrate_flask.set_fill(
            pct(totals["carbohydrate"], kbzhu["carbohydrate"])
        )
        self.carbohydrate_flask.set_fill_color(
            color(totals["carbohydrate"], kbzhu["carbohydrate"])
        )
        self.carbohydrate_value_lbl.setText(
            fmt(totals["carbohydrate"], kbzhu["carbohydrate"], "г")
        )

        self.calories_flask.set_fill(pct(totals["calories"], kbzhu["calories"]))
        self.calories_flask.set_fill_color(color(totals["calories"], kbzhu["calories"]))
        self.calories_value_lbl.setText(
            fmt(totals["calories"], kbzhu["calories"], "ккал")
        )

    def _on_error(self, msg: str) -> None:
        QMessageBox.warning(self, "Ошибка загрузки", msg)
