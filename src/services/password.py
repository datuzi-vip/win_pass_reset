"""Password change and admin reset via win32net."""

from __future__ import annotations

import win32net

from src.app.config import USER_INFO_PASSWORD


def change_own_password(
    username: str,
    old_password: str,
    new_password: str,
    server: str | None = None,
) -> None:
    win32net.NetUserChangePassword(server, username, old_password, new_password)


def admin_reset_password(
    username: str,
    new_password: str,
    server: str | None = None,
) -> None:
    win32net.NetUserSetInfo(
        server,
        username,
        USER_INFO_PASSWORD,
        {"password": new_password},
    )
