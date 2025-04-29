from dataclasses import dataclass
from yatumas.simulator.simulation_state import SimulationState
from yatumas.simulator.tape import Tape
from yatumas.machine.machine import Machine
from yatumas.machine.symbol import Symbol
from yatumas.machine.state import State
from yatumas.machine.transition_table import Condition, Transition


@dataclass
class Model:
    """
    This dataclass contains all the data required to render the simulator interface.

    Attributes
    ----------
    machine: Machine
        defines the simulated TM
    machine_input: list[Symbol]
        contains the initial input of the TM
    tape: Tape
        is the current state of the tape
    machine_state: State
        is the current state of the TM
    head_offset: int
        what is the current position of the TM's head

    simulator_state: State
        is the current state of the simulator
    transition: Transition | None
        the currently performed transition (if any)
    last_move: int | None
        what was the last position change (if any)
    last_head_offset: int | None
        what was the last position of the TM's head (if any)

    default_step_interval_in_sec: float
        what is the default interval between the simulation updates (in seconds)
    step_interval_in_sec: float
        what is the current interval between the simulation updates (in seconds)
    """

    # parameters describing the machine state
    machine: Machine
    machine_input: list[Symbol]
    tape: Tape
    machine_state: State
    head_offset: int

    # parameters describing the simulation state
    simulator_state: SimulationState
    transition: Transition | None
    last_move: int | None
    last_head_offset: int | None

    # parameters controlling the simulation
    default_step_interval_in_sec: float
    step_interval_in_sec: float

    def __init__(
        self,
        machine: Machine,
        machine_input: list[Symbol],
        step_interval_in_sec: float,
    ) -> None:
        """
        Initializes the model with the simulation parameters.

        Parameters
        ----------
        machine: Machine
            machine being simulated
        machine_input: list[Symbol]
            the initial input of the machine
        step_interval_in_sec: float
            how often the simulation should update its state
        """

        self.machine = machine
        self.machine_input = machine_input
        self.default_step_interval_in_sec = step_interval_in_sec
        self.reset()

    def reset(self):
        """
        Resets the model to the state before the simulation started.
        """
        self.last_move = None
        self.last_head_offset = None
        self.transition = None
        self.simulator_state = SimulationState.IDLE
        self.head_offset = 0
        self.tape = Tape(self.machine_input)
        self.machine_state = self.machine.initial_state
        self.step_interval_in_sec = self.default_step_interval_in_sec

    def move_head(self, offset: int):
        """
        Moves the machine head by a given offset.

        Parameters
        ----------
        offset: int
            how the head should be moved, e.g.,
            `1` moves head directly to the right, `-1` to the left
        """
        self.last_move = offset
        self.head_offset += offset

    @property
    def is_after_the_first_move(self) -> bool:
        """
        Whether the simulation has already finished at least single transition

        Returns
        -------
        is_after_the_first_move: bool
            True, if the simulator made at least single transition
            False, otherwise
        """
        return self.last_move is not None and self.last_head_offset is not None

    @property
    def current_condition(self) -> Condition:
        """
        What is the current state of the machine for sake of finding a correct transition.

        Returns
        -------
        condition: Condition
            a condition object corresponding to the current machine state
        """
        return Condition(self.machine_state, self.current_symbol)

    @property
    def current_symbol(self) -> Symbol:
        """
        What is the current symbol observed by the TM's head

        Returns
        -------
        symbol: Symbol
            a symbol object taken from the tape at the current position
        """
        return self.tape[self.head_offset]

    @current_symbol.setter
    def current_symbol(self, symbol: Symbol):
        """
        Writes a symbol on the tape below the TM's head.

        Parameters
        ----------
        symbol: Symbol
            a symbol object to be written on the tape
        """
        self.tape[self.head_offset] = symbol
