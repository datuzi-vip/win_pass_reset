"""Orchestrates password operations between UI and services."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QObject, Signal

from src.services.errors import translate_error
from src.services.password import admin_reset_password, change_own_password
from src.ui.workers import PasswordTaskRunner


class PasswordController(QObject):
    """Runs blocking Win32 password APIs off the UI thread."""

    busy_changed = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._runner = PasswordTaskRunner()
        self._busy = False

    @property
    def busy(self) -> bool:
        return self._busy

    def _set_busy(self, busy: bool) -> None:
        if self._busy != busy:
            self._busy = busy
            self.busy_changed.emit(busy)

    def _execute(
        self,
        operation: Callable[[], None],
        *,
        admin_mode: bool,
        on_success: Callable[[], None],
        on_error: Callable[[str], None],
    ) -> None:
        if self._busy:
            return

        self._set_busy(True)

        def on_finished(success: bool, exc: object | None) -> None:
            self._set_busy(False)
            if success:
                on_success()
            elif isinstance(exc, BaseException):
                on_error(translate_error(exc, admin_mode=admin_mode))
            else:
                on_error("操作失败，请稍后重试。")

        self._runner.run(operation, on_finished)

    def change_own_password(
        self,
        username: str,
        old_password: str,
        new_password: str,
        *,
        on_success: Callable[[], None],
        on_error: Callable[[str], None],
    ) -> None:
        def operation() -> None:
            change_own_password(username, old_password, new_password)

        self._execute(operation, admin_mode=False, on_success=on_success, on_error=on_error)

    def admin_reset_password(
        self,
        username: str,
        new_password: str,
        *,
        on_success: Callable[[], None],
        on_error: Callable[[str], None],
    ) -> None:
        def operation() -> None:
            admin_reset_password(username, new_password)

        self._execute(operation, admin_mode=True, on_success=on_success, on_error=on_error)
