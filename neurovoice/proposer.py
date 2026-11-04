"""Generates candidate replies using a local LLM (Ollama)."""

import json
import ollama

MODEL = "llama3.2"

SYSTEM_PROMPT = """You help a person who cannot speak reply in a conversation.
Given what the other person just said, write short, natural replies
the user might want to say. Vary them: agree, decline, ask a question, etc.
Respond ONLY with JSON in this format:
{"replies": ["reply 1", "reply 2", "reply 3", "reply 4", "reply 5"]}"""


def propose_replies(heard_text, history=None, n=5):
    """Return a list of n candidate replies to heard_text."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Earlier conversation turns give the model context
    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": f'The other person said: "{heard_text}". Give {n} replies.',
    })

    response = ollama.chat(model=MODEL, messages=messages, format="json")

    try:
        replies = json.loads(response["message"]["content"])["replies"]
    except (json.JSONDecodeError, KeyError):
        return []

    return replies[:n]


if __name__ == "__main__":
    text = input("Other person says: ")
    for i, reply in enumerate(propose_replies(text), start=1):
        print(f"{i}. {reply}")