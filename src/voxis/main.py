"""Interactive command-line interface"""

import argparse
from pathlib import Path

from voxis.config.commands import load_command_config
from voxis.core.action_engine import ActionEngine
from voxis.core.registry import ActionRegistry
from voxis.core.voice_input import listen
import pyttsx3

tts = pyttsx3.init()


def speak(text: str) -> None:
    """Speak text and wait for playback to finish before continuing."""
    tts.say(text)
    tts.runAndWait()


def run(
    config_path: str | Path,
    voice: bool = False,
    model_path: str | Path = "models/vosk-model-small-en-us-0.15",
    device: int | str | None = None,
) -> None:
    """Run the interactive CLI using the supplied JSON configuration."""
    config = load_command_config(config_path)
    registry = ActionRegistry(config)
    engine = ActionEngine(registry)
    voice_input = listen(model_path, device=device) if voice else None
    ready_message = (
        "Ready. Say a command or say exit."
        if voice
        else "Ready. Type 'exit' or 'quit' to leave."
    )
    print(f"Voxis: {ready_message}")
    speak(ready_message)
    while True:
        try:
            if voice_input is None:
                user_text = input("You: ")
            else:
                user_text = next(voice_input)
                print(f"You: {user_text}")
        except (EOFError, KeyboardInterrupt):
            print("\nVoxis: Goodbye.")
            speak("Goodbye.")
            break
        if user_text.strip().lower() in {"exit", "quit"}:
            print("Voxis: Goodbye.")
            speak("Goodbye")
            break
        command = registry.resolve(user_text)
        if command is None:
            print("Voxis: I don't recognize that command.")
            continue
        result = engine.execute(command)
        if result.success:
            if command.response:
                print(f"Voxis: {command.response}")
                speak(f"{command.response}")
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
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Recognize microphone input offline using the local Vosk model.",
    )
    parser.add_argument(
        "--model",
        default="models/vosk-model-small-en-us-0.15",
        help="Path to the downloaded Vosk model (used with --voice).",
    )
    parser.add_argument(
        "--device",
        help="Microphone device ID or name (list devices with 'python -m sounddevice').",
    )
    args = parser.parse_args()
    device = args.device
    if device is not None and device.isdecimal():
        device = int(device)
    try:
        run(args.config, voice=args.voice, model_path=args.model, device=device)
    except Exception as exc:
        parser.exit(1, f"Voxis: Could not start: {exc}\n")


if __name__ == "__main__":
    main()
