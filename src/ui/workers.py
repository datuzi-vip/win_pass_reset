"""Background worker for password operations."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal, Slot
from PySide6.QtWidgets import QApplication


class PasswordWorkerSignals(QObject):
    finished = Signal(bool, object)


class PasswordWorker(QRunnable):
    def __init__(self, operation: Callable[[], None]) -> None:
        super().__init__()
        self._operation = operation
        app = QApplication.instance()
        self.signals = PasswordWorkerSignals(app)

    @Slot()
    def run(self) -> None:
        try:
            self._operation()
            self.signals.finished.emit(True, None)
        except Exception as exc:
            self.signals.finished.emit(False, exc)


class PasswordTaskRunner:
    def run(
        self,
        operation: Callable[[], None],
        on_finished: Callable[[bool, object | None], None],
    ) -> None:
        worker = PasswordWorker(operation)
        worker.signals.finished.connect(on_finished)
        QThreadPool.globalInstance().start(worker)
