import logging
import os
from collections import deque
from random import randint
from typing import Optional, NamedTuple
from unittest.mock import patch

import pytest

from wallbox.finder import file_finder, DEFAULT_MAX_SIZE

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class MockedStat(NamedTuple):
    """
    NamedTuple with mocked info
    """

    executable: bool
    st_uid: int
    st_size: int


"""
Files with all possible combinations of the three validations
"""
VALID_COMBINATION_FILE = "valid.txt"
ALL_COMBINATIONS_FILE = {
    "any_conditions.txt": MockedStat(False, 1, DEFAULT_MAX_SIZE + 1),
    "only_size.txt": MockedStat(False, 1, DEFAULT_MAX_SIZE),
    "only_user.txt": MockedStat(False, 0, DEFAULT_MAX_SIZE + 1),
    "only_access.txt": MockedStat(True, 1, DEFAULT_MAX_SIZE + 1),
    "size_and_user.txt": MockedStat(False, 0, DEFAULT_MAX_SIZE),
    "size_and_access.txt": MockedStat(True, 1, DEFAULT_MAX_SIZE),
    "user_and_access.txt": MockedStat(True, 1, DEFAULT_MAX_SIZE + 1),
    VALID_COMBINATION_FILE: MockedStat(True, 0, DEFAULT_MAX_SIZE),
}


def call_file_finder(path: str) -> Optional[str]:
    """
    Call function and add extra debug
    """
    LOGGER.debug(f"Input path: {path}")
    result = file_finder(path)
    LOGGER.debug(f"Result: {result}")
    return result


def test_non_existing_folder():
    assert not call_file_finder("__non_existing_folder__" + str(randint(0, 2 ** 30)))


def test_arg_is_a_file():
    assert not call_file_finder(__file__)


@patch("wallbox.finder.os.walk")
def test_empty_folder(walk_mock):
    walk_mock.return_value = []
    assert not call_file_finder(os.path.dirname(__file__))


@patch("wallbox.finder.os.stat")
@patch("wallbox.finder.os.access")
@patch("wallbox.finder.os.walk")
@patch("wallbox.finder.os.path.isdir")
@pytest.mark.parametrize(
    "size_and_valid",
    (
        (0, True),
        (DEFAULT_MAX_SIZE - 1, True),
        (DEFAULT_MAX_SIZE, True),
        (DEFAULT_MAX_SIZE + 1, False),
    ),
)
def test_check_length_corner_cases(
    is_dir_mock, walk_mock, access_mock, stat_mock, size_and_valid
):
    """
    Check all corner cases for the size validation.
    Other checkins are mocked and will always return True
    """

    size, valid = size_and_valid
    LOGGER.debug(f"Checking size {size} / {DEFAULT_MAX_SIZE}")

    is_dir_mock.return_value = True
    walk_mock.return_value = [["", [], [VALID_COMBINATION_FILE]]]
    access_mock.return_value = True
    stat_mock.return_value = MockedStat(True, 0, size)

    result = call_file_finder(os.path.dirname(__file__))

    if valid:
        assert result == VALID_COMBINATION_FILE
    else:
        assert result != VALID_COMBINATION_FILE


@patch("wallbox.finder.os.stat")
@patch("wallbox.finder.os.access")
@patch("wallbox.finder.os.walk")
@patch("wallbox.finder.os.path.isdir")
@pytest.mark.parametrize("roll_index", tuple(range(len(ALL_COMBINATIONS_FILE))))
def test_three_conditions_combination(
    is_dir_mock, walk_mock, access_mock, stat_mock, roll_index
):
    """
    We have a list of all possible combinations for the three validations.
    This test will rotate this list and expects always the only valid file

    Each file has a linked namedtuple with the result that the mock should return
    """

    # Mock files to be tested
    sorted_files = deque(ALL_COMBINATIONS_FILE.keys())
    sorted_files.rotate(roll_index)

    LOGGER.debug(f"Files to look in: {sorted_files}")

    # Configure mocks
    is_dir_mock.return_value = True
    walk_mock.return_value = [["", [], sorted_files]]
    access_mock.side_effect = lambda file_abspath, permissions: ALL_COMBINATIONS_FILE[
        file_abspath
    ].executable
    stat_mock.side_effect = lambda file_abspath: ALL_COMBINATIONS_FILE[file_abspath]

    assert call_file_finder(os.path.dirname(__file__)) == VALID_COMBINATION_FILE
