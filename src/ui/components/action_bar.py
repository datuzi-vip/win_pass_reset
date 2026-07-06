"""Standard footer with optional left action and primary buttons."""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class ActionBar(QWidget):
    def __init__(
        self,
        *,
        cancel_text: str = "取消",
        primary_text: str = "确认",
        left_widget: QWidget | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(0)

        if left_widget is not None:
            layout.addWidget(left_widget)
        layout.addStretch()

        self.cancel_btn = QPushButton(cancel_text)
        self.primary_btn = QPushButton(primary_text)
        self.primary_btn.setObjectName("primaryBtn")

        layout.addWidget(self.cancel_btn)
        layout.addSpacing(8)
        layout.addWidget(self.primary_btn)

    def set_primary_enabled(self, enabled: bool) -> None:
        self.primary_btn.setEnabled(enabled)

    def set_enabled(self, enabled: bool) -> None:
        self.cancel_btn.setEnabled(enabled)
        self.primary_btn.setEnabled(enabled)
