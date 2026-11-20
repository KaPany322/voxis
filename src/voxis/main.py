"""Interactive command-line interface"""

import argparse
from pathlib import Path

from voxis.actions import create_default_registry
from voxis.config.commands import load_command_config
from voxis.core.action_engine import ActionEngine
from voxis.core.command_resolver import CommandResolver


def run(config_path: str | Path) -> None:
    """Run the interactive CLI using the supplied JSON configuration."""
    config = load_command_config(config_path)
    resolver = CommandResolver(config)
    engine = ActionEngine(create_default_registry())
    print("Voxis: Ready. Type 'exit' or 'quit' to leave.")
    while True:
        try:
            user_text = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nVoxis: Goodbye.")
            break
        if user_text.strip().lower() in {"exit", "quit"}:
            print("Voxis: Goodbye.")
            break
        command = resolver.resolve(user_text)
        if command is None:
            print("Voxis: I don't recognize that command.")
            continue
        result = engine.execute(command)
        if result.success:
            if command.response:
                print(f"Voxis: {command.response}")
            else:
                print("Voxis: Done.")
        else:
            action_number = (
                result.failed_action_index + 1
                if result.failed_action_index is not None
                else "unknown"
            )
            print(
                f"Voxis: Action {action_number} failed: "
                f"{result.message or 'unknown error'}"
            )


def main() -> None:
    """Parse CLI arguments and start Voxis."""
    parser = argparse.ArgumentParser(description="Voxis text command engine")
    parser.add_argument(
        "--config",
        default="config/commands.json",
        help="Path to the JSON command configuration.",
    )
    args = parser.parse_args()
    try:
        run(args.config)
    except Exception as exc:
        parser.exit(1, f"Voxis: Could not start: {exc}\n")


if __name__ == "__main__":
    main()
