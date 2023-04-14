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
    CLUB = 0
    SPADE = 1
    HEART = 2
    DIAMOND = 3


# Alright, the boilerplate is out of the way. Now, lets define the Card class.
class Card:
    suit = None
    value = None
    image = None
    pos = Position(0, 0)

    def __init__(self, suit, value, position=None):
        self.suit = suit
        self.value = value
        self.image = pygame.image.load(
            "images/" + self.suit.name + "-" + str(self.value) + ".svg"
        )
        self.pos = position

    def __repr__(self):
        return (
            "{" + str(self.suit) + ", " + str(self.value) + ", " + str(self.pos) + "}"
        )


class Deck:
    cards = None

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


class Pile:
    cards = None

    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def peek(self):
        if len(self.cards) > 0:
            return self.cards[-1]
        else:
            return None

    def popAll(self):
        return self.cards

    def clear(self):
        self.cards = []

    def isSnap(self):
        if len(self.cards) > 1:
            return self.cards[-1].value == self.cards[-2].value
        return False


CARD_LENGTH = 100


class BelotePlayer:
    hand = None
    position = None
    name = None
    next_spot = None

    def __init__(self, name, position):
        self.hand = []
        self.position = position
        self.name = name

    def sort_hand(self):
        # sort list by `name` in reverse order
        self.hand.sort(key=lambda card: (str(card.suit), card.value,), reverse=False)

    def draw(self, deck):
        self.hand.append(deck.deal())

    def dispose_cards(self):
        for index, card in enumerate(self.hand):
            card_x = self.position.x + index * card.image.get_size()[0] * 1.1 + 300
            card_y = self.position.y
            card.pos = Position(card_x, card_y)

    def play(self):
        return self.hand.pop(0)
