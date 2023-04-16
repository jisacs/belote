from engine import Deck, GameState
from models import BelotePlayer, Team, Suits, Card
from models import Position
import utils
from time import sleep


class BeleteEngine:
    deck = None
    player1 = None
    player2 = None
    player4 = None
    player4 = None
    players = None
    state = None
    first_player_id = None
    currentPlayer = None
    result = None
    currentsuit = None


    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player1 = BelotePlayer("Bob", Position(50, 100))
        self.player2 = BelotePlayer("Tom", Position(50, 250))
        self.player3 = BelotePlayer("Joe", Position(50, 400))
        self.player4 = BelotePlayer("Mat", Position(50, 550))
        self.players = [
            self.player1,
            self.player2,
            self.player3,
            self.player4,
        ]
        self.error_msg = "N/A"
        self.teams = [
            Team("Bob Joe", [self.player1, self.player3]),
            Team("Tom MAt", [self.player2, self.player4]),
        ]
        self.first_player_id = 0
        self.currentPlayer = 0
        self.trump = None
        self.state = GameState.BETTING
        self.deal()
        self.dispose_cards()

    def get_team(self, player):
        for team in self.teams:
            if player in team.players:
                return team
        return None

    def deal(self):
        half = self.deck.length() // 4
        for i in range(0, half):
            for player in self.players:
                player.draw(self.deck)

    def sort_all(self):
        for player in self.players:
            utils.sort(player.hand, self.trump)

    def dispose_cards(self):
        for player in self.players:
            utils.sort(player.hand, self.trump)
            player.dispose_cards()

    def switchPlayer(self):
        self.currentPlayer += 1
        if self.currentPlayer >= 4:
            self.currentPlayer = 0

    def set_trump(self, key):
        if key in [99, 115, 104, 100]:
            self.trump = Suits.suit(key)
            self.state = GameState.PLAYING
            self.currentPlayer = self.first_player_id
            return True
        else:
            return False

    def current_player(self):
        return self.players[self.currentPlayer]

    def main_game(self, key):

        # If it is the firt card of the round set the currentsuit
        if len(self.deck.cards) == 1:
            self.currentsuit = self.deck.cards[0].suit

        figure = key - 48
        if 1 > figure or figure > len(self.current_player().hand):
            return False

        selected_card = self.current_player().hand[figure - 1]

        # If a suit is asking, the player have to play the same, if he can
        if self.currentsuit:

            if selected_card.suit != self.currentsuit:
                if self.current_player().count_suit(self.currentsuit) >= 1:
                    self.error_msg = f"Il faut jouer {self.currentsuit} comme demandé"
                    return False
                # Si pas la couleur demander, le joueur doit couper si il le peu
                if self.current_player().count_suit(self.trump) >= 1:
                    if selected_card.suit != self.trump:
                        self.error_msg = f"Tu dois couper {self.currentsuit}"
                        return False

        if selected_card.suit == self.trump:
            # A l atout on doit monter
            if len(self.deck.cards) > 0:
                best_deck_card = utils.best_card(self.deck.cards, self.trump)
                if utils.card_value(selected_card, self.trump) < utils.card_value(best_deck_card, self.trump):
                    # Sauf si on ne peut pas
                    if utils.card_value(utils.best_card(self.current_player().hand, self.trump, filter=self.trump), self.trump) >\
                            utils.card_value(best_deck_card, self.trump):
                        self.error_msg = f"{self.current_player().name} Tu dois monter a l atout {self.currentsuit} avec " \
                                         f"{utils.best_card(self.current_player().hand, self.trump)}"
                        return False

        #A chaque tour on met a jour le tenant de la maine
        if len(self.deck.cards) == 0 or utils.card_value(utils.best_card(self.deck.cards, self.trump), self.trump) > utils.card_value(selected_card, self.trump):
            self.deck.current_best_player = self.current_player()

        self.error_msg = f"N/A"
        self.deck.cards.append(self.current_player().hand.pop(figure - 1))
        self.dispose_cards()
        self.switchPlayer()

        # If fin de manche, on désigne le vainqueur,vide le vide et reset le current suit
        if len(self.deck.cards) >= 4:
            # L equipe qui remporte cette maine prend les cartes
            team = self.get_team(self.deck.current_best_player)
            # Compute score
            team.score += utils.get_points(self.deck.cards, self.trump)
            self.deck.last_handle = self.deck.cards.copy()
            self.deck.cards = []
            self.currentsuit = None

        # Plus personne n 'a de carte on arrete la partie
        if sum([len(player.hand) for player in self.players]) <= 0:
            #Dix de der
            team.score += 10
            #self.state = GameState.ENDED

    def play(self, key):
        if key is None:
            return

        if self.state == GameState.ENDED:
            self.first_player_id += 1
            if self.first_player_id >= len(self.players):
                self.first_player_id = 0
            return

        if self.state == GameState.PLAYING:
            self.main_game(key)

        if self.state == GameState.BETTING:
            if not self.set_trump(key):
                self.switchPlayer()
            else:
                self.state = GameState.PLAYING
                self.dispose_cards()


