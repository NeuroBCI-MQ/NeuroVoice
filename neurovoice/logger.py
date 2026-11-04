"""Saves every interaction to a JSON Lines file (one JSON object per line)."""

import json
import uuid
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("data/logs")


class InteractionLogger:
    def __init__(self, source="self-test", input_mode="keyboard", model="llama3.2"):
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        self.session_id = uuid.uuid4().hex[:8]
        self.path = LOG_DIR / f"session_{datetime.now():%Y%m%d_%H%M%S}.jsonl"
        self.source = source          # e.g. "self-test", "friend", "ai-partner"
        self.input_mode = input_mode
        self.model = model

    def log(self, heard, decisions, final_reply, reply_source):
        """
        heard:        what the other person said
        decisions:    list of {"batch": int, "reply": str, "choice": "yes"/"no"/"none"}
        final_reply:  what the user ended up saying
        reply_source: "llm" or "typed"
        """
        record = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "source": self.source,
            "input_mode": self.input_mode,
            "model": self.model,
            "heard": heard,
            "decisions": decisions,
            "final_reply": final_reply,
            "reply_source": reply_source,
        }
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")