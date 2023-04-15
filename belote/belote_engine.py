from engine import Deck, GameState
from models import BelotePlayer, Team, Suits
from models import Position
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
            if self.players[self.currentPlayer] in self.teams[0].players:
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
            non_trump_values = {1: 11, 7: 0, 8: 0, 9: 0, 10: 10, 11: 2, 12: 3, 13: 4}
            trump_values = {1: 11, 7: 0, 8: 0, 9: 14, 10: 10, 11: 20, 12: 3, 13: 4}
            if card.suit == trump:
                return trump_values[card.value]
            else:
                return non_trump_values[card.value]

        cards.sort(
            key=lambda card: (
                card.suit == self.trump,
                str(card.suit),
                get_value(card, self.trump),
            ),
            reverse=True,
        )

    def play(self, key):
        if key is None:
            return

        if self.state == GameState.ENDED:
            self.first_player_id += 1
            if self.first_player_id >= len(self.players):
                self.first_player_id = 0
            return

        if self.state == GameState.PLAYING:
            if self.players[self.currentPlayer].throw(key, self.deck):
                self.switchPlayer()
                if len(self.deck.cards) >= 4:
                    # sort list by `name` in reverse order
                    self.sort(self.deck.cards)
                    higher_card = self.deck.cards[0]
                    print(f'higher_card {higher_card}')
                    self.deck.last_handle = self.deck.cards.copy()
                    self.deck.cards = []

                if sum([len(player.hand) for player in self.players]) <= 0:
                    self.state = GameState.ENDED


        if self.state == GameState.BETTING:
            if not self.set_trump(key):
                self.switchPlayer()
