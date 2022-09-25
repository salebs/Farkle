"""
Functions that construct the scorings for a dice roll.

A scoring is a pair(score, dice), where score is an int value and dice is a tuple of values 1 through 6.

BUGS SHOULD BE REPORTED IN PIAZZA. INCLUDE IN THE BUG REPORT THE DICE ROLL.
"""

# THIS CODE WILL BENEFIT FROM REFACTORING.


import farkle


def merge_scorings(scorings1, scorings2):
    """
    Merge the scorings for different portions of the same roll
    Args:
        scorings1: a list of scorings
        scorings2: another list of scorings

    Returns:
        A list of merged scorings
    """
    result = list(scorings1)  # Make a copy
    result.extend(scorings2)
    for score1, roll1 in scorings1:
        for score2, roll2 in scorings2:
            result.append((score1 + score2, roll1 + roll2))
    return result


def seq_scorings(top, points_each, n):
    """
    Generate a sequence of n scorings for from 1 to n values
    Args:
        top: the number on top of a die
        points_each: the number of points for each top value
        n: the number of dice with that number on top

    Returns:
        a list containing scorings for 1 roll, 2 rolls, ..., n rolls
        Example:
            seq_scorings(1, 100, 2) --> [(100, (1,)), (200, (1, 1))]
            seq_scorings(5, 50, 0) --> []
    """
    return list((points_each * k, (top,) * k) for k in range(1, n + 1))


def n_of_a_kind_scorings(top, n):
    """
    Compute a sequence of scorings for n-of-a-kind
    Args:
        top: the number occurring n times
        n: an int value between 3 and 6

    Returns:
        a list of scorings for n-of-a-kind of the value top
    """
    # When top is 1 or 5, the scoring is quite rich!

    scorings = []
    if n == 6:
        # Score as 6-of-a-kind
        scorings.append((3000, (top,) * 6))
    if n >= 5:
        # Score as 5-of-a-kind
        scorings.append((2000, (top,) * 5))
    if n >= 4:
        # Score as 4-of-a-kind
        scorings.append((1000, (top,) * 4))
    if n >= 3:
        # Score as 3-of-a-kind
        scorings.append((300 if top == 1 else top * 100, (top,) * 3))
    return scorings


def scorings_3_to_6_of_a_kind(dice_roll):
    pass


def scorings_for(dice_roll):
    """
    Find all of the ways to score a randomize of zero or more dice
    Args:
        dice_roll: a list of die values

    Returns:
        A list of zero or more 2-tuples of the form (score, selected-dice),
        where score is an integer value and selected-dice is a list of one
        or more die values. The 2-tuples are sorted from lowest score to
        highest score.  An empty list denotes a Farkle.
    """
    scorings = []

    if dice_roll:
        # There is at least one die to process
        dice_roll = list(dice_roll)  # COPY AS A list
        dice_roll.sort()

        left_roll = dice_roll[0]

        if len(dice_roll) == 1:
            if left_roll == 1:
                scorings.append((100, (1,)))
            elif left_roll == 5:
                scorings.append((50, (5,)))
        else:
            hist = farkle.histogram_for(dice_roll)

            if hist.count(1) == 6:
                # Straight
                scorings.append((1500, (1, 2, 3, 4, 5, 6)))
                scorings.append((150, (1, 5)))
                scorings.append((100, (1,)))
                scorings.append((50, (5,)))
            elif hist.count(3) == 2:
                # Two triples
                top1 = hist.index(3)  # triple 1
                top2 = hist.index(3, top1 + 1)  # triple 2
                scorings.append((2500, tuple(dice_roll)))
                scorings.append((300 if top1 == 1 else top1 * 100, (top1, top1, top1)))
                scorings.append((top2 * 100, (top2, top2, top2)))  # top2 cannot be 1
                scorings.extend(seq_scorings(1, 100, hist[1]))
                scorings.extend(seq_scorings(5, 50, hist[5]))
            elif hist.count(2) == 3:
                # Three pairs
                scorings.append((1500, tuple(dice_roll)))
                scorings.extend(seq_scorings(1, 100, hist[1]))
                scorings.extend(seq_scorings(5, 50, hist[5]))
            elif 4 in hist and 2 in hist:
                # Four of any number and a pair
                scorings.append((1500, tuple(dice_roll)))
                scorings.extend(n_of_a_kind_scorings(hist.index(4), 4))     # ignore pair
                scorings.extend(n_of_a_kind_scorings(hist.index(4), 3))     # triple
                scorings.extend(seq_scorings(1, 100, hist[1]))
                scorings.extend(seq_scorings(5, 50, hist[5]))
            elif 6 in hist:
                # Six of a kind
                scorings.extend(n_of_a_kind_scorings(hist.index(6), 6))
                scorings.extend(n_of_a_kind_scorings(hist.index(6), 5))
                scorings.extend(n_of_a_kind_scorings(hist.index(6), 4))
                scorings.extend(n_of_a_kind_scorings(hist.index(6), 3))
                scorings.extend(seq_scorings(1, 100, hist[1]))
                scorings.extend(seq_scorings(5, 50, hist[5]))
            elif hist[left_roll] == 5:
                # five-of-a-kind
                scorings.extend(n_of_a_kind_scorings(hist.index(5), 5))
                scorings.extend(n_of_a_kind_scorings(hist.index(5), 4))
                scorings.extend(n_of_a_kind_scorings(hist.index(5), 3))
                scorings.extend(seq_scorings(1, 100, hist[1]))
                scorings.extend(seq_scorings(5, 50, hist[5]))
                # scorings.extend(scorings_for(dice_roll[:1]))
                # scorings.extend(scorings_for(dice_roll[1:]))
            elif hist[left_roll] == 4:
                # 4-of-a-kind
                scorings.extend(n_of_a_kind_scorings(hist.index(4), 4))
                scorings.extend(n_of_a_kind_scorings(hist.index(4), 3))
                scorings.extend(seq_scorings(1, 100, hist[1]))
                scorings.extend(seq_scorings(5, 50, hist[5]))
                # scorings.extend(scorings_for(dice_roll[:1]))
                # scorings.extend(scorings_for(dice_roll[1:]))
            elif hist[left_roll] == 3:
                # three-of-a-kind
                scorings.extend(n_of_a_kind_scorings(hist.index(3), 3))
                scorings.extend(seq_scorings(1, 100, hist[1]))
                scorings.extend(seq_scorings(5, 50, hist[5]))
            else:
                # rolled 1 or 2 of the left number
                # Just count 1s and 5s
                if left_roll == 1:
                    scorings.extend(seq_scorings(1, 100, hist[1]))
                elif left_roll == 5:
                    scorings.extend(seq_scorings(5, 50, hist[5]))
                scorings = merge_scorings(scorings, scorings_for(dice_roll[hist[left_roll]:]))

    # Remove any duplicates
    scorings = list(set(scorings))

    # Sort from largest score to smallest
    scorings.sort(reverse=True)
    return scorings


if __name__ == '__main__':
    import random

    ROLLS = [
        (1, 2, 3, 4, 5, 6),
        (1, 3, 3, 3, 4, 6),
        (2, 3, 4, 4, 4, 4),
        (2, 3, 3, 3, 4, 4),
        (5, 5, 6, 6, 6, 6),
        (1, 1, 1, 1, 1, 1),
        (5, 5, 5, 5, 5, 5,),
        (1, 1, 1, 5, 5, 5,),
        (1, 1, 1, 1, 5, 5),
        (1, 2, 3, 4, 5, 5),
        (1, 1, 5, 6, 6, 6),
        (2, 6, 6, 6, 6, 6),
        (2, 2, 3, 5, 5, 5),
        (1, 1, 1, 1, 1, 1),
    ]

    for roll in ROLLS:
        print(f'Roll: {roll} - {scorings_for(roll)}')
        print()

    # Generate random rolls
    print('-' * 80)
    for _ in range(40):
        n = 6       # random.randint(3, 6)
        roll = tuple(sorted(random.randint(1, 6) for __ in range(n)))
        print(f'Roll: {roll} - {scorings_for(roll)}')
        print()
