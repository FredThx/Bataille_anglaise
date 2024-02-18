from game import Game
from FUTIL.my_logging import *
my_logging(console_level = INFO, logfile_level = INFO, details = True)
import json
from more_itertools import distinct_permutations

file_path = "resultats.json"
best = 0
infinites = []
cartes = ['A','K','Q','J']*4+['-']*4*9
white_cards = tuple(['-']*26)
for melange_cartes in distinct_permutations(cartes):
    j1 = [melange_cartes[2*i] for i in range(26)]
    j2 = [melange_cartes[2*i+1] for i in range(26)]
    if j1 != white_cards and j2 != white_cards:
        game = Game()
        game.import_distribution(j1,j2)
        resultat = game.play()
        if resultat['winner']=='Nobody':
            infinites.append(resultat)
        else:
            best = max(best, resultat['nb_tours'])
        print(f"Best game : {best}. Infinite games : {infinites}")
        with open(file_path,'a') as file:
            file.write(json.dumps(resultat)+'\n')
        
