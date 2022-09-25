"""
The class human.FarklePlayer makes decisions based on direction from a human.
"""

import consoleui

__AUTHOR__ = 'DAVID SYKES'


class FarklePlayer:
    """ A Farkle player who takes directions interactively"""

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

        print(f'Your turn, {self.name()}.')
        print(f'Your score is {my_score}. The high score is {high_score}')
        if farkle_danger_level > 0:
            print(f'  Farkle danger level {farkle_danger_level}.')

        wants_to_keep_going = True
        roll_number = 0
        score_this_turn = 0
        nbr_of_dice = 6          # Start with 6
        scorings = None
        while roll_number == 0 or (wants_to_keep_going and scorings):

            roll_number += 1
            print(f'Roll #{roll_number}:')
            commentary = input(f'Enter your thoughts before you make roll #{roll_number}: ').strip()
            scorings = match.roll(commentary)

            # Determine the scoring to use by constructing a menu and then getting a selection
            menu_items = [f'{" ".join(str(die) for die in dice):12} - {scoring} pts'
                          for scoring, dice in scorings]
            selection = consoleui.input_menu_selection(menu_items, 'Which scoring? ')

            scoring, dice_to_use = scorings[selection]
            score_this_turn += scoring
            commentary = input(f'Your thoughts about selecting {dice_to_use}: ').strip()
            nbr_of_dice = match.score_as(selection, commentary)

            print(f'Your score for this turn so far is {score_this_turn}.')
            if my_score == 0 and score_this_turn < 500:
                print('  REMEMBER THAT YOU NEED 500 POINTS TO GET ON THE BOARD.')
            print(f'  The probability of a Farkle rolling {nbr_of_dice} dice is '
                  f'{round(self.FARKLE_ODDS[nbr_of_dice], 2)}')
            prompt = f'Do you want to roll {nbr_of_dice} dice? '
            wants_to_keep_going = consoleui.input_menu_selection(['Yes', 'No'], prompt) == 0

        # Turn ends
        if not scorings:
            # No scorings are available!
            print(f'Farkle after roll #{roll_number}!')

        return input('Enter your thoughts about this turn: ').strip()
