"""Administrator privilege detection and UAC elevation."""

from __future__ import annotations

import ctypes
import sys


def is_user_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except OSError:
        return False


def relaunch_as_admin(*, open_admin_tab: bool = False) -> bool:
    """Restart the current app elevated. Returns False if launch failed."""
    params = " ".join(
        arg for arg in sys.argv[1:] if arg != "--admin-tab"
    )
    if open_admin_tab:
        params = (params + " --admin-tab").strip()

    executable = sys.executable
    if getattr(sys, "frozen", False):
        executable = sys.argv[0]

    result = ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        executable,
        params or None,
        None,
        1,
    )
    return result > 32
