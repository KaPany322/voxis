"""CLI notification action."""

from voxis.config.commands import ActionConfig
from voxis.actions.actions import ActionResult


class NotificationAction:
    """Print a configured message to the terminal."""

    def __call__(self, action: ActionConfig) -> ActionResult:
        message = action.parameters.get("message")
        if not isinstance(message, str) or not message:
            return ActionResult(False, "Notification action requires a non-empty 'message'.")
        print(message)
        return ActionResult(True, message)
