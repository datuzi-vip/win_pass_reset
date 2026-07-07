"""SVG icon loading utilities."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication

from src.ui.styles import COLOR_ICON_DEFAULT
from src.utils.resources import resource_path

_ICON_DIR = resource_path("resources", "icons")


def icon_file(name: str) -> Path:
    return _ICON_DIR / name


def _device_pixel_ratio() -> float:
    app = QApplication.instance()
    if app is None:
        return 1.0
    screen = app.primaryScreen()
    return screen.devicePixelRatio() if screen else 1.0


def _read_svg(name: str, color: str) -> bytes:
    path = icon_file(name)
    if not path.exists():
        return b""
    content = path.read_text(encoding="utf-8")
    content = content.replace("currentColor", color)
    return content.encode("utf-8")


def svg_to_pixmap(name: str, size: int, *, color: str = COLOR_ICON_DEFAULT) -> QPixmap:
    svg_data = _read_svg(name, color)
    if not svg_data:
        return QPixmap()

    renderer = QSvgRenderer(svg_data)
    ratio = _device_pixel_ratio()
    physical = max(1, int(size * ratio))
    pixmap = QPixmap(physical, physical)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()
    pixmap.setDevicePixelRatio(ratio)
    return pixmap


def load_svg_icon(
    name: str,
    size: int = 20,
    *,
    color: str = COLOR_ICON_DEFAULT,
) -> QIcon:
    pixmap = svg_to_pixmap(name, size, color=color)
    if pixmap.isNull():
        return QIcon()
    return QIcon(pixmap)


def load_svg_pixmap(
    name: str,
    size: int = 16,
    *,
    color: str = COLOR_ICON_DEFAULT,
) -> QPixmap:
    return svg_to_pixmap(name, size, color=color)
