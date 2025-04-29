from timeit import default_timer as timer
import blessed
from yatumas.machine.transition_table import Transition
from yatumas.simulator.simulation_state import SimulationState  # noqa
from yatumas.simulator.view import View
from yatumas.simulator.model import Model


class Controller:
    """
    Class responsible for controlling the simulation.

    Protected Attributes
    ----------
    _model: Model
        contains all the data required by the simulation
    _view View
        display the simulation to the user
    _term: blessed.Terminal
        used to gather input from the terminal

    Methods
    -------
    def run_simulation() -> None:
        runs the simulation
    """

    _model: Model
    _view: View
    _term: blessed.Terminal

    def __init__(self, model: Model, view: View, term: blessed.Terminal):
        """
        Initializes the controller.

        Parameters
        ----------
        model: Model
            corresponds to the self._model attribute
        view: View
            corresponds to the self._view attribute
        erm: blessed.Terminal
            correspond to the self._term attribute
        """
        self._model = model
        self._view = view
        self._term = term

    def run_simulation(self):
        """
        Runs the simulation
        """
        with self._view as refresh:  # Use the view as a context manager
            refresh()  # Refresh the screen once
            self._run_input_loop()  # Run the input loop

            # Main simulation loop
            while self._step():
                refresh()  # Refresh the screen
                self._run_input_loop()  # Run the input loop

            # After the loop, refresh the screen and wait for user input
            refresh()
            self._wait_for_any_key()

    def _find_applicable_transition(self) -> Transition | None:
        """
        Helper method to find the currently applicable transition.

        Returns
        -------
        transition: Transition | None
            an applicable transition, if there is any, otherwise None
        """
        condition = self._model.current_condition
        if effect := self._model.machine.transition_table.get(condition, None):
            return Transition(condition, effect)
        return None

    def _step(self) -> bool:
        """
        Makes a single step of the simulation.

        Returns
        -------
        should_continue: bool
            True - if the simulation should continue
            False - if the simulation has finished
        """
        match self._model.simulator_state:
            case SimulationState.IDLE:
                transition = self._find_applicable_transition()
                if transition is None:
                    self._model.simulator_state = SimulationState.FINISHED
                else:
                    self._model.transition = transition
                    self._model.simulator_state = SimulationState.FOUND_TRANSITION
                return True

            case SimulationState.FOUND_TRANSITION:
                self._model.machine_state = self._model.transition.effect.new_state
                self._model.current_symbol = self._model.transition.effect.new_symbol
                self._model.simulator_state = SimulationState.CHANGED_STATE
                return True

            case SimulationState.CHANGED_STATE:
                move_offset = self._model.transition.effect.action.value
                self._model.move_head(move_offset)
                self._model.simulator_state = SimulationState.MOVED
                return True

            case SimulationState.MOVED:
                self._model.simulator_state = SimulationState.IDLE
                self._model.transition = None
                return True
            case SimulationState.FINISHED | SimulationState.INTERRUPTED:
                return False

    def _wait_for_any_key(self) -> None:
        """
        Waits indefinitely for any key to be pressed.
        """
        with self._term.cbreak():  # to read the user input from the terminal
            self._term.inkey(timeout=None)  # wait for an input indefinitely

    def _run_input_loop(self) -> None:
        """
        Reacts to the user input:
        - 's' -> slows down the simulation
        - 'a' -> accelerates the simulation
        - 'q' -> quits the simulation
        """

        start = timer()  # noqa <- for ruff check to ignore

        def time_left() -> float:
            return self._model.step_interval_in_sec - (timer() - start)

        with self._term.cbreak():
            while time_left() > 0:
                key = self._term.inkey(timeout=time_left())
                if key == "s":
                    self._model.step_interval_in_sec += 0.1
                elif key == "a":
                    self._model.step_interval_in_sec = max(
                        0.1, self._model.step_interval_in_sec - 0.1
                    )
                elif key == "q":
                    self._model.simulator_state = SimulationState.INTERRUPTED
