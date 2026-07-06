"""Map Win32 / pywin32 errors to user-friendly Chinese messages."""

from __future__ import annotations

import pywintypes


_ERROR_MAP: dict[int, str] = {
    5: "权限不足，请以管理员身份运行。",
    86: "当前密码不正确。",
    1325: "新密码不符合系统密码策略（长度、复杂度或历史记录要求）。",
    2221: "指定的用户不存在。",
    1907: "无法重置密码，账户可能被锁定或受域策略限制。",
    2245: "密码不符合密码策略要求。",
}


def _extract_codes(exc: BaseException) -> list[int]:
    codes: list[int] = []
    if isinstance(exc, pywintypes.error):
        if exc.winerror is not None:
            codes.append(int(exc.winerror))
        if exc.args:
            try:
                codes.append(int(exc.args[0]))
            except (TypeError, ValueError):
                pass
    return codes


def translate_error(exc: BaseException, *, admin_mode: bool = False) -> str:
    for code in _extract_codes(exc):
        if code in _ERROR_MAP:
            msg = _ERROR_MAP[code]
            if code == 86 and admin_mode:
                continue
            return msg
        # HRESULT-style codes
        low = code & 0xFFFF if code > 0xFFFF else code
        if low in _ERROR_MAP:
            return _ERROR_MAP[low]

    if isinstance(exc, pywintypes.error) and exc.winerror is not None:
        return f"操作失败（错误代码：{exc.winerror}），请联系管理员。"

    return f"操作失败：{exc}"
