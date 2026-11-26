"""Platform-aware application launcher."""

import subprocess
from typing import Sequence

from voxis.config.commands import ActionConfig
from voxis.actions.actions import ActionResult


class ApplicationAction:
    """Launch only executables present in an explicit application mapping."""

    def __init__(self, mapping: dict[str, Sequence[str]] | None = None) -> None:
        self._mapping = {
            name.lower(): list(command)
            for name, command in (mapping or {"firefox": ["firefox"]}).items()
        }

    def __call__(self, action: ActionConfig) -> ActionResult:
        name = action.parameters.get("name")
        if not isinstance(name, str) or not name.strip():
            return ActionResult(False, "Application action requires a non-empty 'name'.")
        command = self._mapping.get(name.strip().lower())
        if not command:
            return ActionResult(False, f"Application '{name}' is not in the application mapping.")
        try:
            subprocess.Popen(command, shell=False)  # noqa: S603 - executable is explicitly configured.
        except (OSError, ValueError) as exc:
            return ActionResult(False, f"Could not launch '{name}': {exc}")
        return ActionResult(True, f"Started {name}.")
