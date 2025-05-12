from itertools import combinations
import random

SUITS = ['s', 'h', 'd', 'c']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']


def create_deck():
    return [rank + suit for rank in RANKS for suit in SUITS]


def remove_cards_from_deck(deck, cards_to_remove):
    return [card for card in deck if card not in cards_to_remove]


def card_value(card):
    rank_order = {r: i for i, r in enumerate(RANKS, 2)}
    return rank_order[card[0]]


def evaluate_hand(cards):
    """
    7枚のカードを受け取り、5枚の組み合わせの中で最高の役を評価する
    スコアは単純な強さ比較のためのスカラー値（大きいほど強い）
    """
    best_score = 0
    for combo in combinations(cards, 5):
        score = simple_hand_score(combo)
        if score > best_score:
            best_score = score
    return best_score


def simple_hand_score(hand):
    """
    役を簡易評価する（ハイカード〜フルハウス程度まで）
    将来的に改良の余地あり
    """
    values = sorted([card_value(c) for c in hand], reverse=True)
    suits = [c[1] for c in hand]
    value_counts = {v: values.count(v) for v in set(values)}

    is_flush = len(set(suits)) == 1
    is_straight = sorted(values) == list(range(min(values), max(values)+1)) and len(set(values)) == 5

    if is_straight and is_flush:
        return 900 + max(values)
    elif 4 in value_counts.values():
        return 800 + max(k for k, v in value_counts.items() if v == 4)
    elif sorted(value_counts.values()) == [2, 3]:
        return 700 + max(k for k, v in value_counts.items() if v == 3)
    elif is_flush:
        return 600 + values[0]
    elif is_straight:
        return 500 + max(values)
    elif 3 in value_counts.values():
        return 400 + max(k for k, v in value_counts.items() if v == 3)
    elif list(value_counts.values()).count(2) == 2:
        return 300 + max(k for k, v in value_counts.items() if v == 2)
    elif 2 in value_counts.values():
        return 200 + max(k for k, v in value_counts.items() if v == 2)
    else:
        return 100 + values[0]
