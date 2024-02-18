import random
import logging

class Card:
    cost = 0
    name = "-"
    def __repr__(self):
        return self.name
class As(Card):
    cost = 4
    name = "A"
class Roi(Card):
    cost = 3
    name = "K"
class Dame(Card):
    cost = 2
    name = "Q"
class Valet(Card):
    cost = 1
    name = "J"


class Cards:
    '''Un tas de cartes
    '''
    def __init__(self, cards:list[Card] = None):
        self.cards = cards or []
    def __repr__(self):
        return "".join([str(card) for card in self.cards])
    def empty(self)->bool:
        return len(self.cards)==0

class Heap(Cards):
    '''Une pile de carte
    '''
    def append(self, card:Card):
        self.cards.append(card)

    def get_cards(self)->list[Cards]:
        ''' Vide la pile et renvoie son contenu
        '''
        cards = self.cards
        self.cards= []
        return cards

class Deck(Cards):
    ''' Les cartes d'un joueur
    On pioche en début de list, on empoche en fin de list
    '''
    def pioche(self)->Card:
        if not self.empty():
            return self.cards.pop(0)
    def empoche(self, heap:Heap):
        self.cards += heap.get_cards() #list(reversed(heap.get_cards()))

class Game:
    '''Un jeux : c'est à dire une distribution
    '''
    def __init__(self, j1:list = None, j2:list=None, no_stop = False):
        '''J1 & J2 : 2 listes de distribution
        '''
        self.decks = [Deck(j1), Deck(j2)]
        self.heap = Heap()
        self.tours = [] #historique des (decks, heap)
        self.cartes_52 = [As() for i in range(4)] + [Roi() for i in range(4)] + [Dame() for i in range(4)] + [Valet() for i in range(4)] + [Card() for i in range(9*4)]
        self.player = 0
        self.winner = None
        self.no_stop = no_stop

    def import_distribution(self, j1:str, j2:str):
        '''Import une distribution sous forme de str
        '''
        card_types = {'A':As, 'K' : Roi, 'Q' : Dame, 'J' : Valet, '-' : Card}
        self.decks = [
            Deck([card_types[letter]() for letter in j1]),
            Deck([card_types[letter]() for letter in j2]),
        ]

    def alea_distribute(self):
        cards = self.cartes_52.copy()
        random.shuffle(cards)
        self.decks[0] = Deck(cards[:len(cards)//2])
        self.decks[1] = Deck(cards[len(cards)//2:])
        
    def add_tours(self, nb_cards:int):
        new = (str(self.decks[0]), str(self.decks[1]), str(self.heap))
        if not self.no_stop and nb_cards == 0 and self.player == 0 and new in self.tours:
            logging.info("EUREKA!!!")
            self.winner = "Nobody"
        else:
            self.tours.append(new)
    
    def change(self):
        self.player = (self.player + 1)%2
    
    def empoche(self):
        #self.decks[self.player] += list(reversed(self.heap))
        heap_len = len(self.heap.cards)
        self.decks[self.player].empoche(self.heap)
        logging.debug(f"Joueur {self.player} empoche {heap_len} cartes.")

    def play_turn(self, nb_cards = 0)->bool:
        '''Jour un tour pour un joueur
        renvoie vrai si le dernier jour dois empocher
        nb_card = nb de cartes de pénalité
        '''
        empoche = False
        for i in range(nb_cards or 1):
            new_card= self.decks[self.player].pioche()
            self.heap.append(new_card)
            if new_card is None:
                self.change()
                self.winner = self.player
            else:
                logging.debug(f"Joueur {self.player} ({self.decks[self.player]}): {new_card}")
                self.add_tours(nb_cards)
                if new_card.cost>0:
                    self.change()
                    empoche = self.play_turn(new_card.cost)
                    break
        if self.winner is None:
            if not empoche:
                self.change()
            empoche = empoche or nb_cards > 0
            return empoche

    def play(self)->dict:
        self.distribution = (str(self.decks[0]), str(self.decks[1]))
        while self.winner is None:
            if self.play_turn():
                self.empoche()
        logging.info(f"Gagnant : Joueur {self.winner} en {len(self.tours)} tours.")
        return {
            'distrib' : self.distribution,
            'winner' : self.winner,
            'nb_tours' : len(self.tours)
            }


if __name__ == '__main__':
    from FUTIL.my_logging import *
    my_logging(console_level = DEBUG, logfile_level = INFO, details = True)
    #jeu = Game()
    #jeu.alea_distribute()
    #jeu.play()
    j1 = [Card(),Card(), Card(), Roi(), Card(),Card(), Card(),Dame(), Card(), Roi(), Dame(), As(), Valet(), Card(),Card(), Card(),Card(),Card(), As(), As(), Valet(), Card(), Card(), Valet(), Card(), Card()]
    j2 = [Card(),Card(), Card(),Card(),Card(), Card(),Card(),Card(), Card(),Card(), Dame(),Card(),Card(), Card(),Card(), Roi(), Dame(), Card(), Valet(), Card(),Card(), Card(),Card(),Card(), Roi(), As()]
    jeu = Game(j1,j2)
    #jeu = Game(no_stop=False)
    #jeu.import_distribution("QQ--KJ-K----AK----A---Q-JA","--A--J---J--K-------Q-----")
    jeu.play()