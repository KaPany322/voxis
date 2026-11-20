from voxis.config.commands import CommandConfig
from voxis.core.command_resolver import CommandResolver


def test_normalization_and_exact_matching() -> None:
    config = CommandConfig.model_validate({"commands": [{
        "name": "Open Firefox", "triggers": ["open firefox", "start firefox"],
        "actions": [{"type": "notification", "parameters": {"message": "ok"}}]
    }]})
    resolver = CommandResolver(config)
    assert resolver.resolve("  OPEN FIREFOX  ").name == "Open Firefox"
    assert resolver.resolve("open firefox please") is None


def test_unknown_command() -> None:
    resolver = CommandResolver(CommandConfig(commands=[]))
    assert resolver.resolve("unknown") is None
