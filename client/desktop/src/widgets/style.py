from string import Template

from ..config import QSS_COLORS

_TEMPLATE = Template(
    """
QMainWindow {
    background-color: $bg;
}

QTabWidget::pane {
    background-color: $bg;
    border: 1px solid $border;
}

QTabBar::tab {
    background-color: $bg_secondary;
    color: $text_muted;
    padding: 8px 18px;
    border: none;
}

QTabBar::tab:selected {
    background-color: $bg_elevated;
    color: $text;
    border-bottom: 2px solid $primary;
}

QTabBar::tab:hover:!selected {
    background-color: $bg_elevated;
    color: $text;
}

QDialog {
    background-color: $bg;
}

#MealSearch {
    background-color: $bg_secondary;
    border-right: 1px solid $border;
}

#MealTable {
    background-color: $bg_secondary;
}

#MealLogTable {
    background-color: $bg_secondary;
}

#DailyReport {
    background-color: $bg_secondary;
    border-left: 1px solid $border;
}

#SettingsWidget {
    background-color: $bg_secondary;
}

#SettingsPanel {
    background-color: $bg;
}

#Header {
    color: $text;
    background-color: $bg_elevated;
    font-size: 18px;
    font-weight: bold;
    padding: 12px 18px;
    border-radius: 6px;
}

QLabel {
    color: $text_muted;
    font-size: 14px;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

#SectionTitle {
    color: $text;
    font-size: 18px;
    font-weight: bold;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

#KbzhuName {
    color: $text_muted;
    font-size: 20px;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

#KbzhuValue {
    color: $primary;
    font-size: 48px;
    font-weight: bold;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

#KbzhuUnit {
    color: $text_disabled;
    font-size: 18px;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

#FlaskName {
    color: $text;
    font-size: 13px;
    font-weight: bold;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

#FlaskValue {
    color: $text_muted;
    font-size: 12px;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

#NotFoundLabel {
    color: $text_muted;
    font-size: 16px;
    font-weight: bold;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

#FormSubtitle {
    color: $text_disabled;
    font-size: 13px;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

#WelcomeTitle {
    color: $primary;
    font-size: 22px;
    font-weight: bold;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

#WelcomeLabel {
    color: $text_muted;
    font-size: 13px;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

QPushButton#SwitchBtn {
    background-color: $bg_secondary;
    color: $text_muted;
    border: 1px solid $border;
    border-radius: 0;
    padding: 10px 14px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#SwitchBtn:hover {
    background-color: $bg_elevated;
    color: $text;
}

QPushButton#SwitchBtn:checked {
    background-color: $bg_elevated;
    color: $text;
    border-bottom: 2px solid $primary;
}

#TelegramHint {
    color: $text_muted;
    font-size: 14px;
    line-height: 20px;
    background: transparent;
    padding: 0;
    border-radius: 0;
}

QPushButton#TelegramBtn {
    background-color: $secondary;
    color: $bg;
    border: none;
    border-radius: 7px;
    padding: 11px 14px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton#TelegramBtn:hover {
    background-color: $secondary_hover;
}

QPushButton#TelegramBtn:pressed {
    background-color: $secondary;
}

QLineEdit {
    background-color: $bg_elevated;
    color: $text;
    border: 1px solid $border;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 15px;
}

QLineEdit:focus {
    border-color: $border_focus;
}

QComboBox {
    background-color: $bg_elevated;
    color: $text;
    border: 1px solid $border;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 15px;
}

QComboBox:focus {
    border-color: $border_focus;
}

QComboBox::drop-down {
    border: none;
    width: 28px;
}

QComboBox QAbstractItemView {
    background-color: $bg_elevated;
    color: $text;
    border: 1px solid $border;
    selection-background-color: $primary;
    selection-color: $bg;
    outline: 0;
    font-size: 15px;
}

QDateEdit {
    background-color: $bg_elevated;
    color: $text;
    border: 1px solid $border;
    border-radius: 6px;
    padding: 7px 11px;
    font-size: 13px;
}

QDateEdit:focus {
    border-color: $border_focus;
}

QDateEdit::drop-down {
    border: none;
    width: 24px;
}

QCalendarWidget {
    background-color: $bg_elevated;
    color: $text;
}

QPushButton {
    background-color: $primary;
    color: $bg;
    border: none;
    border-radius: 7px;
    padding: 9px 14px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: $secondary;
}

QPushButton:pressed {
    background-color: $primary;
}

QPushButton#RefreshBtn {
    background-color: $bg_elevated;
    color: $text;
    border: 1px solid $border;
    border-radius: 7px;
    padding: 8px 14px;
    font-size: 13px;
    font-weight: bold;
}

QPushButton#RefreshBtn:hover {
    background-color: $border;
}

QPushButton#RefreshBtn:pressed {
    background-color: $bg_elevated;
}

QPushButton#SaveBtn {
    background-color: $primary;
    color: $bg;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: bold;
}

QPushButton#SaveBtn:hover {
    background-color: $secondary;
}

QPushButton#SaveBtn:pressed {
    background-color: $primary;
}

QPushButton#DeleteBtn {
    background-color: $error;
    color: $bg;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: bold;
}

QPushButton#DeleteBtn:hover {
    background-color: $warning;
    color: $bg_secondary;
}

QPushButton#DeleteBtn:pressed {
    background-color: $error;
}

QTableWidget {
    background-color: $bg;
    color: $text;
    border: 1px solid $border;
    border-radius: 6px;
    font-size: 13px;
    outline: 0;
}

QTableWidget::item {
    padding: 4px 8px;
    border: none;
}

QTableWidget::item:selected {
    background-color: $bg_elevated;
}

QHeaderView::section {
    background-color: $bg_elevated;
    color: $text_muted;
    border: none;
    border-bottom: 1px solid $border;
    border-right: 1px solid $border;
    padding: 5px 8px;
    font-size: 12px;
    font-weight: bold;
}

QHeaderView::section:last {
    border-right: none;
}

QScrollBar:vertical {
    background: $bg;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: $border;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}
"""
)

STYLE = _TEMPLATE.substitute(QSS_COLORS)
