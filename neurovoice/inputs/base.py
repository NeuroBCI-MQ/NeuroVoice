"""Shared interface for every input mode (keyboard, artifacts, motor imagery)."""

from enum import Enum


class Choice(Enum):
    YES = "yes"
    NO = "no"
    NONE = "none"   # Stands in for none of the above, e.g. when the user is still thinking or the input is ambiguous


class InputMode:
    """Every input mode must provide get_choice()."""

    def get_choice(self) -> Choice:
        raise NotImplementedError("Each input mode must define get_choice()")