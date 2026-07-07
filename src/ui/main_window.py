"""Main application window."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QTabWidget, QVBoxLayout, QWidget

from src.app.config import (
    APP_NAME,
    APP_SUBTITLE,
    APP_TITLE,
    WINDOW_DEFAULT_HEIGHT,
    WINDOW_DEFAULT_WIDTH,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
)
from src.services.admin import is_user_admin, relaunch_as_admin
from src.services.users import get_current_username
from src.ui.components.message_dialog import show_confirm, show_error, show_success, show_warning
from src.ui.controller import PasswordController
from src.ui.tabs.admin_reset_tab import AdminResetTab
from src.ui.tabs.self_password_tab import SelfPasswordTab
from src.utils.validators import validate_password_pair


class MainWindow(QWidget):
    def __init__(self, *, open_admin_tab: bool = False) -> None:
        super().__init__()
        self.setObjectName("MainWindow")
        self._controller = PasswordController(self)

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 16)
        root.setSpacing(0)

        title = QLabel(APP_TITLE)
        title.setObjectName("appTitle")
        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setObjectName("appSubtitle")
        root.addWidget(title)
        root.addSpacing(6)
        root.addWidget(subtitle)
        root.addSpacing(16)

        divider = QFrame()
        divider.setObjectName("headerDivider")
        divider.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(divider)
        root.addSpacing(18)

        self._current_user = get_current_username()
        self.self_tab = SelfPasswordTab(self._current_user)
        self.admin_tab = AdminResetTab(self._current_user)

        self.tabs = QTabWidget()
        self.tabs.tabBar().setExpanding(False)
        self.tabs.addTab(self.self_tab, "修改我的密码")
        self.tabs.addTab(self.admin_tab, "管理员重置他人密码")
        root.addWidget(self.tabs, 1)

        if open_admin_tab:
            self.tabs.setCurrentIndex(1)

        self._wire_signals()

    def _wire_signals(self) -> None:
        self.self_tab.actions.cancel_btn.clicked.connect(self.self_tab.clear_form)
        self.self_tab.actions.primary_btn.clicked.connect(self._submit_self_change)
        self.admin_tab.actions.cancel_btn.clicked.connect(self.admin_tab.clear_form)
        self.admin_tab.actions.primary_btn.clicked.connect(self._submit_admin_reset)
        self.admin_tab.elevate_btn.clicked.connect(self._request_elevation)
        self.tabs.currentChanged.connect(self._on_tab_changed)
        self._controller.busy_changed.connect(self._on_busy_changed)

    def _on_tab_changed(self, index: int) -> None:
        if index == 1:
            self.admin_tab.refresh()

    def _on_busy_changed(self, busy: bool) -> None:
        self.tabs.setEnabled(not busy)
        self.self_tab.set_interactive(not busy)
        self.admin_tab.set_interactive(not busy)
        if busy:
            self.setCursor(Qt.CursorShape.WaitCursor)
        else:
            self.unsetCursor()

    def _submit_self_change(self) -> None:
        form = self.self_tab.get_form()
        if not form.old_password:
            show_warning(self, "请输入当前密码。")
            return

        error = validate_password_pair(
            form.new_password,
            form.confirm_password,
            old_password=form.old_password,
        )
        if error:
            show_warning(self, error)
            return

        self._controller.change_own_password(
            self._current_user,
            form.old_password,
            form.new_password,
            on_success=self._on_self_change_success,
            on_error=lambda msg: show_error(self, msg),
        )

    def _on_self_change_success(self) -> None:
        show_success(self, "密码修改成功，请使用新密码登录。")
        self.self_tab.clear_form()

    def _submit_admin_reset(self) -> None:
        if not is_user_admin():
            show_warning(self, "请以管理员身份运行后再试。", title="权限不足")
            return

        form = self.admin_tab.get_form()
        if not form.target_user:
            show_warning(self, "请选择要重置密码的用户。")
            return

        error = validate_password_pair(form.new_password, form.confirm_password)
        if error:
            show_warning(self, error)
            return

        if not show_confirm(
            self,
            f"确定要重置用户「{form.target_user}」的密码吗？",
            title="确认重置",
        ):
            return

        target = form.target_user
        self._controller.admin_reset_password(
            target,
            form.new_password,
            on_success=lambda: self._on_admin_reset_success(target),
            on_error=lambda msg: show_error(self, msg),
        )

    def _on_admin_reset_success(self, target: str) -> None:
        show_success(self, f"已重置用户「{target}」的密码。")
        self.admin_tab.clear_form()

    def _request_elevation(self) -> None:
        if relaunch_as_admin(open_admin_tab=True):
            self.close()
        else:
            show_warning(
                self,
                "无法以管理员身份启动，请手动右键以管理员身份运行。",
                title="提权失败",
            )
