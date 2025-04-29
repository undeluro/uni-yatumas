import re
from yatumas.parser.error import ParsingError, ParsingErrorType
from yatumas.machine.machine import Machine
from yatumas.machine.state import State
from yatumas.machine.symbol import Symbol
from yatumas.machine.transition_table import Condition, Effect, TransitionTable
from yatumas.machine.action import Action

SYMBOL = r"[_*\d]"
SPACE = r"\s*"
STATE = r"\w+"
SEPARATOR = rf"{SPACE}\|>{SPACE}"
PLUS = rf"{SPACE}\+{SPACE}"

INPUT_SYMBOL_REGEXP = re.compile(rf"({SYMBOL})")
INIT_STATE_REGEXP = re.compile(rf"({STATE}){SPACE}$")
STATE_SYMBOL_REGEXP = re.compile(rf"(?P<state>{STATE}){PLUS}(?P<symbol>{SYMBOL})")
ACTION_REGEXP = re.compile(r"(L|R|N)")


def _is_empty(line: str) -> bool:
    """
    Checks whether the line is empty.

    Parameters:
    -----------
    line: str
        text to be checked

    Returns:
    --------
    is_empty: bool
        true if and only if the line has length 0 or contains only white characters
    """
    return line == "" or line.isspace()


def _is_comment(line: str) -> bool:
    """
    Checks whether the line contains a comment.

    Parameters:
    -----------
    line: str
        text to be checked

    Returns:
    --------
    is_comment: bool
        true if and only if the line starts with `#` possibly preceded by white characters
    """

    return line.strip().startswith("#")


def _parse_init_state(line: str) -> State | None:
    """
    Reads initial state from the text.

    Parameters:
    -----------
    line: str
        line to be parsed

    Returns:
    --------
    result
        - `None` if the line does not represent a state
        - a parsed `State` object otherwise
    """

    if init_state_match := INIT_STATE_REGEXP.fullmatch(line):
        return State(init_state_match.group(1))
    return None


def _parse_state_symbol(text: str) -> tuple[State, Symbol] | None:
    """
    Reads a pair state + symbol from the raw text.

    Parameters:
    -----------
    text: str
        text to be parsed

    Returns:
    --------
    result: tuple[State, Symbol] | None
        - `None` if the line does not represent a state + symbol pair
        - a parsed tuple with `State` and `Symbol` object otherwise
    """

    if text_match := STATE_SYMBOL_REGEXP.match(text):
        state = State(text_match.group("state"))
        symbol = Symbol(text_match.group("symbol"))
        return state, symbol
    return None


def _parse_action(text: str) -> Action | None:
    """
    Reads an action for the raw text

    Parameters:
    -----------
    text: str
        text to be parsed

    Returns:
    --------
    result: Action | None
        - `None` if the line does not represent an action
        - a parsed `Action` object otherwise
    """

    if text_match := ACTION_REGEXP.match(text):
        match text_match.group(1):
            case "L":
                return Action.LEFT
            case "R":
                return Action.RIGHT
            case "N":
                return Action.NONE

    return None


def _parse_transition(line: str) -> tuple[Condition, Effect] | None:
    """
    Reads a transition from a line.

    Parameters:
    -----------
    line: str
        line to be parsed

    Returns:
    --------
    result: tuple[Condition, Effect] | None
        - `None` if the line does not represent a TM transition
        - a parsed pair `Condition` and `Effect` otherwise
    """
    try:
        transition_components = re.split(SEPARATOR, line)
        [condition_txt, new_state_txt, action_txt] = transition_components

        condition_components = _parse_state_symbol(condition_txt)
        if condition_components is None:
            return None
        condition_state, condition_symbol = condition_components

        new_state_components = _parse_state_symbol(new_state_txt)
        if new_state_components is None:
            return None
        new_state, new_symbol = new_state_components

        action = _parse_action(action_txt)
        if action is None:
            return None

        condition = Condition(condition_state, condition_symbol)
        effect = Effect(new_state, new_symbol, action)
        return condition, effect
    except Exception:
        return None


def parse_machine(lines: list[str]) -> Machine:
    """
    Parses a text into a Turing Machine.

    Parameters:
    -----------
    lines: list[str]
        lines to be parsed

    Returns:
    --------
    machine: Machine
        a parsed Turing Machine
    """

    init_state: State | None = None
    transition_table: TransitionTable = TransitionTable({})

    numbered_lines = [
        (i + 1, line)
        for i, line in enumerate(lines)
        if not _is_empty(line) and not _is_comment(line)
    ]

    init_state_line_number, init_state_text = numbered_lines[0]
    init_state = _parse_init_state(init_state_text)
    if init_state is None:
        raise ParsingError(ParsingErrorType.INVALID_INIT_STATE, init_state_line_number)

    transition_lines = numbered_lines[1:]
    for i, line in transition_lines:
        transition = _parse_transition(line)
        if transition is None:
            raise ParsingError(ParsingErrorType.INVALID_TRANSITION, i)
        condition, effect = transition
        if condition in transition_table:
            raise ParsingError(ParsingErrorType.DUPLICATED_TRANSITION, i)
        transition_table[condition] = effect

    # for i, line in enumerate(lines): # older version but easier to understand
    #     if _is_empty(line) or _is_comment(line):
    #         continue

    #     if init_state is None:
    #         init_state = _parse_init_state(line)
    #         if init_state is None:
    #             raise ParsingError(ParsingErrorType.INVALID_INIT_STATE, i + 1)
    #         continue

    #     transition = _parse_transition(line)
    #     if transition is None:
    #         raise ParsingError(ParsingErrorType.INVALID_TRANSITION, i + 1)

    #     condition, effect = transition
    #     if condition in transition_table:
    #         raise ParsingError(ParsingErrorType.DUPLICATED_TRANSITION, i + 1)

    #     transition_table[condition] = effect

    return Machine(initial_state=init_state, transition_table=transition_table)


def parse_input(text: str) -> list[Symbol]:
    """
    Parses a text into an input for the Turing Machine..

    Parameters:
    -----------
    text: str
        text to be parsed

    Returns:
    --------
    machine_input: list[Symbol]
        symbols to be put initially on the tape
    """

    machine_input: list[Symbol] = []

    for i, c in enumerate(text):
        symbol_match = INPUT_SYMBOL_REGEXP.fullmatch(c)
        if symbol_match is None:
            raise ParsingError(ParsingErrorType.INVALID_SYMBOL, i)
        machine_input.append(Symbol(symbol_match.group(1)))

    return machine_input
