"""Delay action."""

import time

from voxis.config.commands import ActionConfig
from voxis.actions.actions import ActionResult


class DelayAction:
    """Wait for a non-negative number of seconds."""

    def __call__(self, action: ActionConfig) -> ActionResult:
        seconds = action.parameters.get("seconds")
        if not isinstance(seconds, (int, float)) or seconds < 0:
            return ActionResult(False, "Delay action requires non-negative numeric 'seconds'.")
        time.sleep(seconds)
        return ActionResult(True, f"Waited {seconds:g} seconds.")
