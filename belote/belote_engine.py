from engine import Deck, GameState, Pile
from models import BelotePlayer
from models import Position

class BeleteEngine:
    deck = None
    player1 = None
    player2 = None
    player4 = None
    player4 = None
    state = None
    currentPlayer = None
    result = None

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player1 = BelotePlayer("Player 1", Position(50, 0))
        self.player2 = BelotePlayer("Player 2", Position(50, 150))
        self.player3 = BelotePlayer("Player 3", Position(50, 300))
        self.player4 = BelotePlayer("Player 4", Position(50, 450))
        self.players = [self.player1, self.player2, self.player3, self.player4,]
        self.pile = Pile()
        self.deal()
        self.currentPlayer = self.player1
        self.state = GameState.PLAYING

    def deal(self):
        half = self.deck.length() // 4
        for i in range(0, half):
            self.player1.draw(self.deck)
            self.player1.next_spot
            self.player2.draw(self.deck)
            self.player3.draw(self.deck)
            self.player4.draw(self.deck)

    def switchPlayer(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

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

        """
        if key == self.currentPlayer.flipKey:
            self.pile.add(self.currentPlayer.play())
            self.switchPlayer()

            snapCaller = None
            nonSnapCaller = None
            isSnap = self.pile.isSnap()

            if key == self.player1.snapKey:
                snapCaller = self.player1
                nonSnapCaller = self.player2
            elif key == self.player2.snapKey:
                snapCaller = self.player2
                nonSnapCaller = self.player1

            if isSnap and snapCaller:
                self.winRound(snapCaller)
                self.result = {
                    "winner": snapCaller,
                    "isSnap": True,
                    "snapCaller": snapCaller,
                }
                self.winRound(snapCaller)
            elif not isSnap and snapCaller:
                self.result = {
                    "winner": nonSnapCaller,
                    "isSnap": False,
                    "snapCaller": snapCaller,
                }
                self.winRound(nonSnapCaller)
        """

        """
        We have two cases: one for a valid snap, and one for an invalid snap.
        If the pile is a valid snap, we call the winRound method on the player who called "Snap!". Then we set the result property to a dictionary with the winner, whether it was a valid snap, and the player who called "Snap!". This will be used for information when we make the game user interface (UI).
        Likewise, for an invalid snap, we call the winRound method on the player who didn't call "Snap!". Then we set the result property to a dictionary with the winner as the nonSnapCaller.
        In both cases, we call the winRound method with whichever player won the cards. Recall in the winRound method we assign the pile to the player's hand. Then we clear the pile, and set the gameState to SNAPPING.
        We've got just one last thing to check: if any player has run out of cards. If they have, then it means the other player wins. Add this logic to the play method:
        """
        """
        if len(self.player1.hand) == 0:
            self.result = {
                "winner": self.player2,
            }
            self.state = GameState.ENDED
        elif len(self.player2.hand) == 0:
            self.result = {
                "winner": self.player1,
            }
            self.state = GameState.ENDED
        """