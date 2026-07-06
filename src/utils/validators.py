"""Form validation helpers."""

from __future__ import annotations


def validate_password_pair(
    new_password: str,
    confirm_password: str,
    *,
    old_password: str | None = None,
) -> str | None:
    if not new_password:
        return "请输入新密码。"
    if not confirm_password:
        return "请确认新密码。"
    if new_password != confirm_password:
        return "两次输入的新密码不一致。"
    if old_password is not None and new_password == old_password:
        return "新密码不能与当前密码相同。"
    return None
