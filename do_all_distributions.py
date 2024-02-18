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
    if melange_cartes[:26] != white_cards and melange_cartes[26:] != white_cards:
        game = Game()
        game.import_distribution(melange_cartes[:26], melange_cartes[26:])
        resultat = game.play()
        if resultat['winner']=='Nobody':
            infinites.append(resultat)
        else:
            best = max(best, resultat['nb_tours'])
        print(f"Best game : {best}. Infinite games : {infinites}")
        with open(file_path,'a') as file:
            file.write(json.dumps(resultat)+'\n')
        
