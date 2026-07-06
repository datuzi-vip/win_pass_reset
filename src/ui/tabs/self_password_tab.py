"""Self-service password change tab."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import QLineEdit, QSizePolicy, QVBoxLayout, QWidget

from src.ui.components.action_bar import ActionBar
from src.ui.components.alert_label import AlertLabel
from src.ui.components.form import add_form_row, create_form_grid
from src.ui.widgets.password_input import PasswordInput


@dataclass(frozen=True)
class SelfPasswordForm:
    old_password: str
    new_password: str
    confirm_password: str


class SelfPasswordTab(QWidget):
    def __init__(self, username: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        grid = create_form_grid()

        self.username_field = QLineEdit(username)
        self.username_field.setObjectName("readOnlyField")
        self.username_field.setReadOnly(True)
        self.username_field.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.old_password = PasswordInput("请输入当前密码")
        self.new_password = PasswordInput("请输入新密码")
        self.confirm_password = PasswordInput("请再次输入新密码")

        add_form_row(grid, 0, "用户名", self.username_field)
        add_form_row(grid, 1, "当前密码", self.old_password)
        add_form_row(grid, 2, "新密码", self.new_password)
        add_form_row(grid, 3, "确认密码", self.confirm_password)
        layout.addLayout(grid)

        info = AlertLabel("需输入当前密码才能修改。", variant="info")
        layout.addWidget(info)

        layout.addStretch(1)

        self.actions = ActionBar(cancel_text="取消", primary_text="确认修改")
        layout.addWidget(self.actions)

    def get_form(self) -> SelfPasswordForm:
        return SelfPasswordForm(
            old_password=self.old_password.text(),
            new_password=self.new_password.text(),
            confirm_password=self.confirm_password.text(),
        )

    def clear_form(self) -> None:
        self.old_password.clear()
        self.new_password.clear()
        self.confirm_password.clear()

    def set_interactive(self, enabled: bool) -> None:
        self.old_password.setEnabled(enabled)
        self.new_password.setEnabled(enabled)
        self.confirm_password.setEnabled(enabled)
        self.actions.set_enabled(enabled)
