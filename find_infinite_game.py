from game import Game
from FUTIL.my_logging import *
my_logging(console_level = INFO, logfile_level = INFO, details = True)
import json

file_path = "resultats_aleatoires.json"
best = 0
infinites = []
while True:
    game = Game()
    game.alea_distribute()
    resultat = game.play()
    if resultat['winner']=='Nobody':
        infinites.append(resultat)
    else:
        best = max(best, resultat['nb_tours'])
    print(f"Best game : {best}. Infinite games : {infinites}")
    with open(file_path,'a') as file:
        file.write(json.dumps(resultat)+'\n')
    
