"""Exact-match command resolution."""

from voxis.config.commands import Command, CommandConfig


class CommandResolver:
    """Resolve normalized user text to a configured command."""

    def __init__(self, config: CommandConfig) -> None:
        self._commands = config.commands
        self._trigger_map = {
            self.normalize(trigger): command
            for command in self._commands
            for trigger in command.triggers
        }

    @staticmethod
    def normalize(text: str) -> str:
        """Trim surrounding whitespace and lowercase text."""
        return text.strip().lower()

    def resolve(self, text: str) -> Command | None:
        """Return the command with an exact normalized trigger, if any."""
        return self._trigger_map.get(self.normalize(text))
