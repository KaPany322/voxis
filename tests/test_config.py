import json

import pytest
from pydantic import ValidationError

from voxis.config.commands import CommandConfig, load_command_config


def test_valid_config_and_loader(tmp_path) -> None:
    data = {"commands": [{"name": "Note", "triggers": ["note"], "actions": [
        {"type": "notification", "parameters": {"message": "hello"}},
        {"type": "delay", "parameters": {"seconds": 1}}
    ], "response": "Done"}]}
    path = tmp_path / "commands.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    config = load_command_config(path)
    assert len(config.commands[0].actions) == 2
    assert CommandConfig.model_validate(data) == config


def test_invalid_config_rejected() -> None:
    with pytest.raises(ValidationError):
        CommandConfig.model_validate({"commands": [{"name": "Empty", "triggers": [], "actions": []}]})


def test_duplicate_triggers_rejected_case_insensitively() -> None:
    with pytest.raises(ValidationError):
        CommandConfig.model_validate({"commands": [
            {"name": "First", "triggers": ["open"], "actions": [{"type": "x"}]},
            {"name": "Second", "triggers": [" OPEN "], "actions": [{"type": "x"}]}
        ]})
