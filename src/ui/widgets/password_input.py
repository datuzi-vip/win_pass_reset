"""Password input with inline visibility toggle."""

from __future__ import annotations

from PySide6.QtCore import QEvent, QSize, Qt
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QSizePolicy, QWidget

from src.ui.widgets.eye_icon import build_eye_icon


class PasswordInput(QWidget):
    def __init__(self, placeholder: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("passwordInput")
        self._visible = False
        self._hover = False

        self.input = QLineEdit()
        self.input.setObjectName("passwordField")
        self.input.setPlaceholderText(placeholder)
        self.input.setEchoMode(QLineEdit.EchoMode.Password)
        self.input.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.input.installEventFilter(self)

        self.toggle_btn = QPushButton()
        self.toggle_btn.setObjectName("toggleBtn")
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.toggle_btn.setFixedSize(30, 32)
        self.toggle_btn.setFlat(True)
        self.toggle_btn.setIconSize(QSize(18, 18))
        self.toggle_btn.installEventFilter(self)
        self._update_icon()
        self.toggle_btn.clicked.connect(self._toggle_visibility)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 2, 0)
        layout.setSpacing(0)
        layout.addWidget(self.input, 1)
        layout.addWidget(self.toggle_btn)

    def eventFilter(self, obj, event) -> bool:  # noqa: ANN001
        if obj is self.input and event.type() in (
            QEvent.Type.FocusIn,
            QEvent.Type.FocusOut,
        ):
            focused = event.type() == QEvent.Type.FocusIn
            self.setProperty("focus", "true" if focused else "false")
            self.style().unpolish(self)
            self.style().polish(self)

        if obj is self.toggle_btn:
            if event.type() == QEvent.Type.Enter:
                self._hover = True
                self._update_icon()
            elif event.type() == QEvent.Type.Leave:
                self._hover = False
                self._update_icon()

        return super().eventFilter(obj, event)

    def _update_icon(self) -> None:
        self.toggle_btn.setIcon(
            build_eye_icon(revealed=self._visible, hover=self._hover)
        )
        self.toggle_btn.setToolTip("隐藏密码" if self._visible else "显示密码")

    def _reset_visibility(self) -> None:
        self._visible = False
        self.input.setEchoMode(QLineEdit.EchoMode.Password)
        self._update_icon()

    def _toggle_visibility(self) -> None:
        self._visible = not self._visible
        self.input.setEchoMode(
            QLineEdit.EchoMode.Normal if self._visible else QLineEdit.EchoMode.Password
        )
        self._update_icon()

    def text(self) -> str:
        return self.input.text()

    def setText(self, text: str) -> None:
        self.input.setText(text)

    def clear(self) -> None:
        self.input.clear()
        self._reset_visibility()

    def setEnabled(self, enabled: bool) -> None:
        super().setEnabled(enabled)
        self.input.setEnabled(enabled)
        self.toggle_btn.setEnabled(enabled)
        self.setProperty("disabled", "true" if not enabled else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def setFocus(self) -> None:
        self.input.setFocus()
