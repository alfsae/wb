from typing import Tuple, Optional


def first_repeated_number(
    array_one: Tuple[int, ...], array_two: Tuple[int, ...]
) -> Optional[int]:
    """
    A function that given 2 vectors of integers finds the first repeated number

    It iterates over the longest array and looks into the same subset of the smaller array.

    :param array_one: First vector
    :param array_two: Second vector
    :return: value. None if no repeated value.
    """

    # Sort arrays by length
    longest_array, shortest_array = sorted(
        (array_one, array_two), key=lambda x: -len(x)
    )

    # Iterate over longest array
    for index in range(1, len(longest_array) + 1):
        # Get each item of longest array subset
        for item in longest_array[:index]:
            # And check if it's in a subset with same length of the shortest array
            if item in shortest_array[:index]:
                return item

    return None
