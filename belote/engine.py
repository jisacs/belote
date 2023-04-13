from enum import Enum
import pygame
from models import *


class GameState(Enum):
    PLAYING = 0
    SNAPPING = 1
    ENDED = 2


class SnapEngine:
    deck = None
    player1 = None
    player2 = None
    pile = None
    state = None
    currentPlayer = None
    result = None

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player1 = Player("Player 1", pygame.K_q, pygame.K_w)
        self.player2 = Player("Player 2", pygame.K_o, pygame.K_p)
        self.pile = Pile()
        self.deal()
        self.currentPlayer = self.player1
        self.state = GameState.PLAYING

    def deal(self):
        half = self.deck.length() // 2
        for i in range(0, half):
            self.player1.draw(self.deck)
            self.player2.draw(self.deck)

    def switchPlayer(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

    """
    Here we check which player is the current player and switch currentPlayer to the other player.
    The last helper method we need on the engine is one that handles a player winning a round (by calling "Snap!" correctly, or the other player falsely calling "Snap!"). This method will change the state of the game. It will also add all the cards on the pile to the winner's hand. Then it will clear out the pile so the next round can start:
    """

    def winRound(self, player):
        self.state = GameState.SNAPPING
        player.hand.extend(self.pile.popAll())
        self.pile.clear()

    """
    Now we get to the main logic of the engine. This method will be called from our main game loop, which we will define later. Let's start with the method definition and some basic checks. Then we'll add the logic in sections. Start by adding this method to the engine:
    """

    def play(self, key):
        if key == None:
            return

        if self.state == GameState.ENDED:
            return
        """
        We'll call this main logic method play. It takes whatever key is currently pressed, and processes the logic for that. The first thing we check is if a key has actually been pressed. If it hasn't, we return, as there is nothing to update with the game state.
        The next check to make is if the game is over. If it is, we return, as again, there is nothing to do. If you want to improve the game, you could listen for a key press to restart the game.
        Now let's add some of the logic. The first thing is to check if the current player has pressed the key to play, or flip a card onto the pile. If they have pressed their flipKey, we call their play method and add the returned card to the pile. Then we switch turn to the next player, by calling our switchPlayer method.
        """
        if key == self.currentPlayer.flipKey:
            self.pile.add(self.currentPlayer.play())
            self.switchPlayer()
            """
          Next, let's check if any of the players have called "Snap!". We'll need to keep track of a few things: who called "Snap!", who didn't call "Snap!", and if there is a valid snap condition on the pile. Add this logic to the play method:
          """
            snapCaller = None
            nonSnapCaller = None
            isSnap = self.pile.isSnap()

            if key == self.player1.snapKey:
                snapCaller = self.player1
                nonSnapCaller = self.player2
            elif key == self.player2.snapKey:
                snapCaller = self.player2
                nonSnapCaller = self.player1
            """
            Here we create two variables, snapCaller and nonSnapCaller, which keep track of the player who called "Snap!" and the player who didn't call "Snap!". We also create a variable isSnap to keep track of whether there is a valid snap condition on the pile. Then we check if either of the players has called "Snap!". If they have, then we set the snapCaller and nonSnapCaller variables as applicable.
            We now know if "Snap!" has been called and which player called it. Let's add the logic to see if the player that called "Snap!" wins or loses. Add this logic to the play method:
            """
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
        We have two cases: one for a valid snap, and one for an invalid snap.
        If the pile is a valid snap, we call the winRound method on the player who called "Snap!". Then we set the result property to a dictionary with the winner, whether it was a valid snap, and the player who called "Snap!". This will be used for information when we make the game user interface (UI).
        Likewise, for an invalid snap, we call the winRound method on the player who didn't call "Snap!". Then we set the result property to a dictionary with the winner as the nonSnapCaller.
        In both cases, we call the winRound method with whichever player won the cards. Recall in the winRound method we assign the pile to the player's hand. Then we clear the pile, and set the gameState to SNAPPING.
        We've got just one last thing to check: if any player has run out of cards. If they have, then it means the other player wins. Add this logic to the play method:
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

