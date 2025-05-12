import random

RANK_ORDER = '23456789TJQKA'

def card_value(card):
    return RANK_ORDER.index(card[0])

def parse_card(card_str):
    rank = card_str[0]
    suit = card_str[1]
    return rank + suit

def generate_deck():
    suits = ['s', 'h', 'd', 'c']
    ranks = '23456789TJQKA'
    return [r + s for r in ranks for s in suits]

def remove_cards(deck, used_cards):
    return [card for card in deck if card not in used_cards]

def get_hand_from_range(hand_range, deck):
    while True:
        hand_str = random.choice(hand_range)
        r1, r2 = hand_str[0], hand_str[1]
        suited = 's' in hand_str
        offsuit = 'o' in hand_str
        candidates = []

        for c1 in deck:
            for c2 in deck:
                if c1 == c2:
                    continue
                if c1[0] == r1 and c2[0] == r2 or c1[0] == r2 and c2[0] == r1:
                    if suited and c1[1] == c2[1]:
                        candidates.append((c1, c2))
                    elif offsuit and c1[1] != c2[1]:
                        candidates.append((c1, c2))
                    elif not suited and not offsuit and c1[0] == c2[0]:
                        candidates.append((c1, c2))
        if candidates:
            return random.choice(candidates)
