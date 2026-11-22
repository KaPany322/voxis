"""Registry for action handlers."""

from typing import Protocol
from collections.abc import Sequence

from voxis.config.commands import ActionConfig, Command, CommandConfig


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

    def __init__(self, config: CommandConfig) -> None:
        from voxis.actions.application import ApplicationAction
        from voxis.actions.delay import DelayAction
        from voxis.actions.notification import NotificationAction

        self._commands = config.commands
        self._handlers: dict[str, ActionHandler] = {
            "application": ApplicationAction(
                {
                    "firefox": ["firefox"],
                    "dota2": [
                        "powershell.exe",
                        "-NoProfile",
                        "-Command",
                        "Start-Process 'steam://rungameid/570'",
                    ],
                    "dota2page": [
                        "powershell.exe",
                        "-NoProfile",
                        "-Command",
                        "Start-Process 'https://www.youtube.com/watch?v=s1z5bFRc0qY&list=PLz-r6ePUJBv8azJ3jgFGB7-q4ipPxXiK-&index=1'",
                    ],
                }
            ),
            "notification": NotificationAction(),
            "delay": DelayAction()
        }
        self._trigger_map = {
            self.normalize(trigger): command
            for command in self._commands
            for trigger in command.triggers
        }

    @staticmethod
    def normalize(text: str) -> str:
        """Trim surrounding whitespace and lowercase text."""
        return text.strip().lower()

    def register(self, action_type: str, handler: ActionHandler) -> None:
        """Register or replace a handler for an action type."""
        key = self.normalize(action_type)
        if not key:
            raise ValueError("Action type cannot be empty.")
        self._handlers[key] = handler

    def get(self, action_type: str) -> ActionHandler | None:
        """Look up a handler by action type, case-insensitively."""
        return self._handlers.get(self.normalize(action_type))

    def resolve(self, text: str) -> Command | None:
        """Return the command with an exact normalized trigger, if any."""
        return self._trigger_map.get(self.normalize(text))
