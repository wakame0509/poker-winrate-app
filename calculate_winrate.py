import random
from collections import Counter
import numpy as np
from .utils import evaluate_hand, create_deck, remove_cards_from_deck


def monte_carlo_winrate(player_hand, opponent_range, community_cards, iterations=100000):
    wins, ties = 0, 0
    player_hand = list(player_hand)
    community_cards = list(community_cards)

    deck = create_deck()
    used_cards = player_hand + community_cards
    deck = remove_cards_from_deck(deck, used_cards)

    for _ in range(iterations):
        # ランダムな相手ハンドを opponent_range から選択
        opp_hand = random.choice(opponent_range)
        # 山札から相手のハンドが引けるかチェック
        if any(card not in deck for card in opp_hand):
            continue
        remaining_deck = [c for c in deck if c not in opp_hand]

        # 必要なコミュニティカードの数を補完
        needed = 5 - len(community_cards)
        board = community_cards + random.sample(remaining_deck, needed)

        # 評価
        p_score = evaluate_hand(player_hand + board)
        o_score = evaluate_hand(list(opp_hand) + board)

        if p_score > o_score:
            wins += 1
        elif p_score == o_score:
            ties += 1

    total = iterations
    losses = total - wins - ties
    return {
        "Win": round(wins / total * 100, 2),
        "Tie": round(ties / total * 100, 2),
        "Lose": round(losses / total * 100, 2),
    }


def simulate_winrate_shift(player_hand, opponent_range, community_cards, stage):
    results = {}
    full_deck = create_deck()
    used = player_hand + community_cards
    deck = remove_cards_from_deck(full_deck, used)

    for card in deck:
        next_community = community_cards + [card]
        if stage == "flop" and len(next_community) == 4:
            simulated = monte_carlo_winrate(player_hand, opponent_range, next_community, iterations=10000)
            results[card] = simulated["Win"]
        elif stage == "turn" and len(next_community) == 5:
            simulated = monte_carlo_winrate(player_hand, opponent_range, next_community, iterations=10000)
            results[card] = simulated["Win"]

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
