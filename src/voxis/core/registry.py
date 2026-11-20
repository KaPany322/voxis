"""Registry for action handlers."""

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


class ActionRegistry:
    """Map action type names to callable handlers."""

    def __init__(self) -> None:
        self._handlers: dict[str, ActionHandler] = {}

    def register(self, action_type: str, handler: ActionHandler) -> None:
        """Register or replace a handler for an action type."""
        key = action_type.strip().lower()
        if not key:
            raise ValueError("Action type cannot be empty.")
        self._handlers[key] = handler

    def get(self, action_type: str) -> ActionHandler | None:
        """Look up a handler by action type, case-insensitively."""
        return self._handlers.get(action_type.strip().lower())
