"""Main loop: hear → propose → select → respond."""

from neurovoice.proposer import propose_replies
from neurovoice.inputs.base import Choice
from neurovoice.inputs.keyboard import KeyboardInput

MAX_BATCHES = 2  # after this many "none of these", switch to typing


def select_reply(replies, input_mode):
    """Cycle through replies one at a time. Return the chosen one, or None."""
    for reply in replies:
        print(f"\n  → {reply}")
        choice = input_mode.get_choice()
        if choice == Choice.YES:
            return reply
        if choice == Choice.NONE:
            return None
        # Choice.NO: move to the next reply
    return None  # went through all of them without a yes


def respond_to(heard_text, input_mode, history):
    """Run batches of proposals until the user picks one or falls back."""
    for batch in range(MAX_BATCHES):
        replies = propose_replies(heard_text, history)
        if not replies:
            print("(No replies generated, trying again...)")
            continue
        chosen = select_reply(replies, input_mode)
        if chosen:
            return chosen
        print("\nGetting new options...")

    # Fallback: spelling mode (keyboard stand-in for now)
    return input("\nType your reply: ")


def main():
    input_mode = KeyboardInput()
    history = []

    print("NeuroVoice: type 'quit' to exit.")
    while True:
        heard = input("\nOther person says: ").strip()
        if heard.lower() == "quit":
            break

        reply = respond_to(heard, input_mode, history)
        print(f"\nYOU SAY: {reply}")

        # Remember the conversation for context
        history.append({"role": "user", "content": f"The other person said: {heard}"})
        history.append({"role": "assistant", "content": f"The user replied: {reply}"})


if __name__ == "__main__":
    main()