from collections.abc import Callable  # noqa
from typing import Literal  # noqa
import blessed
from yatumas.machine.symbol import Symbol, EmptySymbol  # noqa
from yatumas.simulator.simulation_state import SimulationState
from yatumas.simulator.model import Model


class View:
    """
    Class responsible for displaying the simulation.
    Expected to be used as a context manager:

        with view as refresh:
            refresh() # < refreshes the screen

    Protected Attributes
    ----------
    _ellipsis: str
        symbol to be printed at the ends of the tape
    _separator: str
        symbol used to separate symbols on the tape
    _term: blessed.Terminal
        a terminal object used to print correct output codes
    _model: Model
        a model component of the simulation
    _head_x_coordinate: int | None
        current position of the TM's head, if any

    Methods
    -------
    def __init__(model: Model, term: blessed.Terminal):
        initializes the view component
    def __enter__() -> Callable[[], None]:
        entering the context manager prepares the terminal
        and returns a handle to refresh the screen
    def __exit__(*args) -> bool:
        when exiting, the terminal returns to its normal mode
    """

    _ellipsis = "..."
    _separator = "|"
    _term: blessed.Terminal
    _model: Model
    _head_x_coordinate: int | None

    def __init__(self, model: Model, term: blessed.Terminal):
        """
        Initializes the object.

        Parameters
        ----------
        model: Model
            corresponds to the self._model attribute
        term: blessed.Terminal
            correspond to the self._term attribute
        """
        self._model = model
        self._term = term
        self._reset()

    def _reset(self):
        """
        Reset the view state.
        """
        self._head_x_coordinate = None

    def __enter__(self) -> Callable[[], None]:
        """
        Enters the view context: clearing the view and entering the fullscreen.

        Returns
        -------
        refresh: Callable[[], None]
            the "refresh" callback
        """
        self._reset()
        print(self._clear_screen(), end="")
        self._term.enter_fullscreen()
        return self._refresh

    def __exit__(self, *args):
        """
        Cleans the context, exiting the fullscreen.
        """
        print(self._term.normal, end="")
        # print(self._term.normal + self._term.clear + self._term.home, end="") Uncomment this line to clear the screen
        self._term.exit_fullscreen()
        return False

    def _refresh(self) -> None:
        """
        Refreshes the simulation view.
        """
        # here we dont clear the whole screen, we clear only lines we need to update
        # it was done to avoid flickering
        # if you want to clear the screen all the time, uncomment the following lines and remove starting with "with ..."
        with self._term.location(0, 0):
            print(self._term.center(self._display_title()))
        with self._term.location(0, 2):
            print(self._display_tape())
        with self._term.location(0, 4):
            print(self._term.center(self._display_transition()))
        with self._term.location(0, 6):
            print(self._term.center(self._display_footer()))
        # print(self._clear_screen())
        # print(self._term.center(self._display_title()))
        # print()
        # print(self._display_tape())
        # print()
        # print(self._term.center(self._display_transition()))
        # print()
        # print(self._term.center(self._display_footer()))

    def _clear_screen(self) -> str:
        """
        Return a terminal sequence clearing the terminal screen
        """
        return self._term.home + self._term.on_black + self._term.clear

    def _display_title(self) -> str:
        """
        Returns a formatted app header
        """
        return self._title_font("Yet Another Turing Machine Simulator")

    def _display_tape(self) -> str:
        """
        Returns a string representing a well-formatted tape.
        """

        head_x_coordinate = self._updated_head_x_coordinate()
        symbols = self._visible_symbols(head_x_coordinate)

        # what is the symbol below the head ?
        head_symbol_index = next(
            i for i, (si, _) in enumerate(symbols) if si == self._model.head_offset
        )

        # splits symbols into three parts:
        # before, below, after the head
        symbols_before_head = [s for _, s in symbols[:head_symbol_index]]
        head_symbol = symbols[head_symbol_index][1]
        symbols_after_head = [s for _, s in symbols[head_symbol_index + 1 :]]

        # renders the symbols according to the positions
        # - the head symbol is selected
        # underline makes the floor of the tape
        before_head = self._separator.join([self._ellipsis] + symbols_before_head)
        head = self._separator + head_symbol + self._separator
        after_head = self._separator.join(symbols_after_head + [self._ellipsis])
        tape_line = (
            self._normal_underlined_font(before_head)
            + self._selected_underlined_font(head)
            + self._normal_underlined_font(after_head)
        )

        # renders the state string, centering it around the head position
        state = self._model.machine_state
        left_state_half = state[: max(0, len(state) // 2 - 1)]
        state_center = state[len(left_state_half) : len(left_state_half) + 3]
        right_state_half = state[len(left_state_half) + len(state_center) :]

        # render the "ceiling" of the tape,
        # there are five types of the ceiling:
        # - before the machine state
        # - before the head position
        # - the head position
        # - after the head, before the end of the state string
        # - after machine state
        above_before_state = " " * (
            len(before_head) - len(left_state_half) - len(state_center) // 2
        )
        above_before_head = self._separator + left_state_half if left_state_half else ""
        above_head = (
            ("" if left_state_half else self._separator)
            + state_center
            + ("" if right_state_half else self._separator)
        )
        above_after_head = (
            right_state_half + self._separator if right_state_half else ""
        )
        above_after_state = " " * (
            len(after_head) - len(right_state_half) - len(state_center) // 2
        )
        above_line = (
            self._normal_underlined_font(above_before_state)
            + self._selected_underlined_font(above_before_head)
            + self._selected_font(above_head)
            + self._selected_underlined_font(above_after_head)
            + self._normal_underlined_font(above_after_state)
        )

        # we return the ceiling + the tape itself
        return above_line + "\n" + tape_line

    def _n_symbols(self) -> int:
        """
        Tells how many symbol can fit on the screen

        Returns
        --------
        n_symbol: int
            number of the symbol that will fit in the terminal, assuming
            - there are two self._ellipsis at the ends separated by a single space character
            - the self._separator is used to separate the symbols
        """
        ellipsis_length = len(self._ellipsis) * 2 + 2
        available_width = self._term.width - ellipsis_length
        separator_length = len(self._separator)

        max_symbols = (available_width + separator_length) // (separator_length + 1)
        return max(0, max_symbols)

    def _movement_direction(self) -> int:
        """
        Tells how the head x coordinate should change on the screen.

        Returns
        -------
        offset: int
            if positive (typically +1), head moves right by the value
            if negative (typically -1), head moves left by the value
        """
        n_symbols = self._n_symbols()

        if (
            self._model.simulator_state != SimulationState.MOVED
            or (
                self._head_x_coordinate <= n_symbols // 10 and self._model.last_move < 0
            )
            or (
                self._head_x_coordinate >= 9 * n_symbols // 10
                and self._model.last_move > 0
            )
        ):
            return 0
        return self._model.last_move

    def _updated_head_x_coordinate(self) -> int:
        """
        Updates the head `x` coordinate (`self._head_x_coordinate`)
        and return the new value.

        Returns
        -------
        x_coordinate: int
            the new coordinate of the head
        """
        move = self._movement_direction()
        n_symbols = self._n_symbols()
        self._head_x_coordinate = (
            n_symbols // 2
            if self._head_x_coordinate is None
            else self._head_x_coordinate + move
        )
        return self._head_x_coordinate

    def _visible_symbols(self, head_x_coordinate: int) -> list[(tuple[int, str])]:
        """
        Returns a list of rendered symbols to be displayed.

        Parameters
        ----------
        head_x_coordinate: int
            the current head position on the screen

        Returns
        -------
        symbol: list[tuple[int, str]]
            a list of tuples containing:
            - index of the symbol on the tape
            - rendered symbol ('_' replaced with ' ')
        """
        n_symbols = self._n_symbols()
        head_offset = self._model.head_offset

        # Calculate the range of visible symbols
        left_count = head_x_coordinate
        right_count = n_symbols - head_x_coordinate - 1

        start_index = head_offset - left_count
        end_index = head_offset + right_count

        visible_symbols = []
        for i in range(start_index, end_index + 1):
            symbol = self._model.tape[i]
            rendered = " " if symbol == EmptySymbol else str(symbol)
            visible_symbols.append((i, rendered))

        return visible_symbols

    def _display_transition(self) -> str:
        """
        Returns a sequence representing the currently chosen transition.
        """
        if self._model.simulator_state == SimulationState.IDLE:
            return self._normal_font("... looking for transition")
        if self._model.simulator_state == SimulationState.FINISHED:
            return self._title_font("FINISHED")
        if self._model.simulator_state == SimulationState.INTERRUPTED:
            return self._title_font("INTERRUPTED")

        if self._model.simulator_state == SimulationState.FOUND_TRANSITION:
            return self._selected_font(
                f"{self._model.transition.condition.state} + {self._model.transition.condition.symbol}"
            ) + self._normal_font(
                f" |> {self._model.transition.effect.new_state} + {self._model.transition.effect.new_symbol} "
                f"|> {self._model.transition.effect.action}"
            )

        if self._model.simulator_state == SimulationState.CHANGED_STATE:
            return (
                self._normal_font(
                    f"{self._model.transition.condition.state} + {self._model.transition.condition.symbol}"
                    f" |> "
                )
                + self._selected_font(
                    f"{self._model.transition.effect.new_state} + {self._model.transition.effect.new_symbol}"
                )
                + self._normal_font(f" |> {self._model.transition.effect.action}")
            )
        if self._model.simulator_state == SimulationState.MOVED:
            return self._normal_font(
                f"{self._model.transition.condition.state} + {self._model.transition.condition.symbol}"
                f" |> {self._model.transition.effect.new_state} + {self._model.transition.effect.new_symbol} |> "
            ) + self._selected_font(f"{self._model.transition.effect.action}")
        return (
            self._state_font(f"{self._model.transition.condition.state}")
            + self._normal_font(" + ")
            + self._symbol_font(f"{self._model.transition.condition.symbol}")
            + self._normal_font(" |> ")
            + self._state_font(f"{self._model.transition.effect.new_state}")
            + self._normal_font(" + ")
            + self._symbol_font(f"{self._model.transition.effect.new_symbol}")
            + self._normal_font(" |> ")
            + self._action_font(f"{self._model.transition.effect.action}")
        )

    def _display_footer(self) -> str:
        """
        Returns a sequence representing the application footer with controls.
        """
        match self._model.simulator_state:
            case SimulationState.FINISHED | SimulationState.INTERRUPTED:
                return self._title_font("Press Any Key to Exit")
            case _:
                controls = [
                    self._control_button("a", "accelerate"),
                    self._control_button("s", "slow down"),
                    self._control_button("q", "quit"),
                ]
                interval = self._interval_display()
                return f"{' | '.join(controls)} | {interval}"

    def _control_button(self, key: str, label: str) -> str:
        """
        Returns a formatted control button with key and label.
        """
        return f"{self._term.dark_cyan_on_black}[{self._term.dark_yellow_on_black}{key}{self._term.dark_cyan_on_black}] {self._term.dark_white_on_black}{label}"

    def _interval_display(self) -> str:
        """
        Returns a formatted interval display with color.
        """
        return f"{self._term.dark_cyan_on_black}interval: {self._term.dark_magenta_on_black}{self._model.step_interval_in_sec:.1f}s"

    def _normal_underlined_font(self, text: str = ""):
        """
        Returns a text formatted as the "normal" underlined font.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._normal_font(self._term.underline + text) + self._normal_font()

    def _normal_font(self, text: str = ""):
        """
        Returns a text formatted using the "normal" font with white color.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._term.normal + self._term.white_on_black + text

    def _selected_underlined_font(self, text: str = ""):
        """
        Returns a text formatted using the "selected" font with the underline effect.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._term.underline + self._selected_font(text)

    def _selected_font(self, text: str = ""):
        """
        Returns a text formatted using the "selected" font with bright yellow color.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._term.bright_yellow_on_black + text + self._normal_font()

    def _title_font(self, text: str = ""):
        """
        Returns a text formatted using the "title" font with bright cyan color.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._term.bright_cyan_on_black + text + self._normal_font()

    def _state_font(self, text: str = ""):
        """
        Returns a text formatted using the "state" font with bright green color.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._term.bright_green_on_black + text + self._normal_font()

    def _symbol_font(self, text: str = ""):
        """
        Returns a text formatted using the "symbol" font with bright magenta color.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._term.bright_magenta_on_black + text + self._normal_font()

    def _action_font(self, text: str = ""):
        """
        Returns a text formatted using the "action" font with bright red color.
        If called without an argument, just return the formatting sequence.

        Parameters
        ----------
        text: str = ""
            text to be formatted
        """
        return self._term.bright_red_on_black + text + self._normal_font()
