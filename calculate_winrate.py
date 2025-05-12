import random
from collections import Counter
from itertools import combinations
from utils import evaluate_hand, generate_possible_hands, generate_deck, remove_known_cards


def run_monte_carlo_simulation(hero, board, villain, deck, selected_range, simulations):
    win = tie = lose = 0

    for _ in range(simulations):
        temp_deck = deck.copy()
        random.shuffle(temp_deck)

        board_complete = board.copy()
        while len(board_complete) < 5:
            card = temp_deck.pop()
            board_complete.append(card)

        if selected_range:
            possible_villains = generate_possible_hands(temp_deck, selected_range, board_complete, hero)
            if not possible_villains:
                continue
            villain_hand = random.choice(possible_villains)
        elif villain:
            villain_hand = villain
        else:
            villain_hand = [temp_deck.pop(), temp_deck.pop()]

        hero_score = evaluate_hand(hero + board_complete)
        villain_score = evaluate_hand(villain_hand + board_complete)

        if hero_score > villain_score:
            win += 1
        elif hero_score == villain_score:
            tie += 1
        else:
            lose += 1

    return win, lose, tie


def run_enumeration_simulation(hero, board, villain, deck, selected_range):
    win = tie = lose = 0
    num_needed = 5 - len(board)

    for extra_cards in combinations(deck, num_needed):
        full_board = board + list(extra_cards)
        temp_deck = [c for c in deck if c not in extra_cards]

        if selected_range:
            villain_hands = generate_possible_hands(temp_deck, selected_range, full_board, hero)
        elif villain:
            villain_hands = [villain]
        else:
            villain_hands = list(combinations(temp_deck, 2))

        for villain_hand in villain_hands:
            hero_score = evaluate_hand(hero + full_board)
            villain_score = evaluate_hand(list(villain_hand) + full_board)
            if hero_score > villain_score:
                win += 1
            elif hero_score == villain_score:
                tie += 1
            else:
                lose += 1

    return win, lose, tie


def simulate_winrate_shift(hero, opponent_range, board, stage):
    shift_result = {}
    deck = generate_deck()
    known = hero + board
    deck = remove_known_cards(deck, known)

    for card in deck:
        next_board = board + [card]
        win, lose, tie = run_monte_carlo_simulation(hero, next_board, [], remove_known_cards(deck, [card]), opponent_range, 5000)
        total = win + tie + lose
        shift_result[card] = round(win / total * 100, 1)

    sorted_result = dict(sorted(shift_result.items(), key=lambda x: x[1], reverse=True))
    return sorted_result
