import logging
from typing import Tuple, Optional

from wallbox.repeated import first_repeated_number

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def call_first_repeated_number(
    array_one: Tuple[int, ...], array_two: Tuple[int, ...]
) -> Optional[int]:
    """
    Call function and add extra debug
    """
    LOGGER.debug(f"Array 1: {array_one}  |  Array 2: {array_two}")
    result = first_repeated_number(array_one, array_two)
    LOGGER.debug(f"Result: {result}")
    return result


def test_in_arg_one():
    result = call_first_repeated_number((3, 1, 2), (2, 3, 1))
    assert result == 3


def test_in_arg_two():
    result = call_first_repeated_number((3, 1, 0), (0, 0, 0, -1, 1))
    assert result == 0


def test_multiple_options():
    result = call_first_repeated_number((3, 1), (1, 3, 0))
    assert result in (3, 1)


def test_first_item():
    result = call_first_repeated_number((1, 2, 3, 4, 5, 0), (1, 7, 8, 9, 0))
    assert result == 1


def test_last_item():
    result = call_first_repeated_number((1, 2, 3, 4, 5, 0), (6, 7, 8, 9, 0))
    assert result == 0


def test_empty():
    result = call_first_repeated_number((), ())
    assert result is None


def test_no_repeated_number():
    result = call_first_repeated_number((3, 1, 2), (4, 5, 6))
    assert result is None
