"""Sequential command action execution."""

from dataclasses import dataclass

from voxis.config.commands import Command
from voxis.core.registry import Registry
from voxis.actions.actions import ActionResult


@dataclass(frozen=True)
class ExecutionResult:
    """Outcome of executing a command's action sequence."""

    success: bool
    message: str | None = None
    failed_action_index: int | None = None
    action_results: tuple[ActionResult, ...] = ()


class ActionEngine:
    """Execute each command action in order, stopping at the first failure."""

    def __init__(self, registry: Registry) -> None:
        self._registry = registry

    def execute(self, command: Command) -> ExecutionResult:
        """Run a command and report the first failed action, if present."""
        results: list[ActionResult] = []
        for index, action in enumerate(command.actions):
            handler = self._registry.get(action.type)
            if handler is None:
                result = ActionResult(False, f"No handler registered for action '{action.type}'.")
            else:
                try:
                    result = handler(action)
                    if not isinstance(result, ActionResult):
                        result = ActionResult(False, "Action handler returned an invalid result.")
                except Exception as exc:  # Keep handler failures from terminating the CLI.
                    result = ActionResult(False, str(exc) or exc.__class__.__name__)
            results.append(result)
            if not result.success:
                return ExecutionResult(
                    success=False,
                    message=result.message,
                    failed_action_index=index,
                    action_results=tuple(results),
                )
        return ExecutionResult(success=True, action_results=tuple(results))
