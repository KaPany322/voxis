"""Pydantic models and loading helpers for command configuration."""

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ActionConfig(BaseModel):
    """Configuration for one action invocation."""

    model_config = ConfigDict(extra="forbid")

    type: str = Field(min_length=1)
    parameters: dict[str, Any] = Field(default_factory=dict)

    @field_validator("type")
    @classmethod
    def nonblank_type(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Action type cannot be blank.")
        return value.strip().lower()


class Command(BaseModel):
    """A named command, its trigger phrases, actions and optional response."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    triggers: list[str] = Field(min_length=1)
    actions: list[ActionConfig] = Field(min_length=1)
    response: str | None = None

    @field_validator("name")
    @classmethod
    def nonblank_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Command name cannot be blank.")
        return value.strip()

    @field_validator("triggers")
    @classmethod
    def valid_triggers(cls, values: list[str]) -> list[str]:
        cleaned = [value.strip() for value in values]
        if any(not value for value in cleaned):
            raise ValueError("Trigger phrases cannot be blank.")
        return cleaned


class CommandConfig(BaseModel):
    """Top-level command configuration."""

    model_config = ConfigDict(extra="forbid")

    commands: list[Command]

    @model_validator(mode="after")
    def unique_triggers(self) -> "CommandConfig":
        seen: dict[str, str] = {}
        for command in self.commands:
            for trigger in command.triggers:
                normalized = trigger.strip().lower()
                if normalized in seen:
                    raise ValueError(
                        f"Trigger '{trigger}' is duplicated in commands "
                        f"'{seen[normalized]}' and '{command.name}'."
                    )
                seen[normalized] = command.name
        return self


def load_command_config(path: str | Path) -> CommandConfig:
    """Load and validate commands from a JSON file."""
    with Path(path).open("r", encoding="utf-8") as config_file:
        data = json.load(config_file)
    return CommandConfig.model_validate(data)
