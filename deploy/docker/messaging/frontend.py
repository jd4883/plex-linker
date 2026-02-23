"""Optional logging hooks; currently no-op. Kept so existing call sites need not change."""

from typing import Any


def method_launch(g: Any) -> None:
    pass


def method_exit(g: Any) -> None:
    pass


def message_exiting_function(g: Any) -> None:
    pass
