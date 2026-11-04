"""Speaks text aloud using macOS's built-in text-to-speech."""

import subprocess

VOICE = "Samantha"   # run `say -v '?'` in the terminal to see all voices
RATE = 185           # words per minute


def speak(text):
    """Say text out loud. Blocks until finished speaking."""
    if not text:
        return
    subprocess.run(["say", "-v", VOICE, "-r", str(RATE), text], check=False)


if __name__ == "__main__":
    speak("Hi, this is NeuroVoice.")