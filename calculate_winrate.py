import random
from utils import evaluate_hand, generate_possible_hands

def run_monte_carlo_simulation(hero, board, villain, deck, selected_range, simulations):
    win = tie = lose = 0

    for _ in range(simulations):
        temp_deck = deck.copy()
        random.shuffle(temp_deck)

        # 残りのボードカードを補完
        board_complete = board.copy()
        while len(board_complete) < 5:
            card = temp_deck.pop()
            board_complete.append(card)

        # 相手ハンド
        if selected_range:
            possible_villains = generate_possible_hands(temp_deck, selected_range, board_complete, hero)
            if not possible_villains:
                continue
            villain_hand = random.choice(possible_villains)
            for c in villain_hand:
                temp_deck.remove(c)
        elif villain:
            villain_hand = villain
        else:
            villain_hand = [temp_deck.pop(), temp_deck.pop()]

        hero_rank = evaluate_hand(hero + board_complete)
        villain_rank = evaluate_hand(villain_hand + board_complete)

        if hero_rank > villain_rank:
            win += 1
        elif hero_rank == villain_rank:
            tie += 1
        else:
            lose += 1

    return win, lose, tie
