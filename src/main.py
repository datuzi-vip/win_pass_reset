"""Application entry point (PyInstaller / setuptools)."""

from __future__ import annotations

from src.app.bootstrap import run


def main() -> int:
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
