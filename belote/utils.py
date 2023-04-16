"""
Module utils
"""

non_trump_values = {1: 11, 7: 0, 8: 0, 9: 0, 10: 10, 11: 2, 12: 3, 13: 4}
trump_values = {1: 11, 7: 0, 8: 0, 9: 14, 10: 10, 11: 20, 12: 3, 13: 4}


def card_value(card, trump):
    if card.suit == trump:
        return trump_values[card.figure]
    else:
        return non_trump_values[card.figure]


def sort(cards, trump):
    cards.sort(
        key=lambda card: (
            card.suit == trump,
            str(card.suit),
            card_value(card, trump),
        ),
        reverse=True,
    )


def best_card(cards, trump, filter=None):
    tmp_cards = cards
    if filter:
        tmp_cards = [card for card in cards if card.suit==filter]

    best = tmp_cards[0]
    for card in tmp_cards[1:]:
        if card_value(card, trump) > card_value(best, trump):
            best = card
    return best


def get_points(cards, trump):
    return sum([card_value(card, trump) for card in cards])
