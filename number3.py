"""
The class automated.FarklePlayer makes decisions automatically based on a strategy.
"""


__AUTHOR__ = 'BEN'


class FarklePlayer:
    """ A Farkle player who makes decisions based on a programmed strategy"""

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

        # start with cont as true to read through the dictionary
        cont = True

        while roll_number == 0 or wants_to_keep_going:

            # determine what you should answer for the first question,
            # as well as risk value
            comments = {0: ((high_score >= 10000 and high_score > my_score), 'Time for hot dice!'),
                        1: ((farkle_danger_level == 2), 'I need to play it safe!'),
                        2: ((my_score == 0), 'I am ready to start!'),
                        3: ((high_score - my_score >= 1500 and high_score >= 5000),
                            'I need to catch up!'),
                        4: (True, 'No need to risk that much.')}

            # determine which parameter of the dictionary is true first,
            # then assign comment and strategy value
            for i in range(5):
                if comments[i][0] and cont:
                    strat, commentary, cont = (i, comments[i][1], False)

            # roll the die
            roll_number += 1
            scorings = match.roll(commentary)

            # determine the number of dice in the highest score selection
            nbr_in_scoring = len((scorings[0])[1])
            # determine how many dice will be left after highest score is chosen
            nbr_left = nbr_of_dice - nbr_in_scoring

            def play(ideal_score):
                """
                How the player would continue rolling if the score is not as high as desired.

                Argument-
                    ideal_score = desired score (int)

                Return-
                    choice = index of the selection with highest score and
                    lowest amount of die (int)

                    go_on = decision to roll again or not (bool)
                """
                # create empty lists for potential scores and dice
                p_scoring, p_dice = ([], [])
                for amount, dice in scorings:
                    p_scoring.append(amount)
                    p_dice.append(len(dice))

                # finding highest score and lowest amount of dice
                max_score, min_dice = (max(p_scoring), min(p_dice))

                # if the score is less than the desired score
                if max_score + score_this_turn < ideal_score:
                    # if the amount of dice is not the lowest, make the matching score be zero
                    for p_die in p_dice:
                        if min_dice < p_die:
                            p_scoring[p_dice.index(p_die)], p_dice[p_dice.index(p_die)] = (0, None)
                    # choose the scoring with the lowest amount of dice and the highest score
                    choice = p_scoring.index(max(p_scoring))
                    # determine how many dice are left
                    nbr_left_1 = nbr_of_dice - p_dice[choice]
                    # roll again if the score this turn is less than the ideal score
                    # or if the number of dice left is zero
                    go_on = bool(max_score + score_this_turn < ideal_score or nbr_left_1 == 0)
                # if the score is more than or equal to the desired score
                else:
                    # choose highest score and roll again if the amount of dice left is zero
                    choice, go_on = (0, bool(nbr_left == 0))

                # return index of choice of score, if you will roll again or not
                return [choice, go_on]

            # how to choose to roll again or not depending on strategy value
            if strat == 1:
                selection, wants_to_keep_going = (0, False)
            elif 2 <= strat <= 4:
                p_ideal_scores = [0, 0, 500, 900, 250]
                selection, wants_to_keep_going = play(p_ideal_scores[strat])
            else:
                selection, wants_to_keep_going = (0,
                                                  bool((my_score + score_this_turn) < high_score))

            # determining  and adding score to score this turn
            scoring = (scorings[selection])[0]
            score_this_turn += scoring

            # create list with score limits and appropriate responses
            comments_1 = [(50, 'Better than nothing.'), (300, 'Totally worth it!'),
                          (900, 'That was a great roll!'),
                          (2500, 'I am the ultimate Farkle player!!!')]
            # determine what to say in response to the second question
            for score, comment in comments_1:
                if score_this_turn >= score:
                    commentary_1 = comment

            # determine number of dice left and say your response
            nbr_of_dice = match.score_as(selection, commentary_1)

        # create list with scores of this turn limits and appropriate responses
        comments_2 = [(50, "At least I didn't farkle."), (300, 'That was pretty good.'),
                      (900, 'You know what? I will take it.'), (1500, 'Wow! That is a lot!'),
                      (10000, 'Good match!')]

        # determining what to say in response to the third question
        for score, comment in comments_2:
            if score_this_turn >= score or my_score + score_this_turn >= 10000:
                commentary_2 = comment

        # Turn ends
        if not scorings:
            # No scorings are available!
            print(f'Farkle after roll #{roll_number}!')

        return commentary_2
