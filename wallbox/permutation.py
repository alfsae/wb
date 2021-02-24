"""
Implements permutation calculator
"""

from typing import Union


def min_quantity_of_permutations(*sequence: Union[bool, int]) -> int:
    """
    A function that given a sequence of coin flips (0 is tails, 1 is heads) finds the
    minimum quantity of permutations so that the sequence ends interspersed.

    For example, given the sequence 0,1,1,0 how many changes are needed
    so that the result is 0,1,0,1

    :param sequence: Tuple with input arguments packed
    :return: Number of changes

    We will compare the received sequence with the two ideal sequences of the same length:
    [0, 1, 0, ...] and [1, 0, 1, ...]
    We don't need to create those arrays. Iterating over the sequence and knowning
    the value and the index we can compare it with both expected ideal values
    in the same position
    """

    starting_one_dif = 0
    starting_zero_dif = 0

    if len(sequence) > 1:
        for index, item in enumerate(sequence):
            is_odd = index % 2
            starting_zero_dif += (not is_odd and item) or (is_odd and not item)
            starting_one_dif += (not is_odd and not item) or (is_odd and item)

    return min(starting_one_dif, starting_zero_dif)
