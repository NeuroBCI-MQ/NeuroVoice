"""Records from the microphone and transcribes speech with Whisper (locally)."""

import queue

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000      # Whisper expects 16 kHz audio
MODEL_SIZE = "small.en"  # good balance of speed and accuracy for English

_model = None


def _get_model():
    """Load the Whisper model once and reuse it (loading is slow)."""
    global _model
    if _model is None:
        print("Loading Whisper model (first run downloads it)...")
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    return _model


def record():
    """Record from the mic until Enter is pressed. Returns audio as a numpy array."""
    chunks = queue.Queue()

    def callback(indata, frames, time, status):
        chunks.put(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=callback):
        input("🎙  Listening... press Enter when they finish.")

    audio = [chunks.get() for _ in range(chunks.qsize())]
    return np.concatenate(audio).flatten() if audio else np.zeros(0, dtype=np.float32)


def listen():
    """Record speech and return the transcribed text."""
    audio = record()
    if audio.size == 0:
        return ""
    segments, _ = _get_model().transcribe(audio, language="en", vad_filter=True)
    return " ".join(seg.text.strip() for seg in segments).strip()


if __name__ == "__main__":
    _get_model()
    input("Press Enter to start listening...")
    print("Heard:", listen())