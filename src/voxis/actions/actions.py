from typing import Protocol

from voxis.config.commands import ActionConfig

class ActionHandler(Protocol):
    """Callable interface implemented by action handlers."""

    def __call__(self, action: ActionConfig) -> "ActionResult": ...


class ActionResult:
    """Structured outcome of running one action."""

    def __init__(self, success: bool, message: str | None = None) -> None:
        self.success = success
        self.message = message
