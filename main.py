"""
Create a Farkle match and start play.
"""

# Last update: 2021-12-02 09:37

import simpleauto
import automated
import farklematch
import platform


def main(a, b):
    """Set up a 2-player match"""

    say = platform.platform().startswith('macOS') and (input('Text-to-speech? ').strip() or 'N').upper().startswith('Y')
    match = farklematch.FarkleMatch([a, b], say=say)

    match.start_play()

    print(f'MATCH OVER! CONGRATULATIONS, {match.winner()}')

    return match.winner()


ben = automated.FarklePlayer('Ben')
jessica = simpleauto.FarklePlayer('Jessica')

main(ben, jessica)

ben = automated.FarklePlayer('Ben')
jessica = simpleauto.FarklePlayer('Jessica')

lst = [ben, jessica]
lst_1 = [ben, jessica]

for player in lst:
    for strat in lst_1:
        if strat != player:
            main(player, strat)
