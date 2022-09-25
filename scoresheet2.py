"""
Handle Farkle score keeping.
"""

# Updates 2021-12-06
#    - Fixed a bug in which a second score below 500 was added at the top of the score sheet
#      when it should not have been added.
#    - Fixed a bug that reported Farkle danger level incorrectly when no score had yet been recorded.

# Updates 2021-12-03  15:03
#    - Added a mark for points under 500 scored at the start of a match


class ScoreSheet:
    """
    A Farkle score sheet for one or more players.
    """

    def __init__(self, player_names):
        """
        Initialize a new score sheet
        Args:
            player_names: a set of player names
        """
        # Create a dictionary whose keys are player names and whose values are lists of numbers,
        # initially an empty list
        self._score_sheet = {player_name: [] for player_name in player_names}

    def add_score(self, player_name, score):
        """
        Add a score for the player whose name is given
        Args:
            player_name: a player's name
            score: a non-negative integer value. None is a Farkle

            Notes:
                - Three Farkles in a row results in a score of -1,000
                - the first score recorded must be 500 or higher; a smaller first score
                  is not added
        Returns:
            None
        """
        scores = self._score_sheet[player_name]
        if len(scores) > 0 and scores[-1] is not None:
            # This player already has at least one score recorded
            if score == 0:
                # Scores as 0 unless two Farkles (0s) precede it
                if self.farkle_danger_level(player_name) == 2:
                    # Triple Farkle!!!
                    scores.append(-1000)
                else:
                    scores.append(0)
            else:
                scores.append(score)
        elif score >= 500:
            # this is an acceptable first score
            scores.append(score)
        else:
            scores.append(None)     # No score

    def score_for(self, player_name):
        """
        Get the current score for the given player
        Args:
            player_name: a player's name
        Returns:
            the current score for the given player
        """
        return sum(item for item in self._score_sheet[player_name] if item is not None)

    def farkle_danger_level(self, player_name):
        """
         Get the number of Farkles at the bottom of a player's score, a number between 0 and 2
         Args:
             player_name: a player's name
         Returns:
             a number between 0 and 2
         """
        scores = self._score_sheet[player_name]
        if len(scores) < 2 or scores[-1] is None or scores[-1] > 0:
            danger_level = 0
        elif scores[-2] == 0:
            # The last TWO scores are zero
            danger_level = 2
        else:
            # The last score is 0, but the one before it is not
            danger_level = 1
        return danger_level

    def winner(self):
        """
         Return the winner's name if the game has been won, None otherwise

         Returns:
             The name of a player whose score is at least 10,000 and None if
             no player has a score of at least 10,000.
        """
        for player_name in self._score_sheet:
            if self.score_for(player_name) >= 10000:
                return player_name

        return None

    def high_score(self):
        """
         Get the high score on the score sheet

         Returns:
             The highest score on this score sheet
         """
        return max(self.score_for(player_name) for player_name in self._score_sheet)

    def __str__(self):
        """
        produce a string version of this score sheet
        Args:
            score_sheet: a score sheet as created by create_score_sheet()

        Returns:
            None
            Side effect: print the score c ard
        """
        result = []     # Accumulate lines of output

        # Print the player names followed by a line
        next_line = ''
        for player_name in self._score_sheet:
            next_line += f'|{player_name:>12}'
        next_line += '|'
        result.append(next_line)
        next_line = '+------------' * len(self._score_sheet) + '+'
        result.append(next_line)

        # Build a list of scores columns and then make all the columns the same length
        # These "columns" are copies of the lists in the score sheet
        score_grid = [self._score_sheet[player_name].copy() for player_name in self._score_sheet]
        longest_column_length = max(len(col) for col in score_grid)
        for col in score_grid:
            col.extend([''] * (longest_column_length - len(col)))

        # Display the scores row-by-row
        for row in range(len(score_grid[0])):
            next_line = ''
            for col in range(len(score_grid)):
                score = score_grid[col][row] if score_grid[col][row] is not None else '*'
                next_line += f'|{score:>12}'
            next_line += '|'
            result.append(next_line)

        # Display the totals
        next_line = '+============' * len(self._score_sheet) + '+'
        result.append(next_line)
        next_line = ''
        for player_name in self._score_sheet:
            next_line += f'|{self.score_for(player_name):>12}'
        next_line += '|'
        result.append(next_line)

        return '\n'.join(result)


def main():
    """Test code"""

    # This code calls methods, but does not check any of the results

    # Create a new score sheet
    score_sheet = ScoreSheet(['David', 'Susan', 'Aaron'])
    print(score_sheet)
    print(f'Farkle danger level {score_sheet.farkle_danger_level("David")} -- should be 0 for empty column')

    # Add some scores
    score_sheet.add_score('David', 1200)
    score_sheet.add_score('Susan', 2000)
    score_sheet.add_score('Aaron', 100)
    print(f'high score: {score_sheet.high_score()}')
    print(f'winner: {score_sheet.winner()}')

    print('\nAfter adding three scores')
    print(score_sheet)
    print(f'David\'s Farkle danger level: {score_sheet.farkle_danger_level("David")}')
    print(f'Susan\'s Farkle danger level: {score_sheet.farkle_danger_level("Susan")}')
    print(f'Aaron\'s Farkle danger level: {score_sheet.farkle_danger_level("Aaron")}')

    score_sheet.add_score('David', 4400)
    score_sheet.add_score('Susan', 5000)
    score_sheet.add_score('Aaron', 1000)

    print('\nAfter adding three more scores')
    print(score_sheet)
    print(f'high score: {score_sheet.high_score()}')
    print(f'winner: {score_sheet.winner()}')
    print(f'David\'s Farkle danger level: {score_sheet.farkle_danger_level("David")}')
    print(f'Susan\'s Farkle danger level: {score_sheet.farkle_danger_level("Susan")}')
    print(f'Aaron\'s Farkle danger level: {score_sheet.farkle_danger_level("Aaron")}')

    score_sheet.add_score('David', 4000)
    score_sheet.add_score('Susan', 100)
    score_sheet.add_score('Aaron', 0)

    print('\nAfter adding three more scores')
    print(score_sheet)
    print(f'high score: {score_sheet.high_score()}')
    print(f'winner: {score_sheet.winner()}')
    print(f'David\'s Farkle danger level: {score_sheet.farkle_danger_level("David")}')
    print(f'Susan\'s Farkle danger level: {score_sheet.farkle_danger_level("Susan")}')
    print(f'Aaron\'s Farkle danger level: {score_sheet.farkle_danger_level("Aaron")}')

    score_sheet.add_score('David', 400)
    score_sheet.add_score('Susan', 500)
    score_sheet.add_score('Aaron', 0)

    print('\nAfter adding three more scores')
    print(score_sheet)
    print(f'high score: {score_sheet.high_score()}')
    print(f'winner: {score_sheet.winner()}')
    print(f'David\'s Farkle danger level: {score_sheet.farkle_danger_level("David")}')
    print(f'Susan\'s Farkle danger level: {score_sheet.farkle_danger_level("Susan")}')
    print(f'Aaron\'s Farkle danger level: {score_sheet.farkle_danger_level("Aaron")}')

    score_sheet.add_score('David', 0)
    score_sheet.add_score('Susan', 500)
    score_sheet.add_score('Aaron', 0)

    print('\nAfter adding three more scores')
    print(score_sheet)

    print(f'winner: {score_sheet.winner()}')
    print(f'high score: {score_sheet.high_score()}')
    print(f'David\'s Farkle danger level: {score_sheet.farkle_danger_level("David")}')
    print(f'Susan\'s Farkle danger level: {score_sheet.farkle_danger_level("Susan")}')
    print(f'Aaron\'s Farkle danger level: {score_sheet.farkle_danger_level("Aaron")}')


if __name__ == '__main__':
    main()