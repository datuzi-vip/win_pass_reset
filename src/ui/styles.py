"""Element Plus design tokens and QSS stylesheet."""

from __future__ import annotations

# Element Plus color palette
PRIMARY = "#409eff"
PRIMARY_HOVER = "#66b1ff"
PRIMARY_ACTIVE = "#3a8ee6"
PRIMARY_LIGHT = "#ecf5ff"

WARNING = "#e6a23c"
WARNING_LIGHT = "#fdf6ec"

INFO = "#909399"
INFO_LIGHT = "#f4f4f5"

TEXT_PRIMARY = "#303133"
TEXT_REGULAR = "#606266"
TEXT_SECONDARY = "#909399"
TEXT_PLACEHOLDER = "#a8abb2"

BORDER = "#dcdfe6"
BORDER_HOVER = "#c0c4cc"
BORDER_LIGHT = "#e4e7ed"

BG = "#ffffff"
FILL_LIGHT = "#f5f7fa"

RADIUS = "4px"

# Icon tint colors (used by icons.py and password_input)
COLOR_ICON_DEFAULT = TEXT_SECONDARY
COLOR_ICON_HOVER = PRIMARY


def load_stylesheet() -> str:
    return f"""
* {{
    font-family: "Segoe UI", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
}}

QWidget {{
    color: {TEXT_REGULAR};
    background: transparent;
}}

QWidget#MainWindow {{
    background: {BG};
}}

QLabel#appTitle {{
    font-size: 18px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    padding: 0;
}}

QLabel#appSubtitle {{
    font-size: 13px;
    color: {TEXT_SECONDARY};
    padding: 0;
}}

QFrame#headerDivider {{
    background: {BORDER_LIGHT};
    max-height: 1px;
    border: none;
    margin: 0;
}}

QLabel#fieldLabel {{
    color: {TEXT_REGULAR};
    font-size: 14px;
    padding-right: 4px;
}}

/* Element Plus el-alert --info.is-light */
QFrame#alertInfo {{
    background-color: {PRIMARY_LIGHT};
    border: 1px solid #d9ecff;
    border-radius: {RADIUS};
    min-height: 36px;
}}

QFrame#alertInfo QWidget#alertContent,
QFrame#alertInfo QFrame#alertIconBox,
QFrame#alertInfo QLabel#alertIcon {{
    background: transparent;
    border: none;
}}

QFrame#alertInfo QLabel#alertText {{
    color: {PRIMARY};
    font-size: 14px;
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
}}

/* Element Plus el-alert --warning.is-light */
QFrame#alertWarning {{
    background-color: {WARNING_LIGHT};
    border: 1px solid #faecd8;
    border-radius: {RADIUS};
    min-height: 36px;
}}

QFrame#alertWarning QWidget#alertContent,
QFrame#alertWarning QFrame#alertIconBox,
QFrame#alertWarning QLabel#alertIcon {{
    background: transparent;
    border: none;
}}

QFrame#alertWarning QLabel#alertText {{
    color: {WARNING};
    font-size: 14px;
    background: transparent;
    border: none;
    padding: 0;
    margin: 0;
}}

QLineEdit, QComboBox {{
    min-height: 32px;
    max-height: 32px;
    padding: 0 11px;
    border: 1px solid {BORDER};
    border-radius: {RADIUS};
    background: {BG};
    color: {TEXT_REGULAR};
    selection-background-color: {PRIMARY};
    selection-color: white;
}}

QLineEdit:hover, QComboBox:hover {{
    border-color: {BORDER_HOVER};
}}

QLineEdit:focus, QComboBox:focus {{
    border-color: {PRIMARY};
    outline: none;
}}

QLineEdit#readOnlyField {{
    background: {FILL_LIGHT};
    color: {TEXT_SECONDARY};
}}

QLineEdit#readOnlyField:hover {{
    border-color: {BORDER};
}}

QLineEdit::placeholder {{
    color: {TEXT_PLACEHOLDER};
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 30px;
    border: none;
}}

QComboBox QAbstractItemView {{
    border: 1px solid {BORDER_LIGHT};
    border-radius: {RADIUS};
    background: {BG};
    selection-background-color: {PRIMARY_LIGHT};
    selection-color: {PRIMARY};
    padding: 4px 0;
    outline: none;
}}

QComboBox:disabled {{
    background: {FILL_LIGHT};
    color: {TEXT_PLACEHOLDER};
    border-color: {BORDER_LIGHT};
}}

QWidget#passwordInput {{
    background-color: {BG};
    border: 1px solid {BORDER};
    border-radius: {RADIUS};
    min-height: 32px;
    max-height: 32px;
}}

QWidget#passwordInput:hover {{
    border-color: {BORDER_HOVER};
}}

QWidget#passwordInput[focus="true"] {{
    border-color: {PRIMARY};
}}

QWidget#passwordInput[disabled="true"] {{
    background-color: {FILL_LIGHT};
    border-color: {BORDER_LIGHT};
}}

QWidget#passwordInput[disabled="true"] QLineEdit#passwordField {{
    color: {TEXT_PLACEHOLDER};
}}

QLineEdit#passwordField {{
    border: none;
    background: transparent;
    min-height: 30px;
    max-height: 30px;
    padding: 0 4px 0 11px;
    margin: 0;
}}

QLineEdit#passwordField:focus {{
    border: none;
}}

QPushButton#toggleBtn {{
    border: none;
    background: transparent;
    border-radius: {RADIUS};
    padding: 0;
    margin: 0;
    min-width: 30px;
    max-width: 30px;
    min-height: 32px;
    max-height: 32px;
}}

QPushButton#toggleBtn:hover {{
    background: {PRIMARY_LIGHT};
}}

QPushButton#toggleBtn:disabled {{
    background: transparent;
}}

QTabWidget::pane {{
    border: none;
    background: transparent;
    top: 0;
    padding: 12px 0 0 0;
}}

QTabWidget::tab-bar {{
    alignment: left;
}}

QTabBar {{
    background: transparent;
    border-bottom: 1px solid {BORDER_LIGHT};
}}

QTabBar::tab {{
    background: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    padding: 10px 4px;
    margin-right: 24px;
    margin-bottom: -1px;
    color: {TEXT_PRIMARY};
}}

QTabBar::tab:selected {{
    color: {PRIMARY};
    border-bottom: 2px solid {PRIMARY};
    font-weight: 500;
}}

QTabBar::tab:hover:!selected {{
    color: {PRIMARY};
}}

QPushButton {{
    min-height: 32px;
    min-width: 80px;
    padding: 0 15px;
    border: 1px solid {BORDER};
    border-radius: {RADIUS};
    background: {BG};
    color: {TEXT_REGULAR};
}}

QPushButton:hover {{
    color: {PRIMARY};
    border-color: #c6e2ff;
    background: {PRIMARY_LIGHT};
}}

QPushButton:pressed {{
    background: #d9ecff;
}}

QPushButton#primaryBtn {{
    background: {PRIMARY};
    border-color: {PRIMARY};
    color: white;
    font-weight: 500;
}}

QPushButton#primaryBtn:hover {{
    background: {PRIMARY_HOVER};
    border-color: {PRIMARY_HOVER};
    color: white;
}}

QPushButton#primaryBtn:pressed {{
    background: {PRIMARY_ACTIVE};
    border-color: {PRIMARY_ACTIVE};
}}

QPushButton#primaryBtn:disabled {{
    background: #a0cfff;
    border-color: #a0cfff;
    color: white;
}}

QPushButton#linkBtn {{
    border: none;
    color: {PRIMARY};
    background: transparent;
    text-align: left;
    padding: 0 4px;
    min-width: 0;
    min-height: 32px;
    font-size: 14px;
}}

QPushButton#linkBtn:hover {{
    color: {PRIMARY_HOVER};
    background: transparent;
}}

/* Modal mask */
QWidget#modalOverlay {{
    background-color: rgba(0, 0, 0, 0.45);
}}

/* Element Plus el-message-box */
QDialog#messageDialog {{
    background-color: {BG};
    border: 1px solid {BORDER_LIGHT};
    border-radius: 6px;
}}

QFrame#dialogHeader {{
    background-color: {BG};
    border: none;
    border-bottom: 1px solid {BORDER_LIGHT};
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}}

QLabel#dialogTitle {{
    color: {TEXT_PRIMARY};
    font-size: 15px;
    font-weight: 600;
    background: transparent;
}}

QPushButton#dialogCloseBtn {{
    border: none;
    background: transparent;
    color: {TEXT_SECONDARY};
    font-size: 18px;
    min-width: 28px;
    min-height: 28px;
    padding: 0;
}}

QPushButton#dialogCloseBtn:hover {{
    color: {PRIMARY};
    background: {PRIMARY_LIGHT};
    border: none;
    border-radius: {RADIUS};
}}

QWidget#dialogBody {{
    background-color: {BG};
}}

QLabel#dialogMessage {{
    color: {TEXT_REGULAR};
    font-size: 14px;
    background: transparent;
}}

QFrame#dialogFooter {{
    background-color: {BG};
    border: none;
}}
"""
