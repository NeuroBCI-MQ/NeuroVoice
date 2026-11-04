"""Main loop: hear → propose → select → respond → log."""

from neurovoice.proposer import propose_replies, MODEL
from neurovoice.inputs.base import Choice
from neurovoice.inputs.keyboard import KeyboardInput
from neurovoice.logger import InteractionLogger
from neurovoice.speaker import speak 


MAX_BATCHES = 2


def select_reply(replies, input_mode, batch, decisions):
    """Cycle through replies; record every decision. Return the chosen reply or None."""
    for reply in replies:
        print(f"\n  → {reply}")
        choice = input_mode.get_choice()
        decisions.append({"batch": batch, "reply": reply, "choice": choice.value})
        if choice == Choice.YES:
            return reply
        if choice == Choice.NONE:
            return None
    return None


def respond_to(heard_text, input_mode, history):
    """Return (final_reply, reply_source, decisions)."""
    decisions = []
    for batch in range(1, MAX_BATCHES + 1):
        replies = propose_replies(heard_text, history)
        if not replies:
            print("(No replies generated, trying again...)")
            continue
        chosen = select_reply(replies, input_mode, batch, decisions)
        if chosen:
            return chosen, "llm", decisions
        print("\nGetting new options...")

    return input("\nType your reply: "), "typed", decisions


def main():
    input_mode = KeyboardInput()
    source = input("Who's the conversation partner? (self-test / friend / ai-partner): ").strip() or "self-test"
    logger = InteractionLogger(source=source, input_mode="keyboard", model=MODEL)
    history = []

    print("NeuroVoice: type 'quit' to exit.")
    while True:
        heard = input("\nOther person says: ").strip()
        if heard.lower() == "quit":
            break

        reply, reply_source, decisions = respond_to(heard, input_mode, history)
        print(f"\nYOU SAY: {reply}")
        speak(reply)
        logger.log(heard, decisions, reply, reply_source)
        history.append({"role": "user", "content": f"The other person said: {heard}"})
        history.append({"role": "assistant", "content": f"The user replied: {reply}"})

    print(f"\nSession saved to {logger.path}")


if __name__ == "__main__":
    main()