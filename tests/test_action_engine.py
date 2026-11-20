from voxis.config.commands import Command
from voxis.core.action_engine import ActionEngine
from voxis.core.registry import ActionRegistry, ActionResult


def test_sequential_actions() -> None:
    events: list[str] = []
    registry = ActionRegistry()
    registry.register("one", lambda action: (events.append("one") or ActionResult(True)))
    registry.register("two", lambda action: (events.append("two") or ActionResult(True)))
    command = Command.model_validate({"name": "sequence", "triggers": ["go"], "actions": [
        {"type": "one"}, {"type": "two"}
    ]})
    result = ActionEngine(registry).execute(command)
    assert result.success
    assert events == ["one", "two"]


def test_failure_stops_sequence_and_identifies_action() -> None:
    events: list[str] = []
    registry = ActionRegistry()
    registry.register("fail", lambda action: ActionResult(False, "nope"))
    registry.register("later", lambda action: (events.append("later") or ActionResult(True)))
    command = Command.model_validate({"name": "sequence", "triggers": ["go"], "actions": [
        {"type": "fail"}, {"type": "later"}
    ]})
    result = ActionEngine(registry).execute(command)
    assert not result.success
    assert result.failed_action_index == 0
    assert result.message == "nope"
    assert events == []
