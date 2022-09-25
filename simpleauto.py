"""
The class simpleauto.FarklePlayer always rolls once and uses the highest scoring
"""

import consoleui

__AUTHOR__ = 'DAVID SYKES'


class FarklePlayer:
    """ A Farkle player who rolls only once each turn"""

    FARKLE_ODDS = (None, 2 / 3, 1 / 2.3, 1 / 3.6, 1 / 6.4, 1 / 13, 1 / 43.2)

    def __init__(self, name):
        """Initialize a player with a given name"""
        self._name = name

    def name(self):
        """Get this player's name"""
        return self._name

    def take_turn(self, match):
        """
        Take my turn, which comprises at least one roll of 6 dice
        Args:
            match:

        Returns:
            a comment string about this turn
        """

        # INSTRUCTIONS: A turn consists of
        #   1. rolling the available dice
        #   2. determining which of the available scorings to use
        #   3. determine whether to loop back to step 1
        #
        #   If a Farkle is rolled, then the turn is ended and play moves to the next player

        my_score = match.score_for(self.name())
        high_score = match.high_score()
        farkle_danger_level = match.farkle_danger_level(self.name())

        wants_to_keep_going = True
        roll_number = 0
        score_this_turn = 0
        nbr_of_dice = 6          # Start with 6
        scorings = None
        while roll_number == 0 or wants_to_keep_going:

            roll_number += 1
            print(f'Roll #{roll_number}:')
            commentary = "Let's roll!"
            scorings = match.roll(commentary)

            selection = 0       # Always use the highest scoring
            scoring, dice_to_use = scorings[selection]
            score_this_turn += scoring
            commentary = f'{scoring} points looks good to me.'
            nbr_of_dice = match.score_as(selection, commentary)

            wants_to_keep_going = False

        # Turn ends
        if not scorings:
            # No scorings are available!
            print(f'Farkle after roll #{roll_number}!')

        return commentary