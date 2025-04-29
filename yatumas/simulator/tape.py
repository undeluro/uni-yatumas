from yatumas.machine.symbol import Symbol, EmptySymbol


class Tape:
    """
    Represents an infinite tape with cells able to hold a single symbol each.
    It's implemented using two lists:
    - one representing the cells on the left of the cell `0`, with negative indices
    - one representing the cells on the right of the cell `0`, with positive indices
    The lists' names starts with `_` to mark they are not public.

    Methods
    -------
    __init__(machine_input: list[Symbol])
        initializes list with the given machine_input
    """

    _negative: list[Symbol]
    _positive: list[Symbol]

    def __init__(self, machine_input: list[Symbol]):
        self._positive = machine_input
        self._negative = []

    def _get_coordinates(self, index: int) -> tuple[list[Symbol], int]:
        if index >= 0:
            return self._positive, index
        else:
            return self._negative, abs(index) - 1

    def _expand_tape(self, tape: list[Symbol], index: int):
        tape += [EmptySymbol for _ in range(len(tape), index + 1)]

    def __setitem__(self, index: int, symbol: Symbol) -> None:
        tape, frame_index = self._get_coordinates(index)
        self._expand_tape(tape, frame_index)
        tape[frame_index] = symbol

    def __getitem__(self, index: int) -> Symbol:
        tape, frame_index = self._get_coordinates(index)
        self._expand_tape(tape, frame_index)
        return tape[frame_index]

    def __str__(self) -> str:
        return "".join(
            [str(symb) for symb in reversed(self._negative)]
            + ["|"]
            + [str(symb) for symb in self._positive]
        )
