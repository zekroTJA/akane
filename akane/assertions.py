from typing import Optional


class AssertionError(Exception):
    """
    Exception thrown when an assertion has failed.
    """

    def __init__(self, msg: str, additional_msg: Optional[str] = None):
        header = "assertion failed:"
        if additional_msg:
            header += f" ({additional_msg})"
        super().__init__(f"{header}\n{msg}")


def assert_eq(exp, rec, msg: Optional[str] = None):
    """
    Asserts that `exp` and `rec` are equal.
    If not, an `AssertionError` is returned.
    """
    if exp != rec:
        exp = str(exp).replace("\n", "\\n")
        rec = str(rec).replace("\n", "\\n")
        m = f" | expected:  {exp}\n" \
            f" | recovered: {rec}"
        raise AssertionError(m, msg)


def assert_true(rec, msg: Optional[str] = None):
    """
    Asserts that `rec` is `True`.
    If not, an `AssertionError` is returned.
    """
    if not rec:
        m = " | expected to be True"
        raise AssertionError(m, msg)


def assert_false(rec, msg: Optional[str] = None):
    """
    Asserts that `rec` is `False`.
    If not, an `AssertionError` is returned.
    """
    if rec:
        m = " | expected to be False"
        raise AssertionError(m, msg)
