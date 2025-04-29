from enum import Enum


class Action(Enum):
    """
    Represents an action performed by the machine after finishing a transition.
    There are three possible actions:
    Their integer values corresponds to the effective position change on the tape.
    """

    NONE = 0
    """machine makes no movement (0 - represents no change)"""
    LEFT = -1
    """machine is moving left (-1 is the effective position change)"""
    RIGHT = 1
    """machine is moving right (1 is the effective position change)"""
