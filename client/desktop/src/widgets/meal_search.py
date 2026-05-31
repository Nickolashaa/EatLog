from PyQt6.QtCore import QLocale, Qt, pyqtSignal
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..database.connection import session_maker
from ..database.models.meals import Meal
from ..services.meal_log import MealLogService
from ..services.meals import MealService
from .header import Header


class MealSearch(QWidget):
    meal_added = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self._meals: list[Meal] = []
        self._init_ui()

    def _float_input(self, placeholder: str) -> QLineEdit:
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        validator = QDoubleValidator(0.0, 9999.0, 1)
        validator.setLocale(QLocale(QLocale.Language.English))
        field.setValidator(validator)
        return field

    def _init_ui(self) -> None:
        self.header = Header(parent=self, text="Добавить прием пищи")

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Поиск блюда...")
        self.search_input.textChanged.connect(self._on_search)

        self.table = QTableWidget(0, 3, self)
        self.table.setHorizontalHeaderLabels(["Название", "Граммы", ""])

        h_header = self.table.horizontalHeader()
        assert h_header is not None
        h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        h_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        h_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(1, 90)
        self.table.setColumnWidth(2, 110)

        v_header = self.table.verticalHeader()
        assert v_header is not None
        v_header.setVisible(False)
        v_header.setDefaultSectionSize(48)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setShowGrid(False)
        self.table.hide()

        self._no_results_section = QWidget(self)

        not_found_lbl = QLabel("Ничего не найдено")
        not_found_lbl.setObjectName("NotFoundLabel")

        subtitle_lbl = QLabel("Создать новое блюдо · на 100 грамм продукта")
        subtitle_lbl.setObjectName("FormSubtitle")

        self._create_title = QLineEdit()
        self._create_title.setPlaceholderText("Название")
        self._create_calories = self._float_input("Калории (ккал)")
        self._create_protein = self._float_input("Белки (г)")
        self._create_fat = self._float_input("Жиры (г)")
        self._create_carbohydrate = self._float_input("Углеводы (г)")

        create_btn = QPushButton("Создать блюдо")
        create_btn.clicked.connect(self._on_create)

        section_layout = QVBoxLayout(self._no_results_section)
        section_layout.setContentsMargins(0, 4, 0, 0)
        section_layout.setSpacing(12)
        section_layout.addWidget(not_found_lbl)
        section_layout.addWidget(subtitle_lbl)
        section_layout.addWidget(self._create_title)
        section_layout.addWidget(self._create_calories)
        section_layout.addWidget(self._create_protein)
        section_layout.addWidget(self._create_fat)
        section_layout.addWidget(self._create_carbohydrate)
        section_layout.addWidget(create_btn)

        self._no_results_section.hide()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)
        layout.addWidget(self.header)
        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.addWidget(self._no_results_section)
        layout.addStretch()
        self.setLayout(layout)

        self.setObjectName("MealSearch")

    def _on_search(self, text: str) -> None:
        query = text.strip()
        if not query:
            self.table.hide()
            self._no_results_section.hide()
            return

        with session_maker() as session:
            meals = MealService.get_list(session, query, limit=5)

        if meals:
            self._no_results_section.hide()
            self._populate_table(meals)
        else:
            self.table.hide()
            self._create_title.setText(query)
            self._no_results_section.show()

    def _populate_table(self, meals: list[Meal]) -> None:
        self._meals = meals
        self.table.setRowCount(len(meals))

        for row, meal in enumerate(meals):
            title_item = QTableWidgetItem(meal.title)
            self.table.setItem(row, 0, title_item)

            grams_input = QLineEdit()
            grams_input.setPlaceholderText("100")
            validator = QDoubleValidator(0.0, 9999.0, 1)
            validator.setLocale(QLocale(QLocale.Language.English))
            grams_input.setValidator(validator)
            self.table.setCellWidget(row, 1, grams_input)

            add_btn = QPushButton("Добавить")
            add_btn.clicked.connect(lambda checked, r=row: self._on_add(r))
            self.table.setCellWidget(row, 2, add_btn)

        self.table.show()

    def _on_add(self, row: int) -> None:
        if row >= len(self._meals):
            return

        meal = self._meals[row]
        grams_widget = self.table.cellWidget(row, 1)
        if not isinstance(grams_widget, QLineEdit):
            return

        grams_text = grams_widget.text().strip().replace(",", ".")
        grams = float(grams_text) if grams_text else 100.0

        with session_maker() as session:
            MealLogService.create(session, {"meal_id": meal.id, "grams": grams})
            session.commit()

        grams_widget.clear()
        self.meal_added.emit()

    def _on_create(self) -> None:
        title = self._create_title.text().strip()
        if not title:
            return

        def parse(field: QLineEdit) -> float:
            return float(field.text().strip().replace(",", ".") or "0")

        try:
            with session_maker() as session:
                MealService.create(
                    session,
                    {
                        "title": title,
                        "calories": parse(self._create_calories),
                        "protein": parse(self._create_protein),
                        "fat": parse(self._create_fat),
                        "carbohydrate": parse(self._create_carbohydrate),
                    },
                )
                session.commit()
        except Exception:
            return

        for field in (
            self._create_calories,
            self._create_protein,
            self._create_fat,
            self._create_carbohydrate,
        ):
            field.clear()

        self._on_search(self.search_input.text())
