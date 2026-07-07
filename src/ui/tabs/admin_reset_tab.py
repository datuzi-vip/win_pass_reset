"""Administrator password reset tab."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import QComboBox, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from src.services.admin import is_user_admin
from src.services.users import list_local_users
from src.ui.components.action_bar import ActionBar
from src.ui.components.alert_label import AlertLabel
from src.ui.components.form import add_form_row, create_form_grid
from src.ui.widgets.password_input import PasswordInput

_PLACEHOLDER = "请选择用户"
_NO_PERMISSION = "需要管理员权限"


@dataclass(frozen=True)
class AdminResetForm:
    target_user: str
    new_password: str
    confirm_password: str


class AdminResetTab(QWidget):
    def __init__(self, current_user: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._current_user = current_user

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        self.alert = AlertLabel(
            "需要管理员权限，将重置指定用户的密码。",
            variant="warning",
        )
        layout.addWidget(self.alert)

        grid = create_form_grid()

        self.user_combo = QComboBox()
        self.user_combo.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        self.new_password = PasswordInput("请输入新密码")
        self.confirm_password = PasswordInput("请再次输入新密码")

        add_form_row(grid, 0, "目标用户", self.user_combo)
        add_form_row(grid, 1, "新密码", self.new_password)
        add_form_row(grid, 2, "确认密码", self.confirm_password)
        layout.addLayout(grid)

        info = AlertLabel(
            "无需输入旧密码；用户下次登录需使用新密码。",
            variant="info",
        )
        layout.addWidget(info)

        layout.addStretch(1)

        self.elevate_btn = QPushButton("以管理员身份运行")
        self.elevate_btn.setObjectName("linkBtn")

        self.actions = ActionBar(
            cancel_text="取消",
            primary_text="确认重置",
            left_widget=self.elevate_btn,
        )
        layout.addWidget(self.actions)

        self._admin = False
        self._users_loaded = False
        self.refresh()

    def refresh(self, *, force_users: bool = False) -> None:
        admin = is_user_admin()
        admin_changed = admin != self._admin
        self._admin = admin

        self.elevate_btn.setVisible(not admin)
        self.actions.set_primary_enabled(admin)

        if force_users or admin_changed or (admin and not self._users_loaded):
            self._reload_users(admin)
            self._users_loaded = admin
        elif admin:
            self.user_combo.setEnabled(True)
        else:
            self.user_combo.setEnabled(False)

    def _reload_users(self, admin: bool) -> None:
        self.user_combo.clear()
        if not admin:
            self.user_combo.addItem(_NO_PERMISSION)
            self.user_combo.setEnabled(False)
            return

        self.user_combo.setEnabled(True)
        self.user_combo.addItem(_PLACEHOLDER)
        users = list_local_users(exclude=self._current_user)
        for name in users:
            self.user_combo.addItem(name)
        self.user_combo.setCurrentIndex(0)

    def get_form(self) -> AdminResetForm:
        target = self.user_combo.currentText()
        if target in (_PLACEHOLDER, _NO_PERMISSION, ""):
            target = ""
        return AdminResetForm(
            target_user=target,
            new_password=self.new_password.text(),
            confirm_password=self.confirm_password.text(),
        )

    def clear_form(self) -> None:
        self.new_password.clear()
        self.confirm_password.clear()
        if self.user_combo.isEnabled() and self.user_combo.count() > 0:
            self.user_combo.setCurrentIndex(0)

    def set_interactive(self, enabled: bool) -> None:
        self.new_password.setEnabled(enabled)
        self.confirm_password.setEnabled(enabled)
        self.elevate_btn.setEnabled(enabled)
        self.actions.set_enabled(enabled)
        if enabled:
            self.elevate_btn.setVisible(not self._admin)
            self.actions.set_primary_enabled(self._admin)
            self.user_combo.setEnabled(self._admin)
        else:
            self.user_combo.setEnabled(False)
