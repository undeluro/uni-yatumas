from typing import NewType
from dataclasses import dataclass
from yatumas.machine.state import State
from yatumas.machine.symbol import Symbol
from yatumas.machine.action import Action


@dataclass(frozen=True, slots=True)
class Condition:
    """
    Represents conditions triggering a given transition of the TM.

    Parameters
    ----------
    state: State
        state of the machine, allowing to perform the transition
    symbol: Symbol
        current symbol on the tape, triggering the transition
    """

    state: State
    symbol: Symbol


@dataclass(frozen=True, slots=True)
class Effect:
    """
    Represents effects of a TM transition.

    Parameters
    ----------
    new_state: State
        state of the machine after performing the transition
    new_symbol: Symbol
        symbol to be put on the tape
    action: Action
        whether and how machine head should move after the transition
    """

    new_state: State
    new_symbol: Symbol
    action: Action


@dataclass(frozen=True, slots=True)
class Transition:
    """
    Represents a TM transition.

    Attributes
    ----------
    condition: Condition
        conditions required for the transition to occur
    effect: Effect
        effects of the transition
    """

    condition: Condition
    effect: Effect


"""
TransitionTable` is just a dictionary mapping
transitions' conditions to their effects
"""
TransitionTable = NewType("TransitionTable", dict[Condition, Effect])
