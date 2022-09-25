"""
Farkle functions.

Note a "die value" is one of 1, 2, 3, 4, 5, or 6.

The function main() runs test cases for each function. If an  Assertion Error
occurs, then a test case failed.
"""

import random


def randomize(dice):
    """
    Randomize one or more die values
    Args:
        dice: a list of die values

    Returns:
        None
        Side effect: Each item in dice is replaced by a random die value
    """
    for i in range(len(dice)):
        dice[i] = random.randint(1, 6)


def histogram_for(dice):
    """
    Create a histogram of the top values of zero or more dice
    Args:
        dice: a list (possibly empty) of die values

    Returns:
        a list H such that H[0] is 0 and H[i] is the number of occurrences
        of i in the list, 0 < i ≤ 6.
    """
    result = [0, 0, 0, 0, 0, 0, 0]
    for number in dice:
        result[number] += 1
    return result


def set_aside_dice(dice, selected_dice):
    """
    Set aside a subset of a list of dice
    Args:
        dice: a list of integer values between 1 and 6, inclusive
        selected_dice:  a list of integer values between 1 and 6, inclusive
                        Constraints:
                            1. len(selected_dice) <= len(dice)
                            2. dice contains all of the values in selected_dice

    Returns:
        A list containing the dice remaining after each of the selected dice
        is removed.  Note: The original lists are left unmodified.
    """

    result = list(dice)  # make a copy
    for top in selected_dice:
        assert top in result
        result.remove(top)
    return result


def main():
    """
    Test the functions above. The first test case failure will terminate program execution.
    """
    # First set the seed to a known value so we get the same sequence of random numbers every run
    random.seed(7771)

    # Test randomize() -- relies on seed being 7771
    print('TESTING randomize()')
    dice_6 = [None, None, None, None, None, None]
    print(f'  randomize({dice_6})')
    randomize(dice_6)
    print(f'    --> {dice_6}')
    assert dice_6 == [5, 5, 5, 5, 1, 4], '    FAIL: expected [5, 5, 5, 5, 1, 4]'
    print(f'  randomize({dice_6})')
    randomize(dice_6)
    print(f'    --> {dice_6}')
    assert dice_6 == [5, 1, 2, 3, 3, 1], '    FAIL: expected [5, 1, 2, 3, 3, 1]'

    dice_5 = [None, None, None, None, None]
    print(f'  randomize({dice_5})')
    randomize(dice_5)
    print(f'    --> {dice_5}')
    assert dice_5 == [6, 2, 6, 1, 4], '    FAIL: expected [6, 2, 6, 1, 4]'
    print(f'  randomize({dice_5})')
    randomize(dice_5)
    print(f'    --> {dice_5}')
    assert dice_5 == [4, 1, 1, 3, 1], '    FAIL: expected [4, 1, 1, 3, 1]'

    dice_1 = [None]
    print(f'  randomize({dice_1})')
    randomize(dice_1)
    print(f'    --> {dice_1}')
    assert dice_1 == [1], '    FAIL: expected [1]'
    print(f'  randomize({dice_1})')
    randomize(dice_1)
    print(f'    --> {dice_1}')
    assert dice_1 == [4], '    FAIL: expected [4]'

    # Test histogram_for()
    histogram_for_test_cases = (
        ([1, 1, 1, 2, 3, 4], [0, 3, 1, 1, 1, 0, 0]),
        ([1, 5, 1, 5, 1, 5], [0, 3, 0, 0, 0, 3, 0]),
        ([1, 2, 3, 4, 5, 6], [0, 1, 1, 1, 1, 1, 1]),
        ([4, 1, 4, 4, 2, 4], [0, 1, 1, 0, 4, 0, 0]),
        ([5, 5, 1, 1], [0, 2, 0, 0, 0, 2, 0]),
        ([1, 2, 1, 2, 1], [0, 3, 2, 0, 0, 0, 0]),
        ([5], [0, 0, 0, 0, 0, 1, 0]),
        ([6, 6], [0, 0, 0, 0, 0, 0, 2]),
    )
    for dice, expected_hist in histogram_for_test_cases:
        print(f'  histogram_for({dice})')
        result_hist = histogram_for(dice)
        print(f'    --> {result_hist}')
        assert result_hist == expected_hist, \
            f'    FAIL: expected {expected_hist}'

    # Test set_aside_test_cases()
    set_aside_test_cases = (
        ([1, 2, 2, 5, 1, 6], [1, 5], [1, 2, 2, 6]),
        ([3, 4, 2, 3, 3, 3], [3, 3, 3], [2, 3, 4]),
        ([1, 1, 4, 5], [5], [1, 1, 4]),
        ([1, 1, 1, 1, 6, 5], [1, 1, 1], [1, 5, 6]),
        ([5, 5, 5], [5, 5, 5], []),
    )
    print('TESTING CALLS TO set_aside_test_cases()')
    for dice, selected_dice, expected_result in set_aside_test_cases:
        print(f'  set_aside_test_cases({dice}, {selected_dice}')
        dice_copy = list(dice)
        selected_dice_copy = list(selected_dice)
        result = set_aside_dice(dice, selected_dice)
        print(f'    --> {result}')
        assert dice == dice_copy, \
            '    FAIL: the function changed dice'
        assert selected_dice == selected_dice_copy, \
            '    FAIL: the function changed selected_dice'
        assert sorted(result) == sorted(expected_result), \
            f'    FAIL: expected: {expected_result}.  Note: order does not matter.'

    print('DONE')


if __name__ == '__main__':
    main()
