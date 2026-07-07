"""Element Plus el-alert component."""

from __future__ import annotations

from typing import Literal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

from src.ui.icons import load_svg_pixmap
from src.ui.styles import PRIMARY, WARNING

AlertVariant = Literal["info", "warning"]

# Element Plus alert icon visual size (slightly larger for clarity)
_ICON_SIZE = 20
_ICON_FILES = {
    "info": "info.svg",
    "warning": "triangle-alert.svg",
}
_ICON_COLORS = {
    "info": PRIMARY,
    "warning": WARNING,
}


class AlertLabel(QFrame):
    """Light-style ``el-alert`` with icon + description."""

    def __init__(
        self,
        text: str,
        *,
        variant: AlertVariant = "info",
        parent=None,
    ) -> None:
        super().__init__(parent)
        object_name = "alertInfo" if variant == "info" else "alertWarning"
        self.setObjectName(object_name)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        root = QHBoxLayout(self)
        root.setContentsMargins(16, 8, 16, 8)
        root.setSpacing(8)

        icon_box = QFrame()
        icon_box.setObjectName("alertIconBox")
        icon_box.setFixedSize(_ICON_SIZE, _ICON_SIZE)
        icon_box.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        icon_layout = QHBoxLayout(icon_box)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setSpacing(0)

        icon_label = QLabel()
        icon_label.setObjectName("alertIcon")
        icon_label.setFixedSize(_ICON_SIZE, _ICON_SIZE)
        icon_label.setPixmap(
            load_svg_pixmap(
                _ICON_FILES[variant],
                size=_ICON_SIZE,
                color=_ICON_COLORS[variant],
            )
        )
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label)

        content = QWidget()
        content.setObjectName("alertContent")
        content.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        desc = QLabel(text)
        desc.setObjectName("alertText")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        content_layout.addWidget(desc)

        root.addWidget(icon_box, 0, Qt.AlignmentFlag.AlignVCenter)
        root.addWidget(content, 1)
