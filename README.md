# Voxis

Voxis is an open-source, modular command engine for a future voice assistant. Phase 1 accepts typed text, resolves exact trigger phrases and runs configured actions. It does not include speech recognition, wake-word detection, AI, a GUI or external plugins.

## Architecture

- `config.commands` validates JSON command definitions with Pydantic.
- `core.command_resolver` normalizes input and performs exact trigger matching.
- `core.registry` maps action type names to handlers.
- `core.action_engine` executes actions in order and stops at the first failure.
- `actions` contains the application, notification and delay handlers.
- `main` wires the modules together for an interactive CLI.

## Installation

Requires Python 3.12 or newer.

```sh
python -m venv .venv
# Activate the virtual environment, then:
python -m pip install -e ".[dev]"
```

## Run

From the project root:

```sh
voxis
# or choose another configuration:
voxis --config path/to/commands.json
```

Type `exit` or `quit` to leave. You can also run `python -m voxis.main` after installing the package.

## Add commands

Edit `config/commands.json`. Every command needs a name, one or more unique trigger phrases and at least one action. Matching trims whitespace and ignores case, but otherwise requires an exact trigger. An optional `response` is printed after every action succeeds.

```json
{
  "commands": [
    {
      "name": "Notify me",
      "triggers": ["notify me", "show a note"],
      "actions": [
        {"type": "notification", "parameters": {"message": "Hello!"}}
      ],
      "response": "Notification sent."
    }
  ]
}
```

## Action registry and built-in actions

The registry maps an action's `type` to a callable handler. The default registry includes `application`, `notification` and `delay`. Handlers receive a validated `ActionConfig` and return an `ActionResult` with a success flag and optional message.

Application launching is deliberately explicit: by default, the mapping contains `firefox` → `firefox`. Applications are started with `subprocess.Popen` and `shell=False`. To customize this mapping in an embedding application, pass a mapping of friendly names to argument lists to `create_default_registry`, for example `{"browser": ["C:/Program Files/Browser/browser.exe"]}`. The executable must be installed and available at that path (or on `PATH`); Voxis does not search for applications.

To add a built-in action, create a callable handler that accepts `ActionConfig` and returns `ActionResult`, register it by type using `ActionRegistry.register`, and add it to `create_default_registry` if it should be available in the CLI. Keep the handler responsible for validating its own required parameters.
