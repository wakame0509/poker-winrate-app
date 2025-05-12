from treys import Card
import itertools


def convert_card_str_to_int(card_str):
    return Card.new(card_str)


def get_deck_minus_known_cards(known_cards):
    full_deck = Card.full_deck()
    return [card for card in full_deck if card not in known_cards]


def evaluate_hand(hand, community, evaluator):
    return evaluator.evaluate(hand, community)


def generate_all_hole_card_combinations():
    ranks = "23456789TJQKA"
    suits = "shdc"
    deck = [r + s for r in ranks for s in suits]
    combos = list(itertools.combinations(deck, 2))
    return combos
