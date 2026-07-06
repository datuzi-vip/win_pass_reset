"""Local user enumeration and current user helpers."""

from __future__ import annotations

import win32api
import win32net
import win32netcon

# Accounts that should not appear in admin reset dropdown.
_SKIP_ACCOUNTS = frozenset(
    {
        "guest",
        "defaultaccount",
        "wdagutilityaccount",
        "krbtgt",
    }
)

# UF_ACCOUNTDISABLE
_UF_ACCOUNTDISABLE = 0x0002


def get_current_username() -> str:
    return win32api.GetUserName()


def list_local_users(*, exclude: str | None = None) -> list[str]:
    """Return login-capable local user names, sorted."""
    resume = 0
    names: list[str] = []
    while True:
        data, total, resume = win32net.NetUserEnum(
            None, 0, win32netcon.FILTER_NORMAL_ACCOUNT, resume
        )
        for entry in data:
            name = entry["name"]
            flags = entry.get("flags", 0)
            if name.lower() in _SKIP_ACCOUNTS:
                continue
            if flags & _UF_ACCOUNTDISABLE:
                continue
            if exclude and name.lower() == exclude.lower():
                continue
            names.append(name)
        if not resume:
            break
    return sorted(names, key=str.lower)
