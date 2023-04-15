from engine import Deck, GameState, Pile
from models import BelotePlayer, Team, Suits
from models import Position


class BeleteEngine:
    deck = None
    player1 = None
    player2 = None
    player4 = None
    player4 = None
    players = None
    state = None
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
        self.pile = Pile()
        self.deal()
        self.sort()
        self.dispose_cards()
        self.currentPlayer = 0
        self.trump = None
        self.active_team = None
        self.state = GameState.BETTING

    def deal(self):
        half = self.deck.length() // 4
        for i in range(0, half):
            for player in self.players:
                player.draw(self.deck)

    def sort(self):
        for player in self.players:
            player.sort_hand()

    def dispose_cards(self):
        for player in self.players:
            player.sort_hand()
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

    """
    Here we check which player is the current player and switch currentPlayer to the other player.
    The last helper method we need on the engine is one that handles a player winning a round 
    (by calling "Snap!" correctly, or the other player falsely calling "Snap!").
     This method will change the state of the game. It will also add all the cards on the pile to the winner's hand.
    Then it will clear out the pile so the next round can start:
    """

    def winRound(self, player):
        self.state = GameState.SNAPPING
        player.hand.extend(self.pile.popAll())
        self.pile.clear()

    """
    Now we get to the main logic of the engine. This method will be called from our main game loop, which we will define later.
    Let's start with the method definition and some basic checks. Then we'll add the logic in sections. Start by adding this method to the engine:
    """

    def play(self, key):
        if key == None:
            return

        if self.state == GameState.ENDED:
            return
