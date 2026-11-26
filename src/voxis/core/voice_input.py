"""Offline microphone input using a locally stored Vosk model."""

import json
import queue
from collections.abc import Iterator
from pathlib import Path


def listen(model_path: str | Path, wake_phrase: str, device: int | str | None = None) -> Iterator[str]:
    """Yield one command after each offline "Hey Voxis" wake phrase."""
    import sounddevice as sd
    from vosk import KaldiRecognizer, Model

    audio_queue: queue.Queue[bytes] = queue.Queue()
    model = Model(str(model_path))
    recognizer = KaldiRecognizer(model, 16_000)

    def on_audio(indata: bytes, frames: int, timing: object, status: object) -> None:
        if status:
            print(f"Microphone: {status}")
        audio_queue.put(bytes(indata))

    while True:
        with sd.RawInputStream(
            samplerate=16_000,
            blocksize=8_000,
            dtype="int16",
            channels=1,
            device=device,
            callback=on_audio,
        ):
            phrase = ""
            while not phrase:
                audio = audio_queue.get()
                if recognizer.AcceptWaveform(audio):
                    phrase = json.loads(recognizer.Result()).get("text", "")
                    print(f"{phrase} first")

        if wake_phrase in phrase.split()[0]:
            print(f"{phrase} second")
            yield " ".join(phrase.split()[1:])
