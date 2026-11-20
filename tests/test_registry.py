from voxis.core.registry import ActionRegistry, ActionResult


def test_register_and_lookup() -> None:
    registry = ActionRegistry()
    handler = lambda action: ActionResult(True)  # noqa: E731
    registry.register("Notification", handler)
    assert registry.get("notification") is handler
    assert registry.get("missing") is None
