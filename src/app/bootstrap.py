"""Application bootstrap and QApplication setup."""

from __future__ import annotations

import argparse
import sys

from PySide6.QtWidgets import QApplication

from src.app.config import CLI_ADMIN_TAB
from src.ui.components.message_dialog import show_error
from src.ui.main_window import MainWindow
from src.ui.styles import load_stylesheet
from src.utils.platform_check import is_supported_windows, unsupported_message


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="WinPassReset")
    parser.add_argument(
        CLI_ADMIN_TAB,
        action="store_true",
        help="启动后直接进入管理员重置标签页",
    )
    return parser.parse_args(argv)


def create_application() -> QApplication:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(load_stylesheet())
    return app


def run(argv: list[str] | None = None) -> int:
    if not is_supported_windows():
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        app.setStyleSheet(load_stylesheet())
        show_error(None, unsupported_message(), title="系统版本不支持")
        return 1

    args = parse_args(argv)
    app = create_application()
    window = MainWindow(open_admin_tab=args.admin_tab)
    window.show()
    return app.exec()
