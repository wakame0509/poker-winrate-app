import random
import pandas as pd
import eval7
from utils import evaluate_hand, generate_possible_hands, generate_deck, remove_known_cards

def run_monte_carlo_simulation(p1_card1, p1_card2, board, selected_range, num_simulations):
    wins = 0
    ties = 0

    deck = generate_deck()
    known_cards = [p1_card1, p1_card2] + board
    deck = remove_known_cards(deck, known_cards)

    for _ in range(num_simulations):
        sim_deck = deck.copy()
        random.shuffle(sim_deck)

        opp_hand = random.sample(selected_range, 1)[0] if selected_range else [sim_deck.pop(), sim_deck.pop()]

        remaining_board = board + [sim_deck.pop() for _ in range(5 - len(board))]

        p1_hand = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in remaining_board]
        p2_hand = [eval7.Card(opp_hand[0]), eval7.Card(opp_hand[1])] + [eval7.Card(c) for c in remaining_board]

        p1_score = evaluate_hand(p1_hand)
        p2_score = evaluate_hand(p2_hand)

        if p1_score > p2_score:
            wins += 1
        elif p1_score == p2_score:
            ties += 1

    winrate = (wins + ties / 2) / num_simulations * 100
    return winrate

def run_enumeration_simulation(p1_card1, p1_card2, board, selected_range):
    wins = 0
    ties = 0
    total = 0

    deck = generate_deck()
    known_cards = [p1_card1, p1_card2] + board
    deck = remove_known_cards(deck, known_cards)

    possible_opponent_hands = generate_possible_hands(deck)
    possible_boards = generate_possible_hands(deck, board_needed=(5 - len(board)))

    for opp_hand in possible_opponent_hands:
        if selected_range and opp_hand not in selected_range:
            continue

        for remaining_cards in possible_boards:
            full_board = board + remaining_cards

            p1_hand = [eval7.Card(p1_card1), eval7.Card(p1_card2)] + [eval7.Card(c) for c in full_board]
            p2_hand = [eval7.Card(opp_hand[0]), eval7.Card(opp_hand[1])] + [eval7.Card(c) for c in full_board]

            p1_score = evaluate_hand(p1_hand)
            p2_score = evaluate_hand(p2_hand)

            if p1_score > p2_score:
                wins += 1
            elif p1_score == p2_score:
                ties += 1

            total += 1

    winrate = (wins + ties / 2) / total * 100 if total > 0 else 0
    return winrate

def simulate_winrate_shift(p1_card1, p1_card2, board, selected_range):
    results = []
    deck = generate_deck()
    known_cards = [p1_card1, p1_card2] + board
    deck = remove_known_cards(deck, known_cards)

    for card in deck:
        hypothetical_board = board + [card]

        if len(hypothetical_board) > 5:
            continue

        winrate = run_enumeration_simulation(p1_card1, p1_card2, hypothetical_board, selected_range)
        results.append({'Card': card, 'Winrate': winrate})

    df = pd.DataFrame(results).sort_values(by='Winrate', ascending=False)
    return df

def simulate_winrate_shift_montecarlo(p1_card1, p1_card2, board, selected_range, num_simulations=10000):
    results = []
    deck = generate_deck()
    known_cards = [p1_card1, p1_card2] + board
    deck = remove_known_cards(deck, known_cards)

    for card in deck:
        hypothetical_board = board + [card]

        if len(hypothetical_board) > 5:
            continue

        winrate = run_monte_carlo_simulation(p1_card1, p1_card2, hypothetical_board, selected_range, num_simulations)
        results.append({'Card': card, 'Winrate': winrate})

    df = pd.DataFrame(results).sort_values(by='Winrate', ascending=False)
    return df
