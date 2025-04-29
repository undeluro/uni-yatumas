from enum import Enum, auto


class SimulationState(Enum):
    """
    Represents state of the graphical simulator.
    """

    IDLE = auto()
    """The simulator is between the simulation steps"""

    FOUND_TRANSITION = auto()
    """The simulator found a transition applicable in the current state"""

    CHANGED_STATE = auto()
    """The simulator just changed the machine state and the put a symbol on the tape"""

    MOVED = auto()
    """The simulator just moved the machine's head"""

    FINISHED = auto()
    """The simulator successfully finished its work"""

    INTERRUPTED = auto()
    "The simulator has been interrupted"
