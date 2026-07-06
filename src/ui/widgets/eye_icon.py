"""Password visibility SVG icons."""

from __future__ import annotations

from PySide6.QtGui import QIcon

from src.ui.icons import COLOR_ICON_DEFAULT, COLOR_ICON_HOVER, load_svg_icon

_EYE = "eye.svg"
_EYE_OFF = "eye-off.svg"
_SIZE = 18


def build_eye_icon(*, revealed: bool, hover: bool = False) -> QIcon:
    """Return eye icon. revealed=True means password is currently visible."""
    name = _EYE_OFF if revealed else _EYE
    color = COLOR_ICON_HOVER if hover else COLOR_ICON_DEFAULT
    return load_svg_icon(name, size=_SIZE, color=color)
