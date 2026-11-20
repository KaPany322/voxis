"""Built-in action handlers."""

from collections.abc import Sequence

from voxis.actions.application import ApplicationAction
from voxis.actions.delay import DelayAction
from voxis.actions.notification import NotificationAction
from voxis.core.registry import ActionRegistry


def create_default_registry(
    application_mapping: dict[str, Sequence[str]] | None = None,
) -> ActionRegistry:
    """Create a registry populated with the built-in handlers."""
    registry = ActionRegistry()
    registry.register("application", ApplicationAction(application_mapping))
    registry.register("notification", NotificationAction())
    registry.register("delay", DelayAction())
    return registry


__all__ = ["create_default_registry"]
