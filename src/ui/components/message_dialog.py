"""Element Plus style message dialog."""

from __future__ import annotations

from typing import Literal

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QKeyEvent
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.ui.icons import load_svg_pixmap

MessageKind = Literal["success", "info", "warning", "error"]

_KIND_META: dict[MessageKind, tuple[str, str]] = {
    "success": ("circle-check.svg", "#67c23a"),
    "info": ("info.svg", "#409eff"),
    "warning": ("triangle-alert.svg", "#e6a23c"),
    "error": ("triangle-alert.svg", "#f56c6c"),
}

_DIALOG_WIDTH = 400
_ICON_SIZE = 22


class ModalOverlay(QWidget):
    """Semi-transparent mask over the parent window."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setObjectName("modalOverlay")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setGeometry(parent.rect())
        self.raise_()
        self.show()


class MessageDialog(QDialog):
    """``el-message-box`` inspired modal dialog."""

    def __init__(
        self,
        parent: QWidget | None,
        title: str,
        message: str,
        *,
        kind: MessageKind = "success",
        button_text: str = "确定",
        confirm: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("messageDialog")
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedWidth(_DIALOG_WIDTH)
        self.setWindowFlags(
            Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 38))
        self.setGraphicsEffect(shadow)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QFrame()
        header.setObjectName("dialogHeader")
        header.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 14, 8, 14)

        title_label = QLabel(title)
        title_label.setObjectName("dialogTitle")
        close_btn = QPushButton("×")
        close_btn.setObjectName("dialogCloseBtn")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.reject)

        header_layout.addWidget(title_label, 1)
        header_layout.addWidget(close_btn, 0, Qt.AlignmentFlag.AlignVCenter)

        body = QWidget()
        body.setObjectName("dialogBody")
        body.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(16, 16, 16, 8)
        body_layout.setSpacing(10)

        icon_file, icon_color = _KIND_META[kind]
        icon_label = QLabel()
        icon_label.setFixedSize(_ICON_SIZE, _ICON_SIZE)
        icon_label.setPixmap(
            load_svg_pixmap(icon_file, size=_ICON_SIZE, color=icon_color)
        )
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        message_label = QLabel(message)
        message_label.setObjectName("dialogMessage")
        message_label.setWordWrap(True)
        message_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        message_label.setMinimumHeight(_ICON_SIZE)

        body_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignVCenter)
        body_layout.addWidget(message_label, 1, Qt.AlignmentFlag.AlignVCenter)

        footer = QFrame()
        footer.setObjectName("dialogFooter")
        footer.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(16, 4, 16, 16)
        footer_layout.setSpacing(8)
        footer_layout.addStretch()

        if confirm:
            cancel_btn = QPushButton("取消")
            cancel_btn.setMinimumWidth(80)
            cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            cancel_btn.clicked.connect(self.reject)
            footer_layout.addWidget(cancel_btn)

        ok_btn = QPushButton(button_text)
        ok_btn.setObjectName("primaryBtn")
        ok_btn.setMinimumWidth(80)
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.clicked.connect(self.accept)
        ok_btn.setDefault(True)
        ok_btn.setAutoDefault(True)
        footer_layout.addWidget(ok_btn)

        root.addWidget(header)
        root.addWidget(body)
        root.addWidget(footer)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.adjustSize()
        self.setFixedSize(_DIALOG_WIDTH, self.height())
        self._center_on_parent()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.reject()
            return
        super().keyPressEvent(event)

    def _center_on_parent(self) -> None:
        parent = self.parentWidget()
        if parent and parent.isVisible():
            center = parent.frameGeometry().center()
        else:
            screen = self.screen() or QApplication.primaryScreen()
            if screen is None:
                return
            center = screen.availableGeometry().center()

        self.move(
            center.x() - self.width() // 2,
            center.y() - self.height() // 2,
        )


def _run_dialog(dialog: MessageDialog) -> int:
    overlay: ModalOverlay | None = None
    parent = dialog.parentWidget()
    if parent is not None:
        overlay = ModalOverlay(parent)

        def _cleanup(_result: int = 0) -> None:
            if overlay is not None:
                overlay.deleteLater()

        dialog.finished.connect(_cleanup)
    return dialog.exec()


def show_message(
    parent: QWidget | None,
    message: str,
    *,
    title: str = "提示",
    kind: MessageKind = "info",
    button_text: str = "确定",
) -> int:
    dialog = MessageDialog(parent, title, message, kind=kind, button_text=button_text)
    return _run_dialog(dialog)


def show_success(
    parent: QWidget | None,
    message: str,
    *,
    title: str = "成功",
) -> None:
    show_message(parent, message, title=title, kind="success")


def show_warning(
    parent: QWidget | None,
    message: str,
    *,
    title: str = "提示",
) -> None:
    show_message(parent, message, title=title, kind="warning")


def show_error(
    parent: QWidget | None,
    message: str,
    *,
    title: str = "失败",
) -> None:
    show_message(parent, message, title=title, kind="error")


def show_confirm(
    parent: QWidget | None,
    message: str,
    *,
    title: str = "提示",
    button_text: str = "确定",
) -> bool:
    dialog = MessageDialog(
        parent,
        title,
        message,
        kind="warning",
        button_text=button_text,
        confirm=True,
    )
    return _run_dialog(dialog) == QDialog.DialogCode.Accepted
