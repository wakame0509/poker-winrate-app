from itertools import combinations
import random

SUITS = ['s', 'h', 'd', 'c']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

def generate_deck():
    return [r + s for r in RANKS for s in SUITS]

def remove_known_cards(deck, known):
    return [card for card in deck if card not in known]

def parse_card_input(card_str):
    return [c.strip() for c in card_str.split() if len(c.strip()) == 2]

def evaluate_hand(cards):
    """
    与えられた7枚のカードから最強の5枚を評価し、数値スコアを返す。
    簡易スコアリング：大きいほど強い。
    """
    best_score = 0
    for combo in combinations(cards, 5):
        score = score_hand(combo)
        if score > best_score:
            best_score = score
    return best_score

def score_hand(hand):
    """簡易ハンド評価ロジック"""
    ranks = [card[0] for card in hand]
    suits = [card[1] for card in hand]
    rank_counts = {r: ranks.count(r) for r in set(ranks)}
    values = sorted([RANKS.index(r) for r in ranks], reverse=True)

    is_flush = len(set(suits)) == 1
    is_straight = len(set(values)) == 5 and max(values) - min(values) == 4

    if is_flush and is_straight:
        return 900 + max(values)
    elif 4 in rank_counts.values():
        return 800 + max(values)
    elif sorted(rank_counts.values()) == [2, 3]:
        return 700 + max(values)
    elif is_flush:
        return 600 + max(values)
    elif is_straight:
        return 500 + max(values)
    elif 3 in rank_counts.values():
        return 400 + max(values)
    elif list(rank_counts.values()).count(2) == 2:
        return 300 + max(values)
    elif 2 in rank_counts.values():
        return 200 + max(values)
    else:
        return 100 + max(values)

def generate_possible_hands(deck, range_labels, board, hero):
    # 簡易版: すべての2枚組み合わせを返す
    combos = []
    for i in range(len(deck)):
        for j in range(i + 1, len(deck)):
            h1, h2 = deck[i], deck[j]
            if h1 not in hero and h2 not in hero and h1 not in board and h2 not in board:
                combos.append([h1, h2])
    return combos
