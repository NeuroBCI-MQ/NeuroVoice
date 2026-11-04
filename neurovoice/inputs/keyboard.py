"""Keyboard input: stands in for brain/muscle signals during development. Pre-implentation of EEG mechanics"""

from neurovoice.inputs.base import Choice, InputMode

KEYMAP = {"y": Choice.YES, "n": Choice.NO, "x": Choice.NONE}


class KeyboardInput(InputMode):
    def get_choice(self) -> Choice:
        while True:
            key = input("[y] yes  [n] next  [x] none of these: ").strip().lower()
            if key in KEYMAP:
                return KEYMAP[key]
            print("Please press y, n, or x.")


if __name__ == "__main__":
    print(KeyboardInput().get_choice())