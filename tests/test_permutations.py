import logging
from typing import Union

import pytest

from wallbox.permutation import min_quantity_of_permutations

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


def call_min_quantity_of_permutations(*sequence: Union[bool, int]) -> int:
    """
    Call function and add extra debug
    """
    LOGGER.debug(f"Input sequence: {sequence}")
    result = min_quantity_of_permutations(*sequence)
    LOGGER.debug(f"Result: {result}")
    return result


def test_empty():
    result = call_min_quantity_of_permutations()
    assert result == 0


def test_one_item():
    result = call_min_quantity_of_permutations(0)
    assert result == 0


def test_two_items_intersect():
    result = call_min_quantity_of_permutations(1, 0)
    assert result == 0


def test_example():
    result = call_min_quantity_of_permutations(0, 1, 1, 0)
    assert result == 2


def test_wrong_start():
    result = call_min_quantity_of_permutations(0, 1, 1, 0, 1, 0, 1, 0, 1, 0)
    assert result == 2


def test_wrong_end():
    result = call_min_quantity_of_permutations(1, 0, 1, 0, 1, 0, 1, 0, 0, 1)
    assert result == 2


@pytest.mark.parametrize("value", [0, 1])
@pytest.mark.parametrize("length", tuple(range(2, 100)))
def test_same_value(value, length):
    sequence = [value] * length
    expected_changes = int(length / 2)
    result = call_min_quantity_of_permutations(*sequence)
    assert result == expected_changes
