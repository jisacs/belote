from enum import Enum
import pygame
import random


# Now let's add in the suits we'll need for the cards. We'll use the Enum class to define the different suits.


class Position:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"x:{self.x}, y:{self.y}"


class Suits(Enum):
    CLUB = 0  # C KEY 99
    SPADE = 1  # S KEY 115
    HEART = 2  # H KEY 104
    DIAMOND = 3  # D KEY 100

    def suit(key):
        if key == 99:
            return Suits.CLUB
        elif key == 115:
            return Suits.SPADE
        elif key == 104:
            return Suits.HEART
        elif key == 100:
            return Suits.DIAMOND


# Alright, the boilerplate is out of the way. Now, lets define the Card class.
class Card:
    suit = None
    figure = None
    image = None
    pos = Position(0, 0)

    def __init__(self, suit, value, position=None):
        self.suit = suit
        self.figure = value
        self.image = pygame.image.load(
            "images/" + self.suit.name + "-" + str(self.figure) + ".svg"
        )
        self.pos = position

    def __repr__(self):
        return (
            "{" + str(self.suit) + ", " + str(self.figure) + ", " + str(self.pos) + "}"
        )


class Team:
    players = None
    score = 0
    name =  "No name"

    def __init__(self, name, players):
        self.players = players
        self.name = name

    def __str__(self):
        return self.name + str([player.name for player in self.players]) + ", score " + str(self.score)


class Deck:
    cards = None
    last_handle = None
    current_best_player = None

    def __init__(self):
        self.cards = []
        for suit in Suits:
            for value in [1, 7, 8, 9, 10, 11, 12, 13]:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def length(self):
        return len(self.cards)



CARD_LENGTH = 100


class BelotePlayer:
    non_trump_values = {1: 11, 7: 0, 8: 0, 9: 0, 10: 10, 11: 2, 12: 3, 13: 4}
    trump_values = {1: 11, 7: 0, 8: 0, 9: 14, 10: 10, 11: 20, 12: 3, 13: 4}
    hand = None
    position = None
    name = None
    next_spot = None

    def __init__(self, name, position):
        self.hand = []
        self.position = position
        self.name = name

    def draw(self, deck):
        self.hand.append(deck.deal())

    def throw(self, figure, deck,):
        deck.cards.append(self.hand.pop(figure - 1))
        self.dispose_cards()

    def count_suit(self, suit):
        result = 0
        for card in self.hand:
            if card.suit == suit:
                result += 1
        return result


    def dispose_cards(self):
        for index, card in enumerate(self.hand):
            card_x = self.position.x + index * card.image.get_size()[0] * 1.1 + 300
            card_y = self.position.y
            card.pos = Position(card_x, card_y)

    def play(self):
        return self.hand.pop(0)

    def __str__(self):
        return self.name
