from enum import Enum, auto


class ParsingErrorType(Enum):
    """
    This enum represents sources of various parsing errors.
    It's accompanying the ParsingError Exception class.
    """

    INVALID_SYMBOL = auto()
    """the machine input contains a symbol unknown to the machine"""
    INVALID_INIT_STATE = auto()
    """the initial state of the machine is malformed"""
    INVALID_TRANSITION = auto()
    """a line representing a transition is malformed"""
    DUPLICATED_TRANSITION = auto()
    """there are two transitions with the same conditions"""

    def message(self, index: int) -> str:
        """
        Translates enum value to a human-friendly message.

        Parameters
        ----------
        index: int
            tells where the error occurred in the text

        Returns
        -------
        message: str
            a human-friendly description of the error
        """
        match self:
            case ParsingErrorType.INVALID_SYMBOL:
                return f"column {index}: an invalid symbol on the input tape"
            case ParsingErrorType.INVALID_INIT_STATE:
                return f"line {index}: the initial state is malformed"
            case ParsingErrorType.INVALID_TRANSITION:
                return f"line {index}: the transition is malformed"
            case ParsingErrorType.DUPLICATED_TRANSITION:
                return f"line {index}: a transition using the same condition has been already defined"
        raise ValueError(f"Unknown value of ParsingErrorType: {self}")


class ParsingError(Exception):
    """
    Exception related to the parsing issues.

    Attributes
    ----------
    error_type: ParsingErrorType
        type of the error
    index:
        points at the origin of the error in the parsed text
    """

    error_type: ParsingErrorType
    index: int

    def __init__(self, error_type: ParsingErrorType, index: int):
        """
        Initializes the parsing error.
        The message is initialized using the enum `message` method.

        Parameters
        ----------
        error_type: ParsingErrorType
            type of the error
        index:
            points at the origin of the error in the parsed text
        """
        message = error_type.message(index)
        super().__init__(message)
        self.error_type = error_type
        self.index = index
