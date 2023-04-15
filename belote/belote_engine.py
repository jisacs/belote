from engine import Deck, GameState
from models import BelotePlayer, Team, Suits, Card
from models import Position
from time import sleep


class BeleteEngine:
    non_trump_values = {1: 11, 7: 0, 8: 0, 9: 0, 10: 10, 11: 2, 12: 3, 13: 4}
    trump_values = {1: 11, 7: 0, 8: 0, 9: 14, 10: 10, 11: 20, 12: 3, 13: 4}
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
        self.player1 = BelotePlayer("Player 1", Position(50, 100))
        self.player2 = BelotePlayer("Player 2", Position(50, 250))
        self.player3 = BelotePlayer("Player 3", Position(50, 400))
        self.player4 = BelotePlayer("Player 4", Position(50, 550))
        self.players = [
            self.player1,
            self.player2,
            self.player3,
            self.player4,
        ]
        self.error_msg = "N/A"
        self.teams = [
            Team([self.player1, self.player3]),
            Team([self.player2, self.player4]),
        ]
        self.first_player_id = 0
        self.currentPlayer = 0
        self.trump = None
        self.active_team = None
        self.state = GameState.BETTING
        self.deal()
        self.dispose_cards()

    def deal(self):
        half = self.deck.length() // 4
        for i in range(0, half):
            for player in self.players:
                player.draw(self.deck)

    def sort_all(self):
        for player in self.players:
            self.sort(player.hand)

    def dispose_cards(self):
        for player in self.players:
            self.sort(player.hand)
            player.dispose_cards()

    def switchPlayer(self):
        self.currentPlayer += 1
        if self.currentPlayer >= 4:
            self.currentPlayer = 0

    def set_trump(self, key):
        if key in [99, 115, 104, 100]:
            self.trump = Suits.suit(key)
            if self.current_player() in self.teams[0].players:
                self.active_team = self.teams[0]
            else:
                self.active_team = self.teams[1]

            self.state = GameState.PLAYING
            self.currentPlayer = self.first_player_id
            print(f"self.currentPlayer {self.currentPlayer}")
            return True
        else:
            return False

    def sort(self, cards):
        def get_value(card, trump):
            if card.suit == trump:
                return self.trump_values[card.value]
            else:
                return self.non_trump_values[card.value]

        cards.sort(
            key=lambda card: (
                card.suit == self.trump,
                str(card.suit),
                get_value(card, self.trump),
            ),
            reverse=True,
        )

    def current_player(self):
        return self.players[self.currentPlayer]

    def best_trump_card(self, player):
        best = Card(self.trump, 7)
        for card in player.hand:
            if card.suit == self.trump:
                if self.trump_values[card.value] > best.value:
                    best = card
        return best

    def main_game(self, key):

        # If it is the firt card of the round set the currentsuit
        if len(self.deck.cards) == 1:
            self.currentsuit = self.deck.cards[0].suit

        figure = key - 48
        if 1 > figure or figure > len(self.current_player().hand):
            return False
        print(f'figure {figure}, len(self.hand {len(self.current_player().hand)}')

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
                self.sort(self.deck.cards)
                best_card = self.deck.cards[0]
                print(f'best_card {best_card}, selected_card {selected_card} ')
                if self.trump_values[selected_card.value] < self.trump_values[best_card.value]:
                    # Sauf si on ne peut pas
                    print(f' self.best_trump_card(self.current_player()) { self.best_trump_card(self.current_player())} ')
                    if self.trump_values[self.best_trump_card(self.current_player()).value] > self.trump_values[best_card.value]:
                        self.error_msg = f"Tu dois monter a l atout {self.currentsuit}"
                        return False

        self.error_msg = f"N/A"
        self.deck.cards.append( self.current_player().hand.pop(figure - 1))
        self.dispose_cards()
        self.switchPlayer()


        # If fin de manche, on designe le vainceur,vide le vide et reset le current suit
        if len(self.deck.cards) >= 4:
            # sort list by `name` in reverse order
            self.sort(self.deck.cards)
            higher_card = self.deck.cards[0]
            print(f'higher_card {higher_card}')
            self.deck.last_handle = self.deck.cards.copy()
            self.deck.cards = []
            self.currentsuit = None

        # Plus personne n 'a de carte on arrete la partie
        if sum([len(player.hand) for player in self.players]) <= 0:
            self.state = GameState.ENDED


        """
            if selected_card.suit == trump:
                # Atout obliger de monter sans si un seul atout
                if len(deck.cards) == 0:
                    deck.cards.append(self.hand.pop(figure - 1))
                    self.dispose_cards()
                    return True

                for card in deck.cards:
                    if self.trump_values[card.value] > self.trump_values[selected_card.value] or \
                            len([card.suit == trump for card in self.hand]) >= 1:
                        deck.cards.append(self.hand.pop(figure - 1))
                        self.dispose_cards()
                        return True

            print(f'DEBUG selected_card.suit {selected_card.suit}  suit {suit}')
            if selected_card.suit != suit:
                return False
            else:
                deck.cards.append(self.hand.pop(figure - 1))
                self.dispose_cards()
                return True
        else:
            deck.cards.append(self.hand.pop(figure - 1))
            self.dispose_cards()
            return True
        print(f'throw {self.current_player().name}')
        self.switchPlayer()
        if len(self.deck.cards) >= 4:
            # sort list by `name` in reverse order
            self.sort(self.deck.cards)
            higher_card = self.deck.cards[0]
            print(f'higher_card {higher_card}')
            self.deck.last_handle = self.deck.cards.copy()
            self.deck.cards = []
            self.currentsuit = None

        self.current_player().throw(key, self.deck)

        if sum([len(player.hand) for player in self.players]) <= 0:
            self.state = GameState.ENDED
        """

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


