"""Reusable form layout helpers."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QLabel, QWidget

FIELD_LABEL_WIDTH = 68


def make_field_label(text: str) -> QLabel:
    label = QLabel(text)
    label.setObjectName("fieldLabel")
    label.setFixedWidth(FIELD_LABEL_WIDTH)
    label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    return label


def create_form_grid() -> QGridLayout:
    grid = QGridLayout()
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setHorizontalSpacing(10)
    grid.setVerticalSpacing(10)
    grid.setColumnStretch(1, 1)
    return grid


def add_form_row(
    grid: QGridLayout,
    row: int,
    label_text: str,
    field: QWidget,
) -> None:
    grid.addWidget(make_field_label(label_text), row, 0, Qt.AlignmentFlag.AlignVCenter)
    grid.addWidget(field, row, 1)
