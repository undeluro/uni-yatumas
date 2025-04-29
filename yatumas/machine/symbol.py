from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Symbol:
    """
    Represents a single symbol on the tape.

    Attributes
    ----------
    value: str
        a single character string
    """

    value: str

    def __post_init__(self):
        if len(self.value) != 1:
            raise ValueError(f"symbol {self.value} is not a single character")

    def __str__(self) -> str:
        return self.value


"""Predefined empty symbol representing an empty tape cell"""
EmptySymbol = Symbol("_")
