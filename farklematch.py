"""
Defines the FarkleMatch class
"""

# Last update: 2021-12-06 15:45
#   - Modified the code so that each player gets one more turn after a player reaches 10,000.
#   - Fixed bug where a Farkle was recorded twice.
#   - Fixed a bug where a score less than 500 was recorded.
#   - Fixed a bug in which the wrong winner was reported.

# Last update: 2021-12-05 10:05
#   - Created a docstring for FarkleMatch.start_play()
#   - Added code to return the winner's name

# Last update: 2021-12-03 10:11
#   - fixed bug that recorded the wrong score for a Farkle

# Last update: 2021-12-02 10:07
#   - removed print('You rolled...')
#   - removed extraneous import statements

import os
import random
import scoresheet2
import farklescoring
import traceback
import sys


class Farkle(Exception):
    """A Farkle has been rolled"""
    pass


class FarkleMatch:
    """A Farkle match is an instance of Farkle played by one or more players"""

    VOICES = ('Alex',
              'Karen',
              'Daniel',
              'Moira',
              'Fred',
              'Rishi',
              'Samantha',
              'Tessa',
              'Veena',
              'Victoria')

    def __init__(self, players, say=False):
        """
        Initialize a match
        Args:
            players: a sequence of FarklePlayer instances. Play will follow this order.
                     Note: player_names should have unique names
        """
        self.__player_index = {player.name(): player for player in players}  # To look up a player by name
        assert len(self.__player_index) == len(players), 'ERROR: Duplicate player names!'
        self.__players = tuple(players)
        self.__player_count = len(self.__players)
        self.__score_sheet = scoresheet2.ScoreSheet(player.name() for player in self.__players)
        self.__turn_number = 0  # Used to count turns and determine current player
        self.__voice = FarkleMatch.VOICES[0]
        self.__player_voices = {player.name(): FarkleMatch.VOICES[(i + 1) % len(FarkleMatch.VOICES)]
                                for i, player in enumerate(players, 1)}
        self.__say = say
        self.__farkle_tallies = {player.name(): 0 for player in players}
        self.__eliminated_player_names = set()

        # These are used to manage a player's turn
        self.__player_taking_turn = None
        self.__dice_remaining = None
        self.__score_this_turn = None
        self.__current_roll = None
        self.__current_roll_scorings = None
        self.__player_has_farkled = None
        self.__awaiting_roll = True
        self.__awaiting_score_as = False

    def player_names(self):
        """Get the names of the player_names in this match"""
        return tuple(player.name() for player in self.__players)

    def score_for(self, player_name):
        """Get the score for a player"""
        return self.__score_sheet.score_for(player_name)

    def high_score(self):
        """Get the high score among all player_names"""
        return self.__score_sheet.high_score()

    def farkle_danger_level(self, player_name):
        """Get the Farkle danger level for the player"""
        return self.__score_sheet.farkle_danger_level(player_name)

    def winner(self):
        """Get the winner (or None if no winner yet)"""
        return self.__score_sheet.winner()

    def start_play(self):
        """Run a match and determine the winner"""
        self._say("Play beginning!", self.__voice)

        winner = self.winner()
        while winner is None:
            self.__turn_number += 1
            current_player = self.__players[(self.__turn_number - 1) % self.__player_count]
            self._manage_turn(current_player)

            print()
            print(self.__score_sheet)
            print()

            winner = self.winner()

        # The current player has reached 10,000 points. Give each other player one more turn
        self._say(f'{winner} has reached {self.high_score()} points.', self.__voice)
        self._say('Everyone else gets one more turn.', self.__voice)
        for _ in range(1, len(self.__players)):
            self.__turn_number += 1
            current_player = self.__players[(self.__turn_number - 1) % self.__player_count]
            self._manage_turn(current_player)

            print()
            print(self.__score_sheet)
            print()

        winner = self.winner()      # Could be someone else!
        self._say(f'Congratulations, {winner.upper()}!', self.__voice)
        self._say('GAME OVER', self.__voice)

        print('Match Statistics')
        print('  Winner:', winner)
        print('  Total number of turns:', self.__turn_number)
        print('  Total number of Farkles:', sum(self.__farkle_tallies.values()))
        print('   ', '\n    '.join(f'{player.name():>10}: {self.__farkle_tallies[player.name()]:>4}'
                               for player in self.__players))

        return winner

    def _manage_turn(self, player):
        """
        Manage the given player's turn
        Args:
            player: the player whose turn is starting

        Returns:

        """
        if player.name() not in self.__eliminated_player_names:
            self.__player_taking_turn = player
            self.__turn_has_ended = False
            self.__dice_remaining = 6
            self.__score_this_turn = 0
            self.__player_has_farkled = False
            self._say(f'{player.name()}\'s TURN:', self.__voice)

            player_name = player.name()
            try:
                try:
                    self.__awaiting_roll = True
                    turn_commentary = player.take_turn(self)
                    self._say(turn_commentary, self.__player_voices[player_name])
                    assert self.__awaiting_roll,\
                           'Your player did not roll and then select a scoring before returning from .take_turn()'
                except Farkle:
                    self.__farkle_tallies[player_name] += 1
                    self.__score_this_turn = 0      # Lost all points
                    self._say('Farkle!!!', self.__player_voices[player_name])
                    farkle_danger_level = self.farkle_danger_level(player_name)

                    if farkle_danger_level == 1:
                        self._say("Warning: Two Farkles in a row.", self.__voice)
                    if farkle_danger_level == 2:
                        self._say("Oh, no!  Three Farkles in a row.", self.__voice)

                self.__awaiting_roll = False
                self.__awaiting_score_as = False
                self._say(f'Your turn is over, {player_name}.', self.__voice)
                self.__turn_has_ended = True
                if self.__score_sheet.score_for(player_name) == 0 and self.__score_this_turn < 500:
                    self._say('You need at least 500 points.', self.__voice)
                self.__score_sheet.add_score(player_name, self.__score_this_turn)
            except:
                self._say('An exception has been raised.', self.__voice)
                self._say(f'{player_name} will sit out the rest of this match.', self.__voice)
                self.__eliminated_player_names.add(player_name)
                print(traceback.format_exc(), file=sys.stderr)
                print(traceback.format_exc())
                input('This player\'s code raised an exception. That bug needs to be fixed.')
                self.__awaiting_roll = False
        else:
            self._say(f'skip {player.name()}', self.__voice)

    def roll(self, comment):
        """
        Roll dice after publishing the comment. The roll is made by self.__player_taking_turn
        Args:
            comment: a comment made by the player when starting this roll

        Returns:
            scorings: a list of possible scorings for the roll, possibly empty. Each scoring in the
                      list is a 2-tuple (points, dice), where points is the point value of the scoring
                      and dice is a tuple containing a one or more of the die values in dice_roll that
                      yield those points. The list is ordered from largest point value to smallest point
                      value.

                      An empty list designates a Farkle.
        """
        assert self.__awaiting_roll, 'A player attempted to roll twice without scoring the first roll.'
        assert not self.__awaiting_score_as, 'You must call match.score_as() for the pending roll.'
        player_name = self.__player_taking_turn.name()
        player_voice = self.__player_voices[player_name]
        self._say(comment, voice=player_voice)
        self.__current_roll = self.__current_roll = tuple(random.randint(1, 6) for _ in range(self.__dice_remaining))
        roll_message = f'{player_name} rolled {" ".join(str(top) for top in self.__current_roll)}'
        self._say(roll_message, self.__voice)

        self.__current_roll_scorings = farklescoring.scorings_for(self.__current_roll)
        if not self.__current_roll_scorings:
            self.__player_has_farkled = True
            raise Farkle()

        self.__awaiting_roll = False
        self.__awaiting_score_as = True
        return self.__current_roll_scorings

    def score_as(self, scorings_index, comment):
        """
        Score the most recent roll as specified by the scorings index. The index must be valid.
        Args:
            scorings_index: The index of the scorings to use as returned by the most recent roll.
                            Note: Uses index 0 if this value is not a valid index
            comment: a player's comment about selecting this scoring
        Returns:
            The number of dice remaining after the scoring is recorded
        """
        assert self.__awaiting_score_as, 'The player needs to call match.roll() first'
        player_voice = self.__player_voices[self.__player_taking_turn.name()]
        if scorings_index < 0 or scorings_index >= len(self.__current_roll_scorings):
            self._say(f'*** INVALID SCORING INDEX. Using 0  - {self.__current_roll_scorings[0]}', self.__voice)
            scorings_index = 0
        score, dice_used = self.__current_roll_scorings[scorings_index]
        self._say(f'Score as {score}, setting aside {", ".join(str(top) for top in dice_used)}.', player_voice)
        self._say(comment, player_voice)
        self.__score_this_turn += score
        dice_remaining = len(self.__current_roll) - len(dice_used)
        if dice_remaining == 0:
            dice_remaining = 6
        self.__dice_remaining = dice_remaining

        self.__awaiting_score_as = False
        self.__awaiting_roll = True
        return dice_remaining

    def _say(self, message, voice):
        """Display a message"""
        print(message)
        if self.__say:
            cleaned_message = message.replace('"', ' ')
            # print(f'say -v "{voice}" "{cleaned_message}"')      # DEBUG
            os.system(f'say -v "{voice}" "{cleaned_message}"')