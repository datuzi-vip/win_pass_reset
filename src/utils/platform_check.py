"""Windows version check — reject Win7 / Server 2008 R2."""

from __future__ import annotations

import platform
import sys


MIN_BUILD = 9600  # Windows 8.1 / Server 2012 R2


def get_windows_build() -> int:
    version = platform.version()
    try:
        return int(version.split(".")[-1])
    except (ValueError, IndexError):
        return 0


def is_supported_windows() -> bool:
    if sys.platform != "win32":
        return False
    return get_windows_build() >= MIN_BUILD


def unsupported_message() -> str:
    return (
        "本工具需要 Windows 8.1 或更高版本。\n"
        "不支持 Windows 7 及 Windows Server 2008 R2。"
    )
