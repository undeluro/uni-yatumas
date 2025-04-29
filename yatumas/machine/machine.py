from dataclasses import dataclass

from yatumas.machine.state import State
from yatumas.machine.transition_table import TransitionTable


@dataclass(frozen=True, slots=True)
class Machine:
    """
    Contains a full definition of a Turing's Machine.

    Attributes
    ----------
    initial_state: State
        the state the machine starts in
    transition_table: TransitionTable
        a table containing information how machine should react to the given input
    """

    initial_state: State
    transition_table: TransitionTable
