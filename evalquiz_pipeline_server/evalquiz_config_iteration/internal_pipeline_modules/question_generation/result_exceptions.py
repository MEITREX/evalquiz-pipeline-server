class ResultException(Exception):
    """The generated result by the language model is not able to be further processed, due to incompatibilities."""


class ResultSectionNotFoundException(ResultException):
    """The result section, marked with `<result></result>` tags was not found in the given text."""


class ResultSectionNotParsableException(ResultException):
    """The structure of the result section, marked with `<result></result>` tags does not match the QuestionType."""
