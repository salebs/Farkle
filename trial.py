import main
import simpleauto
import automated
import number1
import number2
import number3

ben_score = 0
jessica_score = 0
bg_score = 0
stevie_score = 0
maeve_score = 0

for i in range(3):
    ben = automated.FarklePlayer('Ben')
    jessica = simpleauto.FarklePlayer('Jessica')
    bg = number1.FarklePlayer('BG')
    stevie = number2.FarklePlayer('Stevie')
    maeve = number3.FarklePlayer('Maeve')

    lst = [ben, jessica, bg, stevie, maeve]
    lst_1 = [ben, jessica, bg, stevie, maeve]

    for player in lst:
        for strat in lst_1:
            if strat != player:
                winner = main.main(player, strat)
                winner_0 = main.main(player, strat)
                winner_1 = main.main(player, strat)
                if winner == 'Ben' or winner_0 == 'Ben' or winner_1 == 'Ben':
                    ben_score += 1
                if winner == 'Jessica' or winner_0 == 'Jessica' or winner_1 == 'Jessica':
                    jessica_score += 1
                if winner == 'BG' or winner_0 == 'BG' or winner_1 == 'BG':
                    bg_score += 1
                if winner == 'Stevie' or winner_0 == 'Stevie' or winner_1 == 'Stevie':
                    stevie_score += 1
                if winner == 'Maeve' or winner_0 == 'Maeve' or winner_1 == 'Maeve':
                    maeve_score += 1

overall = [ben_score, jessica_score, bg_score, stevie_score, maeve_score]
players = ["Ben", "Jessica", "BG", "Stevie", "Maeve"]
overall_max = max(overall)
overall_winner = players[overall.index(overall_max)]

print(f'Congratulations {overall_winner} on being overall winner!')
print(f'Overall score of Ben: {ben_score}')
print(f'Overall score of Jessica: {jessica_score}')
print(f'Overall score of BG: {bg_score}')
print(f'Overall score of Stevie: {stevie_score}')
print(f'Overall score of Maeve: {maeve_score}')
